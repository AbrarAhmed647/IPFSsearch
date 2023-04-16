#!/usr/bin/env python
import cgi
import cgitb
import mysql.connector

# Enable debug mode to display errors in the browser
cgitb.enable()
#
# Connect to the database
db_host = "ipfs-server.mysql.database.azure.com"
db_user = "mrprcsuoxp"
db_pass = "pass@cs6675db"
db_name = "ipfs-db"
conn = mysql.connector.connect(user=db_user, password=db_pass, host=db_host, database=db_name, ssl_ca="DigiCertGlobalRootCA.crt.pem", ssl_disabled=False)

# Get the search query from the form
form = cgi.FieldStorage()
search = form.getvalue('search')

# Query the database
#sql = "SELECT * FROM keywords WHERE keyword LIKE '%{}%'".format(search)
sql="SELECT * FROM keywords"
cursor = conn.cursor()
cursor.execute(sql)
results = cursor.fetchall()

# Print the results as an HTML table
print("Content-Type: text/html")
print()
print("<!DOCTYPE html>")
print("<html>")
print("<head>")
print("<title>Search Results</title>")
print("</head>")
print("<body>")
print("<h1>Search Results</h1>")
if results:
    print("<table>")
    for row in results:
        print("<tr>")
        for col in row:
            print("<td>{}</td>".format(col))
        print("</tr>")
    print("</table>")
else:
    print("<p>No results found.</p>")
print("</body>")
print("</html>")

# Close the database connection
cursor.close()
conn.close()
