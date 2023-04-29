import mysql.connector

# Establish connection with database
db_host = "ipfs-server.mysql.database.azure.com"
db_user = "mrprcsuoxp"
db_pass = "pass@cs6675db"
db_name = "ipfs-db"
conn = mysql.connector.connect(host=db_host, user=db_user, password=db_pass, database=db_name)


# Fetch all rows from database
sql="SELECT * FROM keywords"
cursor = conn.cursor()
cursor.execute(sql)
results = cursor.fetchall()
print(results)

# Close connection database
cursor.close()
conn.close()
