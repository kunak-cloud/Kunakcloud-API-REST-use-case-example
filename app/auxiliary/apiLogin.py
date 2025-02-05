import requests
import variables

#   We use the 'requests' package from Python in order to make HTTP requests. 
#   For back ends that request to upload credentials, this package has the option to create 'sessions'
#       and store credentials.

user_id = variables.user
password = variables.password
session = requests.Session()
session.auth = ( user_id, password )
