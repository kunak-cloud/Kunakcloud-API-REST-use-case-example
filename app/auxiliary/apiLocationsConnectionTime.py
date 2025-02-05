import variables
import apiCallMethods
import numpy as np
from auxiliary import apiLogin

#  HTTP get call: List all locations
def extract():
    #    In the HTTP request, we send our credentials (session) and the user name
    response = apiLogin.session.get(apiCallMethods.url_prefix + apiCallMethods.list_all_locations(variables.user))
    print('Api call - List all locations -')
    output = np.array(response.json())

    #   The output is a list of locations and the devices from each location that contain the following:
    #               ·   Location ID
    #               ·   Serial number from device
    #               ·   Tag from device
    #               ·   Status from device
    #               ·   Last connection from device
    #               ·   Latitude from device
    #               ·   Longitude from device
    return  output
