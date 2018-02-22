from flask import Flask, render_template, request, redirect, url_for, session
from azure.storage.blob import BlockBlobService
from azure.storage.blob import PublicAccess
from azure.storage.blob import ContentSettings
import mysql.connector
from mysql.connector import errorcode
import os
import csv

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
        return redirect(url_for('dashboard'))
    return render_template('login.html')  

@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    if request.method == 'POST':
        return render_template('dashboard')
    return render_template('dashboard.html')   

if __name__ == '__main__':
    app.run(debug=True)
app.secret_key = 'secretkey'
