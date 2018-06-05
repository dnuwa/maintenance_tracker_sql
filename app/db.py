import psycopg2

class DatabaseConnect:
    def __init__(self):
        try:
            self.conn=psycopg2.connect("dbname='maintenance_tracker_sql' user='postgres' host='localhost' password='1234567890'")
            self.conn.autocommit =True
            self.cursor = self.conn.cursor()

            print("you have done it big man!")
        except:
            print ("I am unable to connect to the database.")

