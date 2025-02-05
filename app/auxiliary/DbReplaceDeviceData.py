from auxiliary import DbConnect

# Once the list of data with the validation logs is obtained (object array), it is necessary to update the validation flags in the database.
# For each object in the array, we replace the validation flag and the reason, filtering by location_id, location_sensor tag, applying the change
# to a data range, defined by the start_ts and end_ts

def replace(log_list, data_from_single_device, serial_number):
    #   If the list of validation logs has only data flags to replace (Invalidate, Validate flag, etc.). It is necessary to replace flag and value
    if data_from_single_device == '' and log_list != '':
        for log in log_list:
            DbConnect.cursor.execute("""
                                            UPDATE device_data_all_data  SET device_validation = %s, device_reason = %s
                                                WHERE device_serial_number = %s 
                                                    AND device_sensor_tag = %s
                                                    AND device_ts >= %s 
                                                    AND device_ts <= %s
                                    """,
                                    (log['action'],(log['reason']), log['serial_number'], log['sensor_tag'], log['range']['start_ts'], log['range']['end_ts']) 
                                    )
    #   If the list of validation logs has the 'Corrected' / 'O' flag, it means that previous data has been modified. It is necessary to replace flag and value
    if log_list == '' and data_from_single_device != '':
        for data_register in data_from_single_device:
            DbConnect.cursor.execute("""
                                            UPDATE device_data_all_data  SET device_validation = %s, device_reason = %s, device_value = %s
                                                WHERE device_serial_number = %s 
                                                    AND device_sensor_tag = %s
                                                    AND device_ts = %s 
                                                    AND device_ts <= %s
                                    """,
                                    (data_register['validation'],(data_register['reason']), data_register['value'] , serial_number, data_register['sensor_tag'], data_register['ts'], data_register['ts']) 
                                    )
    else:
        print('There is no data to update')
        