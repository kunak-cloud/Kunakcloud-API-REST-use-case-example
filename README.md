# Kunakcloud-API-REST-use-case-example

### Kunak API rest manual reference:
https://kunakair.com/doc/08.Manuals/html/Kunak_APIRest_UserManual_EN.html

### Considerations before starting
First, the Kunak device take samples from the sensors (normally, each 5 minutes) and the data is being stored in the internal memory from the device.

The Kunak devices connect to Kunak Cloud each sending period (normally, each hour). Once the device connect to the server, it send all the data that has collected during that period, then the last data is available to extract by using the API. This tool will enable to extract data from Kunak devices and locations.
This program will create in your computer a docker environment with a python container and a postgres database container:
+   The python program will do the following in order:
    -   The API will send the list of devices that belong to your account. The program will use the response to check the following:
        -   The device is available and 
        -   The device connected to Kunak Cloud and sent new data (if yes, make an API request for this device, otherwise, no)
    -   The program, in case knows that the device connected to Kunak Cloud and sent new data, it will make an API call for requesting the parameters we
        would like to extract.
    -   Each time data is requested for locations and devices, a cumulative value (in miliseconds) will increase according to the API call frequency that has
        been configured.
        In case that cumulative value is above one day (in miliseconds), a validation log API call will be performed in order to verify if the data flags have been changed

### How to run the docker
Requirements:
-   Install WSL 2 and download docker desktop as indicated in the docker manuals: https://docs.docker.com/desktop/features/wsl/
-   Login into docker via:
    -   Console line ('docker login -u <username>')
    -   Docker desktop

Before starting the docker, go to the following files:

    - 'app' folder > 'variables.py' file : Edit the username, password, devices and parameter measures to collect.
    - 'app' folder > 'db' folder > 'password.txt' file : In case you would like, edit the password

In order to create a container and run it, in the console, run:

    docker compose up --build

If you close the containter, you can start it with the previous line of code

or 

In Docker Desktop, go to 'Container section' and click the Play icon to run the containter

### How to connect to Postgres Database:
Recommended tools:
-If VScode is used, we recommend to install 'PostgreSQL Explorer' extension in order to access to the databases
-DBeaber

Data to enter when adding a new connection:
-host: 'localhost'
-port: 5433
-user: 'postgres'
-password: 'postgres' by default. In case you would like to modify it, follow the instructions:
    - Go to  'db' > 'password.txt'
    - Inside this file, edit the password

### Do I need to download the python libraries? ###
No. Docker read the file 'requirements.txt' and the container does the job of importing the libraries

### Data protection ###
Under 'variables.py' and 'password.txt' files, we can find sensitive data (password, username, etc.). In case you make the files public, it is recommended to leave the user, passwords, credentials, serial numbers and sensors empty

### How to remove the Postgres Database:
In Docker Desktop:
1. Go to the container list and remove the container
2. Go to the volume section and remove the volume
