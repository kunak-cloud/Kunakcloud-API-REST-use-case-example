import fetch
import time
import variables

#   The main python program (app.py) run continuously
#   Each frequency the api call is requested (in this example, each hour), the python program will run the program 'fetch.py'
while True:
    fetch.getData()
    time.sleep(variables.apiCallFrequencySec())
