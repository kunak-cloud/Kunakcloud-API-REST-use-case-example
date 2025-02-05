import variables
import apiCallMethods
import numpy as np
from auxiliary import apiLogin

#  HTTP get call: List all devices
def extract():
    #    In the HTTP request, we send our credentials (session) and the user name
    response = apiLogin.session.get(apiCallMethods.url_prefix + apiCallMethods.list_all_devices(variables.user))
    print('Api call - List all devices -')
    output = np.array(response.json())

    #   The output is a list of devices that contain the following:
    #               ·   Serial number
    #               ·   Tag
    #               ·   Status
    #               ·   Last connection
    #               ·   Latitude
    #               ·   Longitude
    return output
