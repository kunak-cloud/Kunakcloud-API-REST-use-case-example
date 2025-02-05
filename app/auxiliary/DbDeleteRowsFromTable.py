from auxiliary import DbConnect ,DbCreateTable
import variables

#     A full day of data is not removed because data from last frequency has not been added yet because the deletion of rows happen with the new data 
#     from that frequency not being added yet
#     i.e. if API call frequency is one hour, at hour 24 we remove 24 - 1 = 23
def delete_rows_table(table):
      DbConnect.cursor.execute(""" DELETE FROM {}  WHERE device_ts > (SELECT MAX(device_ts) FROM {}) - {}"""
                               .format(table, table,( variables.dayInMs() - variables.apiCallFrequencyMs() ) ) )
      