url_prefix = 'https://kunakcloud.com/openAPIv0/v1/rest'

#    API call methods that were used for this program
#
##########################################################
#
#    API calls for devices
#

def list_all_devices (user_id):
     return'/devices/list/{}?filter=all'.format( user_id )

def read_from_to_single_device(device_id):
     return '/devices/{}/reads/fromTo'.format( device_id )

def read_devices_validation_log():
     return '/devices/validationLog/fromTo'

def read_from_to_multiple_devices_group_by_ts():
     return '/devices/reads/fromToGroupByTs'


##########################################################
#
#    API calls for locations
#

def list_all_locations (user_id):
     return'/locations/list/{}'.format( user_id )

def read_from_to_single_location(location_id):
     return '/locations/{}/reads/fromTo'.format( location_id )

def read_location_validation_log():
     return '/locations/validationLog/until'

