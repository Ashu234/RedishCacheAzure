from flask import Flask, render_template, request, redirect, url_for, session
from azure.storage.blob import BlockBlobService
from azure.storage.blob import PublicAccess
from azure.storage.blob import ContentSettings
import mysql.connector
from mysql.connector import errorcode
import os
import csv
import datetime

app = Flask(__name__)

config = {
  'host':'myserver-mysql-ashu.mysql.database.azure.com',
  'user':'root123@myserver-mysql-ashu',
  'password':'Superman123',
  'database':'mysqlashudb',
  'ssl_ca':'BaltimoreCyberTrustRoot.crt.pem'
}

#block_blob_service = BlockBlobService(account_name='ashuazurestorage', account_key='HGvsHgPPFOp64gztvR6B9g+RNUUqzwhl+aNid8wpwca1uwejBMEhyVkP3oev1SKEnI5eeq4EIXWfcvzWjxAjuQ==')
#block_blob_service.set_container_acl('ashu-blob-container', public_access=PublicAccess.Container)

@app.route('/')
def index():
  return redirect(url_for('login'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['logged_in'] = True
        session['username'] = username
        time_start = datetime.datetime.now()
        session['time'] = time_start
        return redirect(url_for('dashboard'))
    return render_template('login.html')  

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
  
@app.route('/createDB')
def createDB():
  fileread = open('all_month.csv','rb')
  file_reader = csv.reader(fileread)
  try:
           conn = mysql.connector.connect(**config)
           print("Connection established")
  except mysql.connector.Error as err:
          if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
          elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
          else:
            print(err)
  else:
          cursor = conn.cursor()
          cursor.execute("DROP TABLE IF EXISTS earthquake_table;")
          cursor.execute("CREATE TABLE earthquake_table(time INT(11), latitude DECIMAL(10,10), longitude DECIMAL(10,10), depth DECIMAL(5,2), mag DECIMAL(5,2), magType VARCHAR(10), nst INT, gap DECIMAL(5,4), dmin DECIMAL(10,10), rms DECIMAL(7,7), net VARCHAR(10), id VARCHAR(25), updated INT(11), place VARCHAR(50), type VARCHAR(15), horizontalError DECIMAL(5,5), depthError DECIMAL(5,5), magError DECIMAL(5,5), magNst INT, status VARCHAR(15), locationSource VARCHAR(10), magSource VARCHAR(10));")
          conn.commit()
          cursor.close()
          conn.close()
  return render_template('complete.html')

  
if __name__ == '__main__':
    app.run(debug=True)
app.secret_key = 'secretkey'
