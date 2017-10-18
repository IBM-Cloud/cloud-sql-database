# (C) 2017 IBM
# Author: Henrik Loeser
#
# Very short sample app used with Db2 Warehouse on Cloud to demonstrate
# how to use a SQL Cloud Database with a web app.
#

import os
from flask import Flask,redirect,render_template,request
import urllib
import datetime
import json
import ibm_db

app = Flask(__name__)

# get service information if on IBM Cloud Platform
if 'VCAP_SERVICES' in os.environ:
    db2info = json.loads(os.environ['VCAP_SERVICES'])['dashDB'][0]
    db2cred = db2info["credentials"]
    appenv = json.loads(os.environ['VCAP_APPLICATION'])
else:
    raise ValueError('Expected cloud environment')

# connect to DB2
db2conn = ibm_db.connect("DATABASE="+db2cred['db']+";HOSTNAME="+db2cred['hostname']+";PORT="+str(db2cred['port'])+";UID="+db2cred['username']+";PWD="+db2cred['password']+";","","")

def city(name=None):
    if db2conn:
        # we have a Db2 connection, query the database
        sql="select * from cities2 where name=? order by population desc"
        # Note that for security reasons we are preparing the statement first,
        # then bind the form input as value to the statement to replace the
        # parameter marker.
        stmt = ibm_db.prepare(db2conn,sql)
        ibm_db.bind_param(stmt, 1, name)
        ibm_db.execute(stmt)
        rows=[]
        # fetch the result
        result = ibm_db.fetch_assoc(stmt)
        while result != False:
            rows.append(result.copy())
            result = ibm_db.fetch_assoc(stmt)
    return render_template('city.html', ci=rows)

# main page to dump some environment information
@app.route('/')
def index():
   return render_template('index.html', app=appenv)

# for testing purposes - use name in URI
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/search', methods=['GET'])
def searchroute():
    name = request.args.get('name', '')
    return city(name)

@app.route('/city/<name>')
def cityroute(name=None):
    return city(name)

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
