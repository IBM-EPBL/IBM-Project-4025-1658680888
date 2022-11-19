import hashlib
from flask import Flask,render_template,request,session
import ibm_db,random,base64

from markupsafe import escape
import MailboxValidator

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def db_conn():
    try:
        conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=b1bc1829-6f45-4cd4-bef4-10cf081900bf.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32304;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=khc44923;PWD=VMdkxmMxV1Z30kOH",'','')
    except:     
        print(ibm_db.conn_errormsg())
    else:
        return conn

conn = db_conn()
app = Flask(__name__)
val = random.randint(100000, 999999)
app.secret_key = str(val) 


e = {}

@app.route('/sign-up',methods = ['POST','GET'])
def signup():
    if request.method == 'POST':
        e['email'] = request.form['email']
        e['mobile'] = str(request.form['mobile'])
        e['pswd'] = hashlib.md5(request.form['pswd'].encode()).hexdigest()

        sql =  "SELECT * FROM applicant WHERE email = ?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt, 1, e.get('email') )
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        
        if account:
            return render_template('signup.html', message = 'This email already has an account', active = 'signup')
        else:
            a = verify_mail()
            if a == "True":
                session['email'] = request.form['email']
                session.permanent = True
                skills = ['Software Development','JavaScript', 'SQL' ,'AngularJS', 'Software Development Life Cycle (SDLC)','Agile Methodologies', 'Java', 'Dalim', 'jQuery', '.NET Framework', 'Requirements Analysis', 'PL/SQL', 'XML', 'HTML', 'Web Services', 'Node.js', 'Microsoft SQL Server', 'Oracle Database', 'C#', 'Unix', 'HTML5',' Cascading Style Sheets (CSS)', 'Web Development' ,'ASP.NET MVC', 'Language Integrated Query (LINQ)', 'ASP.NET' ,'Microsoft', 'Azure', 'TypeScript', 'Git', 'ASP.NET', 'Web API', 'Spring Boot', 'MySQL' ,'C++', 'Core Java','Choose a Skill']
                return render_template('Resume.html', required = e['email'],skills=skills)
            elif a == "False":
                message = 'Error in email validation'
                return render_template('signup.html', message=message, active = 'signup' )
    
    elif request.method == 'GET':
        return render_template('signup.html', active = 'signup')



def verify_mail():
    mbv = MailboxValidator.EmailValidation("H4F1G609ZLDB1JVNTIT9")
    results = mbv.validate_email(e['email'])

    email_message = Mail(
    from_email='anagha.nambiar.2019.cse@rajalakshmi.edu.in',
    to_emails= e.get('email'),
    subject='Job UP Email Verification',
    html_content='<h3>Thankyou for signing up with JOB UP</h3><br><p>This email is sent to verify the applicant. You are a registered user now.<br> </p><h2>Job UP, All In One Stop For Job.</h2>')
    try:
        sg = SendGridAPIClient('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')
        response = sg.send(email_message)
        status = response.status_code
    except Exception as err:
        print(err.message)
        
    return results['status']




@app.route('/login',methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        pswd = hashlib.md5(request.form['pswd'].encode()).hexdigest()

        sql =  "SELECT * FROM applicant WHERE email = ? "
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt, 1, email )
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        
        if account:
            if pswd == account['PASSWORD']:
                session['email'] = email
                return render_template('dashboard.html',active = "home")
            else:
                return render_template ('login.html', message = "An account with this email id and password dosen't exist.", active = 'login')
        else:
            return render_template ('login.html', message = "An account with this email id and password dosen't exist.",active = 'login')

    elif request.method == 'GET':
        return render_template('login.html',active = 'login')


