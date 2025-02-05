from auxiliary import DbConnect

#   From 'app/auxiliary/DbConnect.py' file, we use psycopg2. In that file, we initialized the library an the cursor. 
#   The cursor property is used for interacting with the database. In this case, we use it for creating the tables.
#
#   'create_table' variable is a SQL request as a string:
#       -   It request to create a table if it doesn't exist.

#       -   The fields are defined with different types: strings with maximum 200 characters (VARCHAR (200)), decimals,
#           Big numbers (BIGNINT), values as timestamp, etc.

#       -   UNIQUE property is used for avoiding row duplication in our records. In this case, using PostgreSQL, we indicated
#           that we want that, for each row in the table, the following:
#           +   For the device table, a row with the serial number, the sensor tag and the timestamp values, concatenated, is unique
#           +   For the location table, a row with the location id value and the serial number, the sensor tag and the timestamp 
#               values from each device, concatenated, is unique
#

def createDeviceTable(table):
    create_table =""" CREATE TABLE IF NOT EXISTS {} (
                   device_serial_number VARCHAR (200),
                   device_sensor_tag VARCHAR(200),
                   device_value DECIMAL,
                   device_validation VARCHAR(2),
                   device_reason INT,
                   device_ts BIGINT,
                   date_UTC TIMESTAMP,
                   UNIQUE (device_serial_number, device_sensor_tag, device_ts)
                   ) """.format(table)
    DbConnect.cursor.execute(create_table)

def createLocationTable(table):
    create_table =""" CREATE TABLE IF NOT EXISTS {} (
                   location_id VARCHAR (200),
                   location_serial_number VARCHAR (200),
                   location_sensor_tag VARCHAR(200),
                   location_value DECIMAL,
                   location_validation VARCHAR(2),
                   device_reason INT,
                   location_ts BIGINT,
                   date_UTC TIMESTAMP,
                   UNIQUE (location_id, location_serial_number, location_sensor_tag, location_ts)
                   ) """.format(table)
    DbConnect.cursor.execute(create_table)
