import datetime
from auxiliary import DbConnect

#   This function does the following:
#   -   Insert data to the full location table
#   -   Insert data to the temporary location table

#   The response from the API call is an array of data, containing the following:
#   -   Serial number
#   -   Sensor_tag:             Name of the requested parameter (i.e. battery)
#   -   location_value:         Parameter value
#   -   location_validation:    Validation tag from parameter
#   -   location_ts:            Date in timestamp
#   -   date_UTC:               Date in UTC

def insertData(data_from_single_location, location_id):
    #   For each data entry from the response array...
    for data_entry in data_from_single_location:
        #   Add the data to the full location table
        #   Note:   On our tables, we defined that the values from our table are UNIQUE and, if there is a conflict ( duplicate values), it DOES NOTHING.
        #           In this case, if we try to insert a entry with a serial number, sensor tag and timestamp from this measure and this entry is already in the table it DOes NOTHING.            
        #           If this condition is not specified in the SQL request, the program stop working.
        DbConnect.cursor.execute( """ INSERT INTO location_data_all_data (location_id, location_serial_number, location_sensor_tag, location_value, location_validation, device_reason, location_ts, date_UTC)
                                VALUES ( %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (location_id, location_serial_number, location_sensor_tag, location_ts) DO NOTHING""",
                                    ( str(location_id), str(data_entry['device_serial_number']), data_entry['sensor_tag'], float(data_entry['value']), data_entry['validation'], data_entry['reason'], int(data_entry['ts']), datetime.datetime.fromtimestamp((int(data_entry['ts']))/1000 ) ) )
        DbConnect.cursor.execute( """ INSERT INTO location_data_temporary (location_id, location_serial_number, location_sensor_tag, location_value, location_validation, device_reason, location_ts, date_UTC)
                                VALUES ( %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (location_id, location_serial_number, location_sensor_tag, location_ts) DO NOTHING""",
                                    ( str(location_id), str(data_entry['device_serial_number']), data_entry['sensor_tag'], float(data_entry['value']), data_entry['validation'], data_entry['reason'], int(data_entry['ts'] ), datetime.datetime.fromtimestamp((int(data_entry['ts']))/1000) ) )
    