@app.route('/register',methods = ['POST'])
def register():
    
    if request.method == 'POST':

        file = request.files['photo']
        data = file.read()
        render_file = render_picture(data)


        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        dob = request.form['dob']
        gender = request.form['gender']

        c10 = {}
        c10['school'] = request.form['10school']
        c10['year'] = request.form ['10year']
        c10['marks'] = request.form['10marks']

        c12 = {}
        c12['school'] = request.form['12school']
        c12['year'] = request.form ['12year']
        c12['marks'] = request.form['12marks']

        d = {}
        d['course'] = request.form['dcourse']
        d['year'] = request.form ['dyear']
        d['marks'] = request.form['dmarks']

        ug = {}
        ug['clg'] = request.form['ugcollege']
        ug['year'] = request.form ['ugyear']
        ug['degree'] = request.form['ugdegree']
        ug['cgpa'] = request.form['ugcgpa']

        pg = {}
        pg['clg'] = request.form['pgcollege']
        pg['year'] = request.form ['pgyear']
        pg['degree'] = request.form['pgdegree']
        pg['cgpa'] = request.form['pgcgpa']

        skill = []
        for i in range(1,7):
            var = 'skill'+str(i)
            if request.form[var] != 'Choose a Skill':
                skill.append(request.form[var])
            else:
                skill.append("")

        proj = []
        for i in range(1,4):
            var = 'pj'+str(i)
            if request.form[var] != 'NA'.lower():
                proj.append(request.form[var])
            else:
                proj.append("")

        comp = []
        for i in range(1,4):
            var = 'company'+str(i)
            if request.form[var] != '':
                comp.append(request.form[var])
            else:
                comp.append("")


        sql =  "SELECT * FROM applicant WHERE email = ?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt, 1, e.get('email') )
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        
        if account:
            return render_template('login.html',active = 'login')

        else:

            insert_sql = "INSERT INTO applicant (f_name,l_name,dob,gender,email,photo,mobile,password) VALUES (?,?,?,?,?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, firstname )
            ibm_db.bind_param(prep_stmt, 2, lastname)
            ibm_db.bind_param(prep_stmt, 3, dob)
            ibm_db.bind_param(prep_stmt, 4, gender)
            ibm_db.bind_param(prep_stmt, 5, email)
            ibm_db.bind_param(prep_stmt, 6, render_file)
            ibm_db.bind_param(prep_stmt, 7, e.get('mobile'))
            ibm_db.bind_param(prep_stmt, 8, e.get('pswd'))
            ibm_db.execute(prep_stmt)

            sql =  "SELECT * FROM applicant WHERE email = ?"
            stmt = ibm_db.prepare(conn,sql)
            ibm_db.bind_param(stmt, 1, email )
            ibm_db.execute(stmt)
            account = ibm_db.fetch_assoc(stmt)

            if account:
                pid = account['PID']


                insert_sql = "INSERT INTO acd_10 VALUES (?,?,?,?)"
                prep_stmt = ibm_db.prepare(conn, insert_sql)
                ibm_db.bind_param(prep_stmt, 1, pid )
                ibm_db.bind_param(prep_stmt, 2, c10.get('school'))
                ibm_db.bind_param(prep_stmt, 3, c10.get('year'))    
                ibm_db.bind_param(prep_stmt, 4, c10.get('marks'))
                ibm_db.execute(prep_stmt)


                insert_sql = "INSERT INTO acd_12 VALUES (?,?,?,?)"
                prep_stmt = ibm_db.prepare(conn, insert_sql)
                ibm_db.bind_param(prep_stmt, 1, pid )
                ibm_db.bind_param(prep_stmt, 2, c12.get('school'))
                ibm_db.bind_param(prep_stmt, 3, c12.get('marks'))    
                ibm_db.bind_param(prep_stmt, 4, c12.get('year'))
                ibm_db.execute(prep_stmt)

                if d.get('course').lower() != 'NA'.lower():
                    insert_sql = "INSERT INTO acd_diploma VALUES (?,?,?,?)"
                    prep_stmt = ibm_db.prepare(conn, insert_sql)
                    ibm_db.bind_param(prep_stmt, 1, pid )
                    ibm_db.bind_param(prep_stmt, 2, d.get('course'))
                    ibm_db.bind_param(prep_stmt, 3, d.get('marks') )    
                    ibm_db.bind_param(prep_stmt, 4, d.get('year') )
                    ibm_db.execute(prep_stmt)

                if ug.get('clg').lower() != 'NA'.lower():
                    insert_sql = "INSERT INTO acd_ug VALUES (?,?,?,?,?)"
                    prep_stmt = ibm_db.prepare(conn, insert_sql)
                    ibm_db.bind_param(prep_stmt, 1, pid )
                    ibm_db.bind_param(prep_stmt, 2, ug.get('clg'))
                    ibm_db.bind_param(prep_stmt, 3, ug.get('cgpa'))
                    ibm_db.bind_param(prep_stmt, 4, ug.get('year'))    
                    ibm_db.bind_param(prep_stmt, 5, ug.get('degree'))
                    ibm_db.execute(prep_stmt)

                if pg.get('clg').lower() != 'NA'.lower():
                    insert_sql = "INSERT INTO acd_pg VALUES (?,?,?,?,?)"
                    prep_stmt = ibm_db.prepare(conn, insert_sql)
                    ibm_db.bind_param(prep_stmt, 1, pid )
                    ibm_db.bind_param(prep_stmt, 2, pg.get('clg'))
                    ibm_db.bind_param(prep_stmt, 3, pg.get('cgpa'))    
                    ibm_db.bind_param(prep_stmt, 4, pg.get('degree'))
                    ibm_db.bind_param(prep_stmt, 5, pg.get('year'))
                    ibm_db.execute(prep_stmt)

                if proj[0].lower() != 'NA'.lower():
                    insert_sql = "INSERT INTO project VALUES (?,?,?,?)"
                    prep_stmt = ibm_db.prepare(conn, insert_sql)
                    ibm_db.bind_param(prep_stmt, 1, pid )
                    ibm_db.bind_param(prep_stmt, 2, proj[0])
                    ibm_db.bind_param(prep_stmt, 3, proj[1])    
                    ibm_db.bind_param(prep_stmt, 4, proj[2])
                    ibm_db.execute(prep_stmt)

                if skill[0].lower() != 'NA'.lower():
                    insert_sql = "INSERT INTO skill VALUES (?,?,?,?,?,?,?)"
                    prep_stmt = ibm_db.prepare(conn, insert_sql)
                    ibm_db.bind_param(prep_stmt, 1, pid )
                    ibm_db.bind_param(prep_stmt, 2, skill[0])
                    ibm_db.bind_param(prep_stmt, 3, skill[1])    
                    ibm_db.bind_param(prep_stmt, 4, skill[2])
                    ibm_db.bind_param(prep_stmt, 5, skill[3])
                    ibm_db.bind_param(prep_stmt, 6, skill[4])    
                    ibm_db.bind_param(prep_stmt, 7, skill[5])
                    ibm_db.execute(prep_stmt)


                insert_sql = "INSERT INTO top3_comp VALUES (?,?,?,?)"
                prep_stmt = ibm_db.prepare(conn, insert_sql)
                ibm_db.bind_param(prep_stmt, 1, pid )
                ibm_db.bind_param(prep_stmt, 2, comp[0])
                ibm_db.bind_param(prep_stmt, 3, comp[1])    
                ibm_db.bind_param(prep_stmt, 4, comp[2])
                ibm_db.execute(prep_stmt)

                return render_template('dashboard.html',active = "home")
    elif request.method == 'GET':
        if session.get('email') == 'None':
                return render_template('signup.html',active = 'signup')
        else:
            skills = ['Software Development','JavaScript', 'SQL' ,'AngularJS', 'Software Development Life Cycle (SDLC)','Agile Methodologies', 'Java', 'Dalim', 'jQuery', '.NET Framework', 'Requirements Analysis', 'PL/SQL', 'XML', 'HTML', 'Web Services', 'Node.js', 'Microsoft SQL Server', 'Oracle Database', 'C#', 'Unix', 'HTML5',' Cascading Style Sheets (CSS)', 'Web Development' ,'ASP.NET MVC', 'Language Integrated Query (LINQ)', 'ASP.NET' ,'Microsoft', 'Azure', 'TypeScript', 'Git', 'ASP.NET', 'Web API', 'Spring Boot', 'MySQL' ,'C++', 'Core Java','Choose a Skill']
            return render_template('Resume.html', required = session.get('email') ,skills=skills)


