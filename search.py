'#!/usr/bin/env python3'
import cgi
import cgitb
import mysql.connector

# Enable debug mode to display errors in the browser
cgitb.enable()
from flask import Flask, request, render_template
#from search import search_logic

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    # Get user input from form
    query = request.form['query']
    print('query: ',query)
    print("type: ",type(query))
    # Call search logic from search.py
    results = search_logic(query)

    # Return search results
    return render_template('results.html', results=results)

def search_logic(query):
    db_host = "ipfs-server.mysql.database.azure.com"
    db_user = "mrprcsuoxp"
    db_pass = "pass@cs6675db"
    db_name = "ipfs-db"
    conn = mysql.connector.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
    #sql="SELECT * FROM keywords WHERE keyword LIKE apple"
    inputs=query.split(" ")
    results=[]
    for input in inputs:
        sql="SELECT * FROM keywords WHERE keyword LIKE '%{}%'".format(input)
        cursor = conn.cursor()
        cursor.execute(sql)
        cur_res=set([item[2] for item in cursor.fetchall()])
        results.append(cur_res)
        # print("restype: ",type(results))
    cursor.close()
    conn.close()
    print(*results)
    return set.intersection(*results)
if __name__ == '__main__':
    app.run(debug=True)

# Connect to the database




