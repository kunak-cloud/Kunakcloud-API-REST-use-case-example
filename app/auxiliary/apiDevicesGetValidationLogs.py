import variables
import apiCallMethods
import json
from datetime import datetime
from auxiliary import DbReplaceDeviceData, apiLogin, apiDeviceData, DbDeleteRows, DbInsertDeviceData

# This API call will give us the list of changes that were done to the data from specific devices that have to be defined in variables.py
# The result from the API will be an object array. Each object has the following information:
#   - serial_number from one device
#   - sensor_tag: Which sensor validation flag was modified
#   - action: Was the data Validated(V), was it invalidated(I) etc.?
#   - action_ts: When was this change applied to the data?
#   - range: Period in which the data validation flag is modified (indicated by start_ts and end_ts)
#   - reason: Explain why the data was invalidated

def extract( apiCalls ):
    response = apiLogin.session.post(apiCallMethods.url_prefix + apiCallMethods.read_devices_validation_log(), data = json.dumps({
        "devices": variables.device_id,
        "startTs":( variables.currentTimeInMs() - variables.dayInMs() ) ,
        "endTs": ( variables.currentTimeInMs() )
    }))
    log_list = response.json()
    apiCalls+=1
    for log in log_list:
        if (not 'message' in log) and not (log == []):
            if log['action'] == 'O':
                #   HTTP POST petition ( https://en.wikipedia.org/wiki/POST_(HTTP) )
                #   In this API call method, we send our credentials (session), the device id, the sensors, the start and the end of the data range  
                responseDevice = apiLogin.session.post(apiCallMethods.url_prefix + apiCallMethods.read_from_to_single_device("".join(str(x) for x in log['serial_number'])), data = json.dumps({
                    "sensors" :   [log['sensor_tag']],
                    "startTs" :   log['range']['start_ts'],
                    "endTs"   :   log['range']['end_ts']
                }))
                print('START_TS_DEVICE {}'.format(log['range']['start_ts']))

                #   Parsing data obtained from the HTTP petition as JSON, so the data can be processed
                data_from_single_device =  responseDevice.json()

                #   Insert the JSON data to the temporary and full device table
                if (not 'message' in data_from_single_device) and not (data_from_single_device == []):
                    DbReplaceDeviceData.replace('', data_from_single_device, log['serial_number'] )
                    print('Api call - Get reads fromTo: Multiple elements - for device {}'.format(log['serial_number']))
                    print ('Inserted data from DEVICE {}, from {} to {} in the DEVICE database'.format(log['serial_number'], datetime.fromtimestamp(int(log['range']['start_ts'])/1000) , datetime.fromtimestamp(int(log['range']['end_ts'])/1000)) )
                else:
                    print('There is no data to upload from device {}'.format([log['serial_number']]))
                #   The API call counter increase by one unit per filtered device
                apiCalls += 1
            else:
                DbReplaceDeviceData.replace(log_list, '', '')
        else:
            print('In the validation logs, there is no data to add')
    
    return apiCalls