def render_picture(data):
    render_pic = base64.b64encode(data).decode('ascii') 
    return render_pic


def getaccount(email):

    account = {}

    sql =  "SELECT * FROM applicant WHERE email = ?"
    stmt = ibm_db.prepare(conn,sql)
    ibm_db.bind_param(stmt, 1, email )
    ibm_db.execute(stmt)
    account1 = ibm_db.fetch_assoc(stmt)

    pid = account1['PID']

    account['per'] = account1
    
    sql =  "SELECT * FROM acd_10 WHERE pid = ?"
    stmt = ibm_db.prepare(conn,sql)
    ibm_db.bind_param(stmt, 1, pid)
    ibm_db.execute(stmt)
    account1 = ibm_db.fetch_assoc(stmt)
    account['10'] = account1

    sql =  "SELECT * FROM acd_12 WHERE pid = ?"
    stmt = ibm_db.prepare(conn,sql)
    ibm_db.bind_param(stmt, 1, pid)
    ibm_db.execute(stmt)
    account1 = ibm_db.fetch_assoc(stmt)
    account['12'] = account1

    sql =  "SELECT * FROM acd_diploma WHERE pid = ?"
    stmt = ibm_db.prepare(conn,sql)
    ibm_db.bind_param(stmt, 1, pid)
    ibm_db.execute(stmt)
    account1 = ibm_db.fetch_assoc(stmt)
    if account1 :
        account['dip']= account1
    else:
        account['dip']= ""

    sql =  "SELECT * FROM acd_ug WHERE pid = ?"
    stmt = ibm_db.prepare(conn,sql)
    ibm_db.bind_param(stmt, 1, pid)
    ibm_db.execute(stmt)
    account1 = ibm_db.fetch_assoc(stmt)
    if account1 :
        account['ug']= account1
    else:
        account['ug']= ""

    sql =  "SELECT * FROM acd_pg WHERE pid = ?"
    stmt = ibm_db.prepare(conn,sql)
    ibm_db.bind_param(stmt, 1, pid)
    ibm_db.execute(stmt)
    account1 = ibm_db.fetch_assoc(stmt)
    if account1 :
        account['pg']= account1
    else:
        account['pg']= ""

    sql =  "SELECT * FROM project WHERE pid = ?"
    stmt = ibm_db.prepare(conn,sql)
    ibm_db.bind_param(stmt, 1, pid)
    ibm_db.execute(stmt)
    account1 = ibm_db.fetch_assoc(stmt)
    account['p'] = account1

    sql =  "SELECT * FROM skill WHERE pid = ?"
    stmt = ibm_db.prepare(conn,sql)
    ibm_db.bind_param(stmt, 1, pid)
    ibm_db.execute(stmt)
    account1 = ibm_db.fetch_assoc(stmt)
    account['skill'] = account1

    sql =  "SELECT * FROM top3_comp WHERE pid = ?"
    stmt = ibm_db.prepare(conn,sql)
    ibm_db.bind_param(stmt, 1, pid)
    ibm_db.execute(stmt)
    account1 = ibm_db.fetch_assoc(stmt)
    account['comp'] = account1

    return account

