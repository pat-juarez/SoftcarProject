# Import libraries required for connecting to mysql

import mysql.connector

# Import libraries required for connecting to DB2 or PostgreSql

import psycopg2

# Connect to MySQL

connection = mysql.connector.connect(user='root', password='oSASHBsuhoCaGRWB6xuFKOLe',host='172.21.21.211',database='sales')

# create cursor

cursor = connection.cursor()

# Connect to DB2 or PostgreSql

dsn_hostname = '172.21.46.33'
dsn_user='postgres'        # e.g. "abc12345"
dsn_pwd ='dRuIZr0TFz5Ufk0mw1g19pdZ'      # e.g. "7dBZ3wWt9XN6$o0J"
dsn_port ="5432"                # e.g. "50000" 
dsn_database ="postgres"           # i.e. "BLUDB"

# create connection

conn = psycopg2.connect(
   database=dsn_database, 
   user=dsn_user,
   password=dsn_pwd,
   host=dsn_hostname, 
   port= dsn_port
)

#Crreate a cursor onject using cursor() method

cursor1 = conn.cursor()

# Find out the last rowid from DB2 data warehouse or PostgreSql data warehouse
# The function get_last_rowid must return the last rowid of the table sales_data on the IBM DB2 database or PostgreSql.

def get_last_rowid():
    SQL = """SELECT MAX(rowid) FROM sales_data;"""
    # Execute the SQL statement
    cursor1.execute(SQL)
    rows = cursor1.fetchall()
    return rows[-1][0]

last_row_id = get_last_rowid()
print("Last row id on production datawarehouse = ", last_row_id)

# List out all records in MySQL database with rowid greater than the one on the Data warehouse
# The function get_latest_records must return a list of all records that have a rowid greater than the last_row_id in the sales_data table in the sales database on the MySQL staging data warehouse.

def get_latest_records(rowid):
    SQL = f"SELECT * FROM sales_data WHERE rowid>={rowid};"
    # Execute the SQL statement
    cursor.execute(SQL)
    return cursor.fetchall()

new_records = get_latest_records(last_row_id)

print("New rows on staging datawarehouse = ", len(new_records))

# print(new_records[-1])

# Insert the additional records from MySQL into DB2 or PostgreSql data warehouse.
# The function insert_records must insert all the records passed to it into the sales_data table in IBM DB2 database or PostgreSql.

cursor1.execute("SELECT rowid FROM sales_data ORDER BY rowid DESC LIMIT 1;")
print(f"Last rowid before synch: {cursor1.fetchall()[-1][0]}")

def insert_records(records):
    for row in records:
        SQL = f"INSERT INTO  sales_data(rowid,product_id,customer_id,quantity) VALUES({row[0]},{row[1]},{row[2]},{row[3]});"
        # Execute the SQL statement
        cursor1.execute(SQL)

insert_records(new_records)
print("New rows inserted into production datawarehouse = ", len(new_records))

cursor1.execute("SELECT rowid FROM sales_data ORDER BY rowid DESC LIMIT 1;")
print(f"Last rowid after synch: {cursor1.fetchall()[-1][0]}")
# disconnect from mysql warehouse

# connection.close()

# disconnect from DB2 or PostgreSql data warehouse 

conn.close()

# End of program