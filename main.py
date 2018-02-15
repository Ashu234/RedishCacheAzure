from flask import Flask, render_template, request, redirect, url_for, session
from azure.storage.blob import BlockBlobService
from azure.storage.blob import PublicAccess
from azure.storage.blob import ContentSettings
import mysql.connector
from mysql.connector import errorcode
import os

app = Flask(__name__)

config = {
  'host':'myserver-mysql-ashu.mysql.database.azure.com',
  'user':'root123@myserver-mysql-ashu',
  'password':'Superman123',
  'database':'mysqlashudb',
  'ssl_ca':'BaltimoreCyberTrustRoot.crt.pem'
}

block_blob_service = BlockBlobService(account_name='ashuazurestorage', account_key='HGvsHgPPFOp64gztvR6B9g+RNUUqzwhl+aNid8wpwca1uwejBMEhyVkP3oev1SKEnI5eeq4EIXWfcvzWjxAjuQ==')
block_blob_service.set_container_acl('ashu-blob-container', public_access=PublicAccess.Container)

@app.route('/')
def index():
  return redirect(url_for('login'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        print(username)
        session['logged_in'] = True
        session['username'] = username
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
  return render_template('dashboard.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        username = session['username']
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
          for file in request.files.getlist("file"):
              file_to_upload = file.filename
              title = request.form['title']
              full_path_to_file = os.path.join(os.path.dirname(__file__), file_to_upload)
              block_blob_service.create_blob_from_path(
              'ashu-blob-container',
              title,
              full_path_to_file,
              content_settings=ContentSettings(content_type='image/png')
              )
              cursor.execute("INSERT INTO images (username, title) VALUES (%s, %s);", (username, title))
          conn.commit()
          cursor.close()
          conn.close()
        return render_template('complete.html')
    return render_template('upload.html')

@app.route('/rating/<string:title>/', methods=['POST','GET'])
def rating(title):
    if request.method == 'POST':
      rating = request.form['rating']
      return render_template('complete.html', rating=rating)
    return render_template('rating.html', title=title)


class MyBlob(object):
    url = ''
    size = 0
    title = ''
    date = ''

    def __init__(self, url, size, title, date):
        self.url = url
        self.size = (size/1024)
        self.title = title
        self.date = date


@app.route('/viewImages', methods=['GET', 'POST'])
def viewImages():
    blobs = []
    generators = block_blob_service.list_blobs('ashu-blob-container')
    for blob in generators:
        blob_url = block_blob_service.make_blob_url('ashu-blob-container', blob.name, protocol=None, sas_token=None)
        myBlob = MyBlob(blob_url,blob.properties.content_length,blob.name,blob.properties.last_modified)
        blobs.append(myBlob)
    return render_template('viewImages.html', blobs=blobs)

if __name__ == '__main__':
    app.run(debug=True)
app.secret_key = 'secretkey'
