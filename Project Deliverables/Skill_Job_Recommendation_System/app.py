from flask import Flask,render_template
import ibm_db

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=b1bc1829-6f45-4cd4-bef4-10cf081900bf.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32304;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=khc44923;PWD=VMdkxmMxV1Z30kOH",'','')


app = Flask(__name__)

@app.route('/register')
def register():
    return render_template('Registeration.html')

@app.route('/insert', methods = ['POST', 'GET'])
def insert():
    return