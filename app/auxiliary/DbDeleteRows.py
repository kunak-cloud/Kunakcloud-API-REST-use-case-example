from auxiliary import DbConnect

def delete_rows_device(table, device_id):
      DbConnect.cursor.execute('DELETE from {} where device_serial_number = %s'.format(table) , (device_id,))

def delete_rows_devices(table, device_id):
      for device in device_id:
            DbConnect.cursor.execute('DELETE from {} where device_serial_number = %s'.format(table) , (device,))

def delete_rows_location(table, location_id):
      DbConnect.cursor.execute('DELETE from {} where location_serial_number = %s'.format(table) , (location_id,))
      