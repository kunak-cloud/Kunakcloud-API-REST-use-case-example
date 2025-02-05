import variables
import apiCallMethods
import json
from datetime import datetime
from auxiliary import  DbInsertDeviceData, DbGetLastMeasureTsFromSensor, DbDeleteRows, apiLogin

#   This function does the following
#       -   Add all the data from the specified device/s parameters, from the previous day
#       -   Include the data in the device databases
#       -   The function return as an integer the current number of api Calls have been done by the program
# 
#   Function arguments:
#       -   filtered_devices: List of devices that contain the following:
#               ·   Serial number
#               ·   Tag
#               ·   Status
#               ·   Last connection
#               ·   Latitude
#               ·   Longitude
#       -   newLastConnection: This value has, for each filtered device, a serial number and a newest last connection timestamp
#       -   oldLastConnection: This value has, for each filtered device, a serial number and a previous connection timestamp
#       -   frequency:         Frequency in which an API call is performed
#       -   apiCalls:          This argument is passed into the function in order to track the API call counts
def extractAndAddToDb(filtered_devices, newLastConnection, oldLastConnection, oldLastConnectionDeviceList, frequency, apiCalls):
    if len(filtered_devices) > 1:
        #   For each 10 devices in the filtered device list, make an API call for 10 devices
        for x in range (0, len(filtered_devices), 10):  
            newLastConnectionDeviceList = []
            devices_id = []
            #   The filtered list is sliced and an array of 10 devices is obtained in the loop. In the next loop the next 10 devices are sliced from the list. 
            filtered_ten_by_ten_devices = filtered_devices[ x : x + 10 ]
            for device in filtered_ten_by_ten_devices:
                devices_id.append(device['serial_number'])            
                newLastConnectionDeviceList.append( device[ 'last_connection_ts' ] )
            if(oldLastConnectionDeviceList != [] and newLastConnectionDeviceList == oldLastConnectionDeviceList):
                print( 'All the devices {} were not connected to Kunak Cloud yet and there is no new data'.format( filtered_devices ) )
            else:
                newLastConnectionFromDevice = min(newLastConnectionDeviceList)
                sensors = variables.sensors
                startTs =   ( ( newLastConnectionFromDevice - frequency ) if ( variables.start_ts == '' )  else ( variables.start_ts ))
                endTs   =   newLastConnectionFromDevice
                responseDevice = apiLogin.session.post(apiCallMethods.url_prefix + apiCallMethods.read_from_to_multiple_devices_group_by_ts(), data = json.dumps({
                    "devices"   :   devices_id,
                    "sensors"   :   sensors,
                    "startTs"   :   startTs,
                    "endTs"     :   endTs,
                    "number"    :   40000
                }))
                print('START_TS_DEVICES {}'.format(devices_id))

                # Insert data
                #   Parsing data obtained from the HTTP petition as JSON, so the data can be processed
                data_from_devices =  responseDevice.json()

                #   Delete all rows from the temporary device table
                DbDeleteRows.delete_rows_devices('device_data_temporary', devices_id)

                #   Insert the JSON data to the temporary and full device table
                DbInsertDeviceData.insertDataMultipleDevice(data_from_devices)
                print('Api call - Get reads fromTo: Multiple elements - for multiple devices {}'.format(devices_id))
                print ('Inserted data from DEVICES {}, from {} to {} in the DEVICE database'.format(devices_id, datetime.fromtimestamp(int(startTs)/1000) , datetime.fromtimestamp(int(endTs)/1000)) )
                
                #   The API call counter increase by one unit per filtered device
                apiCalls += 1
    if len(filtered_devices) == 1:
    #   For each device from the filered ones...
        for device in filtered_devices:
            #   Variable that contain the serial number from this device
            device_id = str(device['serial_number'])
            #   Variable that contain new last connection from this device
            newLastConnectionFromDevice = device['last_connection_ts']
            
            #   Prior to start making API calls, this validator check if the device has connected to the cloud:
            #       -   The device was in the list of devices that connected to the cloud before
            #       AND
            #       -   +   The device is in the list and it has data/timestamp
            #           OR
            #           +   The device's new connection date is not the same as the old connection date
            #
            #   If the conditions does not match, the program does the following:
            #       -   The console print the warning
            #       -   The program avoid to make an API call

            if ( device_id in oldLastConnection ) and (( oldLastConnection[device_id] is None ) or ( int(newLastConnectionFromDevice) <= int(oldLastConnection[device_id])) ):
                print('device {} was not connected to Kunak Cloud yet and there is no new data'.format(device_id))
            
            else:
                #   Variable that has the sensors specified in 'auxiliary/variables.py' file > 'sensors' variable
                sensors =   variables.sensors

                #   the start of the period in which we want to extract data is based on the following:
                #   -   If the device table does not have last connection date for this device, the value will be the new connection date minus the frequency from the 
                #       API call
                #   -   If the device table does have last connection date for this device, the startTs will be calculated in the file 
                #       'app/auxiliary/DbGetLastMeasureTsFromSensor.py'
                startTs =   ( ( newLastConnectionFromDevice - frequency ) if ( variables.start_ts == '' )  else ( variables.start_ts ))  if  ( DbGetLastMeasureTsFromSensor.extractFromDeviceList(device_id) == [] )  else  ( min(DbGetLastMeasureTsFromSensor.extractFromDeviceList(device_id))[0] )
                endTs   =   newLastConnectionFromDevice            

                #   HTTP POST petition ( https://en.wikipedia.org/wiki/POST_(HTTP) )
                #   In this API call method, we send our credentials (session), the device id, the sensors, the start and the end of the data range  
                responseDevice = apiLogin.session.post(apiCallMethods.url_prefix + apiCallMethods.read_from_to_single_device(device_id), data = json.dumps({
                    "sensors" :   sensors,
                    "startTs" :   startTs,
                    "endTs"   :   endTs
                }))
                print('START_TS_DEVICE {}'.format(device_id))

                #   Parsing data obtained from the HTTP petition as JSON, so the data can be processed
                data_from_single_device =  responseDevice.json()

                #   Delete all rows from the temporary device table
                DbDeleteRows.delete_rows_device('device_data_temporary', device_id)

                #   Insert the JSON data to the temporary and full device table
                DbInsertDeviceData.insertDataOneDevice(data_from_single_device, device_id)
                print('Api call - Get reads fromTo: Multiple elements - for device {}'.format(device_id))
                print ('Inserted data from DEVICE {}, from {} to {} in the DEVICE database'.format(device_id, datetime.fromtimestamp(int(startTs)/1000) , datetime.fromtimestamp(int(endTs)/1000)) )
                
                #   The API call counter increase by one unit per filtered device
                apiCalls += 1
            
            #   As new data has been inserted, the new last connection is saved as old last connection in order to compare it the next time an API call is done for
            #   this device
            oldLastConnection[device_id] = newLastConnectionFromDevice
        
    else:
        print('The list of filtered devices is empty. Try to put the correct serial numbers')
        
    return apiCalls
