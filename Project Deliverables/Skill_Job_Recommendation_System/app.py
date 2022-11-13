from flask import Flask,render_template,request,redirect,url_for
import ibm_db
import flask_MailboxValidator



conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=b1bc1829-6f45-4cd4-bef4-10cf081900bf.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32304;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=khc44923;PWD=VMdkxmMxV1Z30kOH",'','')


app = Flask(__name__)



global e

@app.route('/sign-up',methods = ['POST','GET'])
def signup():
    if request.method == 'POST':
        e['email'] = request.form['email']
        e['mobno'] = request.form['mobile number']
        e['username'] = request.form['username']
        
        a = verify_mail()
        if a == True:
            return render_template('Resume.html')
        else:
            return redirect(url_for('signup.html', message=a))

    elif request.method == 'GET':
        return render_template('signup.html')

def verify_mail():
    mbv = flask_MailboxValidator.EmailValidation('H4F1G609ZLDB1JVNTIT9')
    results = mbv.validate_email(e['email'])
    if results['status'] == True:
        return True
    else:
        return results['error_message']

@app.route('/login')
def login():
    return render_template('login.html')



@app.route('/register')
def register():
    return render_template('Registeration.html')

@app.route('/insert', methods = ['POST', 'GET'])
def insert():
    return

