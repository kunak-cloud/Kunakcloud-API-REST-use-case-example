from auxiliary import DbConnect

# Once the list of data with the validation logs is obtained (object array), it is necessary to update the validation flags in the database.
# For each object in the array, we replace the validation flag and the reason, filtering by location_id, location_sensor tag, applying the change
# to a data range, defined by the start_ts and end_ts

def replace(log_list):
    if (not 'message' in log_list) or not(log_list == []):
        for log in log_list:
            DbConnect.cursor.execute("""
                                            UPDATE location_data_all_data  SET location_validation = %s, device_reason = %s
                                                WHERE location_id = %s
                                                    AND location_sensor_tag = %s
                                                    AND location_ts >= %s 
                                                    AND location_ts <= %s
                                    """,
                                    (log['action'],log['reason'], log['location_id'], log['sensor_tag'], log['range']['start_ts'], log['range']['end_ts']) 
                                    )
    else:
        print('There is no data to update')
        