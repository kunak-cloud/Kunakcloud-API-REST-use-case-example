from auxiliary import DbConnect

#   This function extract from the database a list of the newest timestamps from a device, grouped by parameters
def extractFromDeviceList(device_id):
    DbConnect.cursor.execute(""" SELECT MAX(device_ts)  FROM device_data_all_data  WHERE  device_serial_number =  %s GROUP BY device_sensor_tag""" ,( device_id, ))
    result = DbConnect.cursor.fetchall()
    return result

#   This function extract from the database a list of the newest timestamps from a location, grouped by device and parameters
def extractFromLocationList(location_id):
    DbConnect.cursor.execute(""" SELECT MAX(location_ts)  FROM location_data_all_data  WHERE  location_id =  %s GROUP BY location_serial_number, location_sensor_tag""" ,( location_id, ))
    result = DbConnect.cursor.fetchall()
    return result
