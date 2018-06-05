import psycopg2
from flask import Flask

app = Flask(__name__)

class DatabaseManager:
    def __init__(self):
        try:
            self.conn=psycopg2.connect("dbname='maintenance_tracker_sql' user='postgres' host='localhost' password='1234567890'")
            self.conn.autocommit =True
            self.cursor = self.conn.cursor()

            print("you have done it big man!")
        except:
            print ("I am unable to connect to the database.")

    def create_table(self):
        creata_table_command = "CREATE TABLE IF NOT EXISTS users(id serial PRIMARY KEY, email varchar(100) NOT NULL, password varchar(100) NOT NULL)"
        self.cursor.execute(creata_table_command)

    def insert_new_record(self, email, password):        
        sql = "INSERT INTO users (email, password) VALUES (%s, %s);"
        self.cursor.execute(sql, (email, password,))

    def query_all(self):
        sql = "SELECT * FROM Users"
        self.cursor.execute(sql)
        return{'message':'succeful!'}
        # row=self.cursor.execute(sql)
        # for item in row:

class RequestsManager(DatabaseManager):
    def __init__(self):
        DatabaseManager.__init__(self)
    
    def create_table(self):
        creata_table_command = "CREATE TABLE IF NOT EXISTS requests(id serial PRIMARY KEY, item varchar(100) NOT NULL, issue varchar(100) NOT NULL, issue_details varchar(500) NOT NULL, status varchar(100))"
        self.cursor.execute(creata_table_command)

    def insert_new_record(self, item, issue, issue_details, status):        
        sql = "INSERT INTO requests (item, issue, issue_details, status) VALUES (%s, %s, %s, %s);"
        self.cursor.execute(sql, (item, issue, issue_details, status,))

            
if __name__ == '__main__':
    datab = RequestsManager()

    datab.create_table()
    app.run(debug = True)    


    