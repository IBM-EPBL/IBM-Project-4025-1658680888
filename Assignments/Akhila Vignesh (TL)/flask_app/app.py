from flask import Flask, render_template, request
import ibm_db

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=3883e7e4-18f5-4afe-be8c-fa31c41761d2.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31498;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=wnd97037;PWD=WWsiwUsyj0R9WNt8",'','')
app=Flask(__name__)


@app.route('/')
def home():
    return render_template("signup.html")

@app.route('/home')
def index():
    return render_template('home.html')


@app.route('/signup')
def register():
    roll_no=request.form['roll_no']
    name=request.form["name"]
    email=request.form["email"]
    pwd=request.form["pwd"]
    stmt=ibm_db.prepare(conn,"Insert into User values(?,?,?,?)")
    ibm_db.bind_param(stmt,1,roll_no)
    ibm_db.bind_param(stmt,2,name)
    ibm_db.bind_param(stmt,3,email)
    ibm_db.bind_param(stmt,4,pwd)
    ibm_db.execute(stmt)
    return render_template("login.html")
@app.route('/signin')
def login():
    roll_no=request.form['roll_no']
    pwd=request.form["pwd"]
    stmt=ibm_db.prepare(conn,"select * from Users id=? and pwd=?")
    ibm_db.bind_param(stmt,1,id)
    ibm_db.bind_param(stmt,2,pwd)
    flag=ibm_db.fetch_assoc(stmt)
    if flag:
        return render_template("home.html")
    else :
        return "Invalid id or password"





if __name__=="__main__":
    app.run(debug=True)