@app.route('/view', methods = ['GET'])
def viewresume():
        account = getaccount(session.get('email'))
        if account:
            return render_template('View.html', account=account, active = "view", l = account)

@app.route('/edit',methods = ['POST','GET'])
def edit():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        dob = request.form['dob']
        

        c10 = {}
        c10['school'] = request.form['10school']
        c10['year'] = request.form ['10year']
        c10['marks'] = request.form['10marks']

        c12 = {}
        c12['school'] = request.form['12school']
        c12['year'] = request.form ['12year']
        c12['marks'] = request.form['12marks']

        d = {}
        d['course'] = request.form['dcourse']
        d['year'] = request.form ['dyear']
        d['marks'] = request.form['dmarks']

        ug = {}
        ug['clg'] = request.form['ugcollege']
        ug['year'] = request.form ['ugyear']
        ug['degree'] = request.form['ugdegree']
        ug['cgpa'] = request.form['ugcgpa']

        pg = {}
        pg['clg'] = request.form['pgcollege']
        pg['year'] = request.form ['pgyear']
        pg['degree'] = request.form['pgdegree']
        pg['cgpa'] = request.form['pgcgpa']

        skill = []
        for i in range(1,7):
            var = 'skill'+str(i)
            if request.form[var] != 'Choose a Skill':
                skill.append(request.form[var])
            else:
                skill.append("")

        proj = []
        for i in range(1,4):
            var = 'pj'+str(i)
            if request.form[var] != 'NA'.lower():
                proj.append(request.form[var])
            else:
                proj.append("")

        comp = []
        for i in range(1,4):
            var = 'company'+str(i)
            if request.form[var] != '':
                comp.append(request.form[var])
            else:
                comp.append("")


        sql =  "SELECT * FROM applicant WHERE email = ?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt, 1, session.get('email') )
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        
        if account:

            pid = account['PID']
            insert_sql = "UPDATE applicant SET f_name = ? ,l_name = ?,dob = ?  WHERE pid = ?"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, firstname )
            ibm_db.bind_param(prep_stmt, 2, lastname)
            ibm_db.bind_param(prep_stmt, 3, dob)
            ibm_db.bind_param(prep_stmt, 4, pid)
            ibm_db.exec_immediate(prep_stmt)



            insert_sql = "UPDATE acd_10 SET s_name=?, marks = ?, year=? WHERE pid = ?"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, c10.get('school'))
            ibm_db.bind_param(prep_stmt, 2, c10.get('year'))    
            ibm_db.bind_param(prep_stmt, 3, c10.get('marks'))
            ibm_db.bind_param(prep_stmt, 4, pid )
            ibm_db.exec_immediate(prep_stmt)

            insert_sql ="UPDATE acd_12 SET s_name=?, marks = ?, year=? WHERE pid = ?"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, c12.get('school'))
            ibm_db.bind_param(prep_stmt, 2, c12.get('marks'))    
            ibm_db.bind_param(prep_stmt, 3, c12.get('year'))
            ibm_db.bind_param(prep_stmt, 4, pid )
            ibm_db.exec_immediate(prep_stmt)

            if d.get('course').lower() != 'NA'.lower():
                insert_sql = "UPDATE acd_diploma SET course_name=?, marks = ?, year=? WHERE pid = ?"
                prep_stmt = ibm_db.prepare(conn, insert_sql)
                
                ibm_db.bind_param(prep_stmt, 1, d.get('course'))
                ibm_db.bind_param(prep_stmt, 2, d.get('marks') )    
                ibm_db.bind_param(prep_stmt, 3, d.get('year') )
                ibm_db.bind_param(prep_stmt, 4, pid )
                ibm_db.exec_immediate(prep_stmt)

            if ug.get('clg').lower() != 'NA'.lower():
                insert_sql = "UPDATE acd_ug SET c_name=?, cgpa = ?, year=?, degree=? WHERE pid = ?"
                prep_stmt = ibm_db.prepare(conn, insert_sql)
                
                ibm_db.bind_param(prep_stmt, 1, ug.get('clg'))
                ibm_db.bind_param(prep_stmt, 2, ug.get('cgpa'))
                ibm_db.bind_param(prep_stmt, 3, ug.get('year'))    
                ibm_db.bind_param(prep_stmt, 4, ug.get('degree'))
                ibm_db.bind_param(prep_stmt, 5, pid )
                ibm_db.exec_immediate(prep_stmt)

            if pg.get('clg').lower() != 'NA'.lower():
                insert_sql = "UPDATE acd_pg SET c_name=?, cgpa = ?, year=?, degree=? WHERE pid = ?"
                prep_stmt = ibm_db.prepare(conn, insert_sql)
                
                ibm_db.bind_param(prep_stmt, 1, pg.get('clg'))
                ibm_db.bind_param(prep_stmt, 2, pg.get('cgpa'))    
                ibm_db.bind_param(prep_stmt, 3, pg.get('degree'))
                ibm_db.bind_param(prep_stmt, 4, pg.get('year'))
                ibm_db.bind_param(prep_stmt, 5, pid )
                ibm_db.exec_immediate(prep_stmt)

            if proj[0].lower() != 'NA'.lower():
                insert_sql = "UPDATE project SET proj1=?, proj2 = ?, proj3=? WHERE pid = ?"
                prep_stmt = ibm_db.prepare(conn, insert_sql)
                
                ibm_db.bind_param(prep_stmt, 1, proj[0])
                ibm_db.bind_param(prep_stmt, 2, proj[1])    
                ibm_db.bind_param(prep_stmt, 3, proj[2])
                ibm_db.bind_param(prep_stmt, 4, pid )
                ibm_db.exec_immediate(prep_stmt)

            if skill[0].lower() != 'NA'.lower():
                insert_sql = "UPDATE skill SET skill1=?, skill2 = ?, skill3=?, skill4=?, skill5 = ?, skill6=? WHERE pid = ?"
                prep_stmt = ibm_db.prepare(conn, insert_sql)
                
                ibm_db.bind_param(prep_stmt, 1, skill[0])
                ibm_db.bind_param(prep_stmt, 2, skill[1])    
                ibm_db.bind_param(prep_stmt, 3, skill[2])
                ibm_db.bind_param(prep_stmt, 4, skill[3])
                ibm_db.bind_param(prep_stmt, 5, skill[4])    
                ibm_db.bind_param(prep_stmt, 6, skill[5])
                ibm_db.bind_param(prep_stmt, 7, pid )
                ibm_db.exec_immediate(prep_stmt)

            insert_sql = "UPDATE top3_comp SET comp1=?, comp2=?, comp3=? WHERE pid = ?"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
           
            ibm_db.bind_param(prep_stmt, 1, comp[0])
            ibm_db.bind_param(prep_stmt, 2, comp[1])    
            ibm_db.bind_param(prep_stmt, 3, comp[2])
            ibm_db.bind_param(prep_stmt, 4, pid )
            ibm_db.exec_immediate(prep_stmt)

        return render_template('dashboard.html', active = "home")

    elif request.method == 'GET':
        if session.get('email') == 'None':
            return render_template('signup.html')
        else:
            account = getaccount(session.get('email'))
            skills = ['Software Development','JavaScript', 'SQL' ,'AngularJS', 'Software Development Life Cycle (SDLC)','Agile Methodologies', 'Java', 'Dalim', 'jQuery', '.NET Framework', 'Requirements Analysis', 'PL/SQL', 'XML', 'HTML', 'Web Services', 'Node.js', 'Microsoft SQL Server', 'Oracle Database', 'C#', 'Unix', 'HTML5',' Cascading Style Sheets (CSS)', 'Web Development' ,'ASP.NET MVC', 'Language Integrated Query (LINQ)', 'ASP.NET' ,'Microsoft', 'Azure', 'TypeScript', 'Git', 'ASP.NET', 'Web API', 'Spring Boot', 'MySQL' ,'C++', 'Core Java','Choose a Skill']
            return render_template('Edit.html', account=account, skills=skills,active = "edit")
        
@app.route('/dashboard',methods = ['GET'])
def dashboard():
    return render_template('dashboard.html',active = "home")

@app.route('/search', methods=['GET'])
def search():
    return render_template('dashboard.html',active = "search")

@app.route('/logout',methods = ['GET'])
def logout():
    session.pop('email',None)
    return render_template('login.html', active = 'login')






