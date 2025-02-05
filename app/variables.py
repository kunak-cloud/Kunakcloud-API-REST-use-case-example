import datetime

#region Common data
user =              '' # 'user'
password =          '' # 'password1234'

sensors =           [  ] # ['PM1', 'PM2.5', 'PM10']
 
# Timestamp in miliseconds .
# start_ts is an optional parameter. There are two scenarios:
#   1.In case its is not used, the response from the api call that collect general data
#     from devices or location already includes the last connection date and this parameter will be used as start of the data range
#     to collect
#
#   2.In case used, the start_ts parameter will be used the first time the docker container is initiated and the database is created.
#     In the next iterations, the start date will be taken from the database table : 
#       2.1: The maximum date from all devices is taken, resulting in an array of dates, one date per device
#       2.2: The minimum date value from the array wil be considered as the start date

start_ts =          '' # 1717568329000
end_ts =            '' # 1717568329000

number =            '4000'

# If device_id variable is empty ([]), the API won't make API calls regarding devices
device_id =         [  ] # ['123456789', '567894231']

# If location_id variable is empty ([]), the API won't make API calls regarding locations
location_id =       [  ] # []

#######################
#
# API CALL FREQUENCY
#   
#######################
#
#   It is only necessary to modify the 'minutes' variable
#
#   In this example, the device connects and send data from the last hour in an hourly basis
#       ==> 1 hour * 60 minutes * 60 seconds * 1000 miliseconds
#
#   In case the minutes variable is modified, the data range of taken data will vary
#   i.e if I take data eack 30 minutes, the API will take data from the last 30 minutes

minutes = 1

def apiCallFrequencyMs():
    return  minutes * 60 * 1000

def apiCallFrequencySec():
    return  minutes * 60

def dayInMs():
    return 24 * 60 * 60 * 1000

def hourInMs():
    return 1 * 60 * 60 * 1000

def currentTimeInMs():
    return (datetime.datetime.now().timestamp()) * 1000
