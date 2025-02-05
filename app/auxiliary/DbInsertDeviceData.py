import datetime
from auxiliary import DbConnect

#   This function does the following:
#   -   Insert data to the full device table
#   -   Insert data to the temporary device table

#   The response from the API call is an array of data, containing the following:
#   -   Serial number
#   -   Sensor_tag:             Name of the requested parameter (i.e. battery)
#   -   device_value:           Parameter value
#   -   device_validation:      Validation tag from parameter
#   -   Device_ts:              Date in timestamp
#   -   date_UTC:               Date in UTC


def insertDataOneDevice(data_from_single_device, device_id):
    #   For each data entry from the response array...
    for data_entry in data_from_single_device:

        #   Add the data to the full device table
        #   Note:   On our tables, we defined that the values from our table are UNIQUE and, if there is a conflict ( duplicate values), it DOES NOTHING.
        #           In this case, if we try to insert a entry with a serial number, sensor tag and timestamp from this measure and this entry is already in the table it DOES NOTHING.            
        #           If this condition is not specified in the SQL request, the program stop working.
        DbConnect.cursor.execute( """ 
                                INSERT INTO device_data_all_data (device_serial_number, device_sensor_tag, device_value, device_validation, device_reason, device_ts, date_UTC)
                                VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (device_serial_number, device_sensor_tag, device_ts) DO NOTHING""",
                                    ( str(device_id), data_entry['sensor_tag'], float(data_entry['value']), data_entry['validation'], data_entry['reason'], int(data_entry['ts']), datetime.datetime.fromtimestamp((int(data_entry['ts']))/1000 ) ) )
        
        #   Add the data to the temporary device table
        DbConnect.cursor.execute( """ 
                                INSERT INTO device_data_temporary (device_serial_number, device_sensor_tag, device_value, device_validation, device_reason, device_ts, date_UTC)
                                VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (device_serial_number, device_sensor_tag, device_ts) DO NOTHING""",
                                    ( str(device_id), data_entry['sensor_tag'], float(data_entry['value']), data_entry['validation'], data_entry['reason'], int(data_entry['ts'] ), datetime.datetime.fromtimestamp((int(data_entry['ts']))/1000) ) )

def insertDataMultipleDevice(data_from_devices):
        ts = 0
        serial_number = 0
        for data_entry in data_from_devices:
            for key, data in data_entry.items():
                if key == 'ts':
                     ts = data
                     continue
                serial_number = key
                for sensor_parameter, sensor_value in data.items():
                    DbConnect.cursor.execute( """ 
                                INSERT INTO device_data_temporary (device_serial_number, device_sensor_tag, device_value, device_validation, device_reason, device_ts, date_UTC)
                                VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (device_serial_number, device_sensor_tag, device_ts) DO NOTHING""",
                                    ( str( serial_number ), sensor_parameter, float( sensor_value[ 'value' ] ), sensor_value[ 'validation' ], sensor_value[ 'reason' ], int( ts ), datetime.datetime.fromtimestamp( ( int( ts ) ) / 1000 )  ) )

                    DbConnect.cursor.execute( """ 
                                INSERT INTO device_data_all_data (device_serial_number, device_sensor_tag, device_value, device_validation, device_reason, device_ts, date_UTC)
                                VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (device_serial_number, device_sensor_tag, device_ts) DO NOTHING""",
                                    ( str( serial_number ), sensor_parameter, float( sensor_value[ 'value' ] ), sensor_value[ 'validation' ], sensor_value[ 'reason' ], int( ts ), datetime.datetime.fromtimestamp( ( int( ts ) ) / 1000 )  ) )

