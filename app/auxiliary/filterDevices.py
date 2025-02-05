import numpy as np
import variables

def filter(device_list):
    #   We define an empty array, which we want to fill with filtered devices
    devices_to_filter = []
    #   For each device that was obtained with the 'List all devices' API call...
    for device_from_fetched_list in device_list:
        #   For each device that we specified in 'app/variables.py' > 'device_id' variable...
        for requested_device_serial_number in variables.device_id:
            #   Initializing variable 'match' as false. This variable allow to use it as filter, between true and false values
            match = False
            #   If the device from the API call is the same as the one that we specified in 'app/variables.py' > 'device_id' variable, there is a match
            if device_from_fetched_list['serial_number'] == requested_device_serial_number:
                match = True
                break

        #   Append True or False to the devices_to_filter array
        if match == True:
            devices_to_filter.append(True)
        else:
            devices_to_filter.append(False)
    
    #   Formatting to work with the array
    filter = np.array(devices_to_filter)

    #   The return value is a device list, filtered with the values that are True only - https://www.w3schools.com/python/numpy/numpy_array_filter.asp
    #   For example:
    #
    #       device_list from my account:    [ '123', '456', '678' ]
    #       variables.device_id:            [ '123', '678' ]
    #       filter:                         [ True, False, True ]
    #       return value:                   [ '123', '678' ]

    return device_list[filter]
