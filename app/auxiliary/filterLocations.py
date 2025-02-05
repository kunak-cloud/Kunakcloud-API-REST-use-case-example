import numpy as np
import variables

def filter(location_list):
    #   We define an empty array, which we want to fill with filtered locations
    locations_to_filter = []
    #   For each location that was obtained with the 'List all locations' API call...
    for location_from_fetched_list in location_list:
        #   For each location that we specified in 'app/variables.py' > 'location_id' variable...
        for requested_location_serial_number in variables.location_id:
            #   Initializing variable 'match' as false. This variable allow to use it as filter, between true and false values
            match = False
            #   If the location from the API call is the same as the one that we specified in 'app/variables.py' > 'location_id' variable, there is a match
            if str(location_from_fetched_list['location_id']) == str(requested_location_serial_number):
                match = True
                break
        #   Append True or False to the locations_to_filter array
        if match == True:
            locations_to_filter.append(True)
        else:
            locations_to_filter.append(False)
    
    #   Formatting to work with the array
    filter = np.array(locations_to_filter)

    #   The return value is a location list, filtered with the values that are True only - https://www.w3schools.com/python/numpy/numpy_array_filter.asp
    #   For example:
    #
    #       location_list from my account   [ '123', '456', '678', '12345', '67890' ]
    #       variables.location_id:          [ '123', '678', '67890'  ]
    #       filter:                         [ True, False, True, False, True ]
    #       return value:                   [ '123', '678', '67890' ]

    return location_list[filter]
