import variables
import apiCallMethods
import json
from datetime import datetime
from auxiliary import  DbInsertLocationData, DbGetLastMeasureTsFromSensor, DbDeleteRows, apiLogin

#   This function does the following
#       -   Add all the data from the specified location/s parameters, from the previous day
#       -   Include the data in the location databases
#       -   The function return as an integer the current number of api Calls have been done by the program    
#
#   Function arguments:
#       -   filtered_locations: List of locations that contain the following:
#               ·   Location ID
#               ·   Serial number from device
#               ·   Tag from device
#               ·   Status from device
#               ·   Last connection from device
#               ·   Latitude from device
#               ·   Longitude from device
#       -   newLastConnection: This value has, for each filtered location, a serial number and a newest last connection timestamp
#       -   oldLastConnection: This value has, for each filtered location, a serial number and a previous connection timestamp
#       -   frequency:         Frequency in which an API call is performed
#       -   apiCalls:          This argument is passed into the function in order to track the API call counts
#
def extractAndAddToDb(filtered_locations, newLastConnection, oldLastConnection, frequency, apiCalls):
    #   For each location from the filered ones...
    for location in filtered_locations:
        #   Variable that contain the location ID from this location
        location_id = str(location['location_id'])
        #   Variable that contain new last connection from this location and devices
        newLastConnection = ''
        newLastConnectionsFromLocations = []

        #   For each device from this location...
        for device in location['device_list']:
            #   If the device is currently installed in the location, the last connection timestamp will be taken from this device
            if device['end_date'] == 'currently':
                newLastConnectionsFromLocations.append(device['last_connection_ts'])
        
        #   After this for loop, an array with timestamps will generate. The oldest timestamp will be the end of the data range to take data
        newLastConnection = min(newLastConnectionsFromLocations)
        
        #   Prior to start making API calls, this validator check if the location has connected to the cloud:
        #       -   The location was in the list of locations that connected to the cloud before
        #       AND
        #       -   +   The location is in the list and it has data/timestamp
        #           OR
        #           +   The location's new connection date is not the same as the old connection date
        #
        #   If the conditions does not match, the program does the following:
        #       -   The console print the warning
        #       -   The program avoid to make an API call
        if ( location_id in oldLastConnection ) and (( oldLastConnection[location_id] is None ) or ( int(newLastConnection) <= int(oldLastConnection[location_id])) ):
            print('location {} was not connected to Kunak Cloud yet and there is no new data'.format(location_id))
            
        else:
            #   Variable that has the sensors specified in 'auxiliary/variables.py' file > 'sensors' variable
            sensors = variables.sensors

            #   the start of the period in which we want to extract data is based on the following:
            #   -   If the location table does not have last connection date for this location, the value will be the new connection date minus the frequency 
            #       from the API call
            #   -   If the location table does have last connection date for this location, the startTs will be calculated in the file 
            #       'app/auxiliary/DbGetLastMeasureTsFromSensor.py'
            
            startTs = ( ( newLastConnection - frequency ) if (variables.start_ts == '') else (variables.start_ts) )  if  ( DbGetLastMeasureTsFromSensor.extractFromLocationList(location_id) == [] )  else  ( min(DbGetLastMeasureTsFromSensor.extractFromLocationList(location_id))[0] )
            endTs   = newLastConnection
            
            #   HTTP POST petition ( https://en.wikipedia.org/wiki/POST_(HTTP) )
            #   In this API call method, we send our credentials (session), the location id, the sensors, the start and the end of the data range  
            responseLocation = apiLogin.session.post(apiCallMethods.url_prefix + apiCallMethods.read_from_to_single_location(location_id),
                data = json.dumps({
                    "sensors" : sensors,
                    "startTs" : startTs,
                    "endTs" :  endTs
                    }
                )
            )
            print('START_TS_LOCATION {}'.format(location_id))

            #   Parsing data obtained from the HTTP petition as JSON, so the data can be processed
            data_from_single_location =  responseLocation.json()

            #   Delete all rows from the temporary location table
            DbDeleteRows.delete_rows_location('location_data_temporary', location_id)
            
            #   Insert the JSON data to the temporary and full location table
            DbInsertLocationData.insertData(data_from_single_location, location_id)
            print('Api call - Get reads fromTo: Multiple elements - for location {}'.format(location_id))
            print('Inserted data from LOCATION {} between {} and {} in the LOCATION database'.format(location_id,  datetime.fromtimestamp(int(startTs)/1000) , datetime.fromtimestamp(int(endTs)/1000) ))
            
            #   The API call counter increase by one unit per filtered location
            apiCalls += 1
        
        #   As new data has been inserted, the new last connection is saved as old last connection in order to compare it the next time an API call is done 
        #   for this location
        oldLastConnection[location_id] = newLastConnection
        
    return apiCalls
