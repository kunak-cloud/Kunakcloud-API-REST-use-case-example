import psycopg2

#   psycopg2 is a Python package that let us connect to databases and interact with them - https://pypi.org/project/psycopg2/
#   In this case, we connect to the database 'example' with our credentials:
#       -   user:       'postgres'
#       -   password:   the one that is specified in 'db/password.txt'
#   The program connect to the "localhost" from the docker --> 'host.docker.internal'
#   The port in which our docker allocate the postgres database is in port 5433. If you make a project from scratch and not downloading this project,
#   the port value might change, depending how the port from the docker is configured.
#
conn = psycopg2.connect(database='example',
                            user='postgres',
                            password= open('db/password.txt', 'r').read(),
                            host='host.docker.internal',
                            port='5433')
cursor = conn.cursor()
conn.autocommit = True
