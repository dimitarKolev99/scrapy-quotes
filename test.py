import psycopg2
from psycopg2 import Error

try:
    connection = psycopg2.connect(
        user='ukggwjdb',
        password='ynLyFB9yx_3CyG-mJ7iwDIJGzrrb8Kn6',
        host='ruby.db.elephantsql.com',
        port='',
        database='ukggwjdb'
    )

    cursor = connection.cursor()

    print("PosrgreSQL server information")
    print(connection.get_dsn_parameters(), "\n")
   
    var = 3
    s = "sffg ${var}"
    
    cursor.execute("SELECT version();")

    record = cursor.fetchone()

    print("You are connected to - ", record, "\n")

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if (connection):
        cursor.close()

        connection.close()
        print("PostgreSQL connection is closed")