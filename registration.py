import mysql.connector

conn=mysql.connector.connect(host='localhost',username='root',password='Muskan@333',database='wanderwise')

my_cursor=conn.cursor()

conn.commit()
conn.close()

print("Connection succesfully created...")