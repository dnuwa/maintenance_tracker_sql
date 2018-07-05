import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask


app = Flask(__name__)


class DatabaseManager:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                "dbname='maintenance_tracker_sql' user='postgres' host='localhost' password='1234567890'")
            self.conn.autocommit = True
            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)

            print("Database connected!")
        except:
            print("I am unable to connect to the database.")

    def create_table(self):
        creata_table_command = "CREATE TABLE IF NOT EXISTS users(id serial PRIMARY KEY, email varchar(100) NOT NULL, password varchar(100) NOT NULL)"
        self.cursor.execute(creata_table_command)

    def insert_new_record(self, email, password):
        sql = "INSERT INTO users (email, password) VALUES (%s, %s);"
        self.cursor.execute(sql, (email, password,))

    def query_all(self):
        sql = "SELECT * FROM users;"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows

    def login(self, stored_email, stored_password):
                       
        sql = "SELECT * FROM users WHERE email=%s AND password=%s" #, (stored_email, stored_password)
        vars = stored_email, stored_password
        self.cursor.execute(sql, vars)
        rows = self.cursor.fetchone()
        #print(rows)
        return rows
                
class RequestsManager(DatabaseManager):
    def __init__(self):
        DatabaseManager.__init__(self)

    def create_table(self):
        creata_table_command = "CREATE TABLE IF NOT EXISTS requests(id serial PRIMARY KEY, item varchar(100) NOT NULL, issue varchar(100) NOT NULL, issue_details varchar(500) NOT NULL, mode varchar(100), standing varchar(100))"
        self.cursor.execute(creata_table_command)

    def insert_new_record(self, item, issue, issue_details, mode):
        sql = "INSERT INTO requests (item, issue, issue_details, mode) VALUES (%s, %s, %s, %s);"
        self.cursor.execute(sql, (item, issue, issue_details, mode,))

    def query_all(self):
        sql = "SELECT * FROM requests;"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        # print (rows)
        return rows
        # for dics in rows:
        #     print (dics)      


    def query_by_id(self, id):
        self.cursor.execute(
            "SELECT * FROM requests WHERE id=%s;", [id])
        row = self.cursor.fetchone()
        return row


    def edit_a_record(self, id , item, issue, issue_details, mode, standing):        
        sql="UPDATE requests SET item=%s, issue=%s, issue_details=%s, mode=%s, standing=%s WHERE id =%s"
        self.cursor.execute(sql, (item, issue, issue_details, mode ,standing, id))

    def reject_or_approve(self, id, mode):
        sql="UPDATE requests SET mode=%s WHERE id = %s"           
        self.cursor.execute(sql, (mode, id))

    def resolve(self, id, standing):
        sql="UPDATE requests SET standing=%s WHERE id=%s"
        self.cursor.execute(sql, (standing, id))

    def update_pending_request(self, id, standing):
        query ="UPDATE requests SET  mode=%s, standing=%s WHERE id =%s"
        self.cursor.execute(query, ( standing, id))
    


if __name__ == '__main__':
    datab = RequestsManager()
    datab.query_all()

    # user = DatabaseManager()
    # user.login('barnabus.k@gmail.com', '1234')
    
    app.run(debug=True)
