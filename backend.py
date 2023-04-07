#!/usr/bin/env python
import cgi
import cgitb
import mysql.connector

# Enable debug mode to display errors in the browser
cgitb.enable()

# Connect to the database
db_host = "localhost"
db_user = "username"
db_pass = "password"
db_name = "database_name"
conn = mysql.connector.connect(host=db_host, user=db_user, password=db_pass, database=db_name)

# Get the search query from the form
form = cgi.FieldStorage()
search = form.getvalue('search')

# Query the database
sql = "SELECT * FROM table_name WHERE column_name LIKE '%{}%'".format(search)
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
