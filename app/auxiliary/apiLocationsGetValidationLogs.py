import variables
import apiCallMethods
import json
from auxiliary import DbReplaceLocationData, apiLogin

# This API call will give us the list of changes that were done to the data from specific devices that have to be defined in variables.py
# The result from the API will be an object array. Each object has the following information:
#   - Location id from one location
#   - sensor_tag: Which sensor validation flag was modified
#   - action: Was the data Validated(V), was it invalidated(I) etc.?
#   - action_ts: When was this change applied to the data?
#   - range: Period in which the data validation flag is modified (indicated by start_ts and end_ts)
#   - reason: Explain why the data was invalidated

def extract( lastConnectionTime, apiCalls ):
    response = apiLogin.session.post(apiCallMethods.url_prefix + apiCallMethods.read_location_validation_log(),    
    data = json.dumps({
        "locations": variables.location_id,
        "startTs":(max(lastConnectionTime.values()) - variables.dayInMs()) ,
        "endTs": lastConnectionTime
    }))
    log_list = response.json()

    DbReplaceLocationData.replace(log_list)
    apiCalls += 1
    return apiCalls
