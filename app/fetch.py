import requests
import variables
import apiCallMethods
from auxiliary import DbConnect, apiDevicesConnectionTime, apiDeviceData, DbCreateTable, filterDevices, apiLocationsConnectionTime, apiLocationData, apiDevicesGetValidationLogs, apiLocationsGetValidationLogs, filterLocations

#   The apiCalls value is 0 by default. Once API calls are requested, the number will increase and the value will be logged into the console
apiCalls = 0

#   The cumulatedApiFrequencyInMs variable is going to increase in each API frequency. The purpose is that, each day, as the values from the parameters might get invalidated by the cloud, 
#   this variable work as a counter. Each day, the counter reach to its limit and the API call regarding the validation is requested
cumulatedApiFrequencyInMs = 0

#   Credential variables that are initialized in the 'auxiliary/variables.py' file
user_id = variables.user
password = variables.password

#   Setting up the Session library. It let us make HTTP requests in Python
session = requests.Session()

#   This method from the Session library let us login into the API site
session.auth = (user_id, password)
auth = session.post(apiCallMethods.url_prefix)

#   Initializing variables related to the connection time from the devices and the device data
oldLastConnection = {}
oldLastConnectionDeviceList = {}
newLastConnection = {}
data_devices = {}

#   This function request data from devices and locations and, at the end, it logs the number of API calls that were done during the operation
def getData ():
    #   The variables from previous lines are declared as global in order to use it in this function
    global oldLastConnection
    global newLastConnection
    global data_devices
    global apiCalls
    global cumulatedApiFrequencyInMs
    global oldLastConnectionDeviceList

    #   Autocommit allow to make changes in the database
    DbConnect.conn.autocommit = True

    #   If the user Kunak Cloud user credentials are not configured, the program cannot continue
    if variables.user == "" or variables.password == "":
        print('The user and password from your Kunak Cloud account are not configured in this program.\nExit the program, go to the variables.py file and configure the credentials.\nFinally, run this program again.')
        return
    else:
        #   If, in the 'auxiliary/variables.py' file, the 'device_id' variable contain one or more device ids
        if(len(variables.device_id) > 0):
            #   If the device table does not exist, the program create the device data, with all data from the devices
            DbCreateTable.createDeviceTable( 'device_data_all_data' )

            #   If the device table does not exist, the program create a table with the last data collected from devices
            DbCreateTable.createDeviceTable( 'device_data_temporary' )      

            #   We request information from all the devices API call 'List all devices' Please review the 'List all devices' API call in the official Kunak Cloud site   
            #   The information that send is the following: serial nuber, tag, status, last connection, latitude and longitude
            #   We are interested in the serial number and the last connection values.
            device_list = apiDevicesConnectionTime.extract()
            #   The API call counter increase by 1
            apiCalls +=1

            #   The response from the API call is going to send information from all the devices associated with the account. The list will be filtered according 
            #   to the specified devices in the 'auxiliary/variables.py' file ( i.e. My account has 200 devices, but I want data from just 3 devices. )
            filtered_devices = filterDevices.filter( device_list )
            
            #   The device data from the API is extracted and added to the device database
            apiCalls = apiDeviceData.extractAndAddToDb( filtered_devices, oldLastConnection, newLastConnection, oldLastConnectionDeviceList, variables.apiCallFrequencyMs(), apiCalls )

            #   If the program was running less than one day, the program request the data from the filtered devices and include it into the databases.
            if( variables.dayInMs() > cumulatedApiFrequencyInMs ):
                #   The cumulatedApiFrequencyInMs counter is increased by the API call frequency, measured in miliseconds
                cumulatedApiFrequencyInMs += variables.apiCallFrequencyMs()

            #   If the program was running more than one day, the program remove from the device table the records from the previous day and request the data from 
            #   the previous day
            else:
                print( 'Because validations tags may get modified, the data from previous day is going to get updated for devices.' )
                #   Remove from the device table the records from the previous day
                #DbDeleteRowsFromTable.delete_rows_table( 'device_data_all_data' )
                #   The devices data is extracted and added to the device database
                apiCalls = apiDevicesGetValidationLogs.extract( apiCalls )
                cumulatedApiFrequencyInMs = variables.apiCallFrequencyMs()
                print('Data validation process has been completed.')

        #   If, in the 'auxiliary/variables.py' file, the 'location_id' variable contain one or more device ids
        if(len(variables.location_id) > 0):
            #   If the location table does not exist, the program create the location data, with all data from the locations
            DbCreateTable.createLocationTable( 'location_data_all_data' )

            #   If the location table does not exist, the program create a table with the last data collected from locations
            DbCreateTable.createLocationTable( 'location_data_temporary' )
            
            #   We request information from all the locations API call 'List all locations'. Please review the 'List all locations' API call in the official Kunak Cloud site  
            #   The information that send is the following: serial nuber, tag, status, last connection, latitude and longitude
            #   We are interested in the serial number and the last connection values.
            location_list = apiLocationsConnectionTime.extract()

            #   The API call counter increase by 1
            apiCalls +=1
        
            #   The response from the API call is going to send information from all the locations associated with the account. The list will be filtered according 
            #   to the specified locations in the 'auxiliary/variables.py' file ( i.e. My account has 15 locations, but I want data from just 2 locations. )
            filtered_locations = filterLocations.filter( location_list )
            
            #   If the program was running less than one day, the program request the data from the filtered locations and include it into the databases.
            if( variables.dayInMs() > cumulatedApiFrequencyInMs ):
                #   The location data from the API is extracted and added to the location database
                apiCalls = apiLocationData.extractAndAddToDb( filtered_locations, newLastConnection, oldLastConnection, variables.apiCallFrequencyMs(), apiCalls )

            #   If the program was running more than one day, the program remove from the location table the records from the previous day and request the data from 
            #   the previous day
            else:
                print( 'Because validations tags may get modified, the data from previous day is going to get updated for locations.' )
                apiCalls = apiLocationsGetValidationLogs.extract( newLastConnection , apiCalls )            
                print('Data from previous day has been updated.')    
        if((len(variables.device_id) > 0) or (len(variables.location_id) > 0) ):
            #   The cumulatedApiFrequencyInMs counter is increased by the API call frequency, measured in miliseconds
            cumulatedApiFrequencyInMs += variables.apiCallFrequencyMs()
            
        print( 'The app has done {} api calls.'.format ( apiCalls )) 
        return 
