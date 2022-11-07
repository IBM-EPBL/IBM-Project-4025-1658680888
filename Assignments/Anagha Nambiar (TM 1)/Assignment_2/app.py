from flask import Flask, render_template,request
import ibm_db

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=815fa4db-dc03-4c70-869a-a9cc13f33084.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=30367;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=znn62798;PWD=0eDwDTT9OIo2mTLG",'','')


app = Flask(__name__)
 

@app.route('/')
def signup():
    return render_template('signup.html')

@app.route('/about')
def about():
    return  render_template('about.html')

@app.route('/signin')
def signin():
    return  render_template('signin.html')

@app.route('/insert',methods = ['POST', 'GET'])
def insert():
    if request.method == 'POST':
        username = request.form['uname']
        rollno = request.form['rollno']
        email = request.form['email']
        pswd = request.form['pswd']

        sql = "SELECT * FROM students WHERE username =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)

        if account:
            return render_template('signin.html')
        else:
            insert_sql = "INSERT INTO students VALUES (?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, rollno)
            ibm_db.bind_param(prep_stmt, 2, username)
            ibm_db.bind_param(prep_stmt, 3, email)
            ibm_db.bind_param(prep_stmt, 4, pswd)
            ibm_db.execute(prep_stmt)
    
            return render_template('about.html')

   
 

if __name__ == '__main__':
    app.run()