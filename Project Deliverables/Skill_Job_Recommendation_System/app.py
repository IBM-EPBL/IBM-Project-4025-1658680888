from passlib.hash import sha256_crypt
from flask import Flask,render_template,request,session
import ibm_db,re,random,base64
import MailboxValidator



def db_conn():
    try:
        conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=b1bc1829-6f45-4cd4-bef4-10cf081900bf.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32304;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=khc44923;PWD=VMdkxmMxV1Z30kOH",'','')
    except:     
        return ibm_db.conn_errormsg()
    else:
        return conn

app = Flask(__name__)
val = random.randint(100000, 999999)
app.secret_key = str(val) 


e = {}

@app.route('/sign-up',methods = ['POST','GET'])
def signup():
    if request.method == 'POST':
        e['email'] = request.form['email']
        e['mobno'] = request.form['mobile']
        e['username'] = request.form['username']
        e['pswd'] = sha256_crypt.encrypt(request.form['pswd'])
        
        a = verify_mail()
        if a == "True":
            session['email'] = request.form['email']
            skills = ['Software Development','JavaScript', 'SQL' ,'AngularJS', 'Software Development Life Cycle (SDLC)','Agile Methodologies', 'Java', 'Dalim', 'jQuery', '.NET Framework', 'Requirements Analysis', 'PL/SQL', 'XML', 'HTML', 'Web Services', 'Node.js', 'Microsoft SQL Server', 'Oracle Database', 'C#', 'Unix', 'HTML5',' Cascading Style Sheets (CSS)', 'Web Development' ,'ASP.NET MVC', 'Language Integrated Query (LINQ)', 'ASP.NET' ,'Microsoft', 'Azure', 'TypeScript', 'Git', 'ASP.NET', 'Web API', 'Spring Boot', 'MySQL' ,'C++', 'Core Java','Choose a Skill']
            return render_template('Resume.html', required = e['email'],skills=skills)
        elif a == "False":
            message = a
            return render_template('signup.html', message=message )

    elif request.method == 'GET':
        return render_template('signup.html')



def verify_mail():
    mbv = MailboxValidator.EmailValidation("H4F1G609ZLDB1JVNTIT9")
    results = mbv.validate_email(e['email'])
    return results['is_verified']
        




@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register',methods = ['POST','GET'])
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
        pg['clg'] = request.form['ugcollege']
        pg['year'] = request.form ['ugyear']
        pg['degree'] = request.form['ugdegree']
        pg['cgpa'] = request.form['ugcgpa']

        skill = []
        for i in range(1,7):
            var = 'skill'+str(i)
            if request.form[var] != 'Choose a Skill':
                skill.append(request.form[var])

        proj = []
        for i in range(1,4):
            var = 'pj'+str(i)
            if request.form[var] != '':
                proj.append(request.form[var])

        comp = []
        for i in range(1,4):
            var = 'company'+str(i)
            if request.form[var] != '':
                comp.append(request.form[var])

        conn = db_conn()

        insert_sql = "INSERT INTO applicant (f_name,l_name,dob,gender,email,photo,mobile,password,username) VALUES (?,?,?,?,?,?,?,?,?)"
        prep_stmt = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, firstname )
        ibm_db.bind_param(prep_stmt, 2, lastname)
        ibm_db.bind_param(prep_stmt, 3, dob)
        ibm_db.bind_param(prep_stmt, 4, gender)
        ibm_db.bind_param(prep_stmt, 5, email)
        ibm_db.bind_param(prep_stmt, 6, render_file)
        ibm_db.bind_param(prep_stmt, 7,  e['mobno'])
        ibm_db.bind_param(prep_stmt, 8,  e['pswd'])
        ibm_db.bind_param(prep_stmt, 9,  e['username'])
        ibm_db.execute(prep_stmt)

        sql = "SELECT * FROM applicant WHERE email =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)

        pid = account['pid']

        insert_sql = "INSERT INTO acd_10 VALUES (?,?,?,?)"
        prep_stmt = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, pid )
        ibm_db.bind_param(prep_stmt, 2, c10['school'])
        ibm_db.bind_param(prep_stmt, 3, c10['year'] )    
        ibm_db.bind_param(prep_stmt, 4, c10['marks'] )
        ibm_db.execute(prep_stmt)

        insert_sql = "INSERT INTO acd_12 VALUES (?,?,?,?)"
        prep_stmt = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, pid )
        ibm_db.bind_param(prep_stmt, 2, c12['school'])
        ibm_db.bind_param(prep_stmt, 3, c12['year'] )    
        ibm_db.bind_param(prep_stmt, 4, c12['marks'] )
        ibm_db.execute(prep_stmt)

        insert_sql = "INSERT INTO acd_diploma VALUES (?,?,?,?)"
        prep_stmt = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, pid )
        ibm_db.bind_param(prep_stmt, 2, d['school'])
        ibm_db.bind_param(prep_stmt, 3, d['year'] )    
        ibm_db.bind_param(prep_stmt, 4, d['marks'] )
        ibm_db.execute(prep_stmt)

        insert_sql = "INSERT INTO acd_ug VALUES (?,?,?,?,?)"
        prep_stmt = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, pid )
        ibm_db.bind_param(prep_stmt, 2, ug['clg'])
        ibm_db.bind_param(prep_stmt, 3, ug['year'] )    
        ibm_db.bind_param(prep_stmt, 4, ug['degree'] )
        ibm_db.bind_param(prep_stmt, 5, ug['cgpa'] )
        ibm_db.execute(prep_stmt)

        insert_sql = "INSERT INTO acd_pg VALUES (?,?,?,?,?)"
        prep_stmt = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, pid )
        ibm_db.bind_param(prep_stmt, 2, pg['clg'])
        ibm_db.bind_param(prep_stmt, 3, pg['year'] )    
        ibm_db.bind_param(prep_stmt, 4, pg['degree'] )
        ibm_db.bind_param(prep_stmt, 5, pg['cgpa'] )
        ibm_db.execute(prep_stmt)

        insert_sql = "INSERT INTO project VALUES (?,?,?,?)"
        prep_stmt = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, pid )
        ibm_db.bind_param(prep_stmt, 2, proj[0])
        ibm_db.bind_param(prep_stmt, 3, proj[1])    
        ibm_db.bind_param(prep_stmt, 4, proj[2])
        ibm_db.execute(prep_stmt)

        insert_sql = "INSERT INTO skill VALUES (?,?,?,?,?,?,?)"
        prep_stmt = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, pid )
        ibm_db.bind_param(prep_stmt, 2, skill[0])
        ibm_db.bind_param(prep_stmt, 3, skill[1])    
        ibm_db.bind_param(prep_stmt, 4, skill[2])
        ibm_db.bind_param(prep_stmt, 2, skill[3])
        ibm_db.bind_param(prep_stmt, 3, skill[4])    
        ibm_db.bind_param(prep_stmt, 4, skill[5])
        ibm_db.execute(prep_stmt)
        
        insert_sql = "INSERT INTO top3_comp VALUES (?,?,?,?)"
        prep_stmt = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, pid )
        ibm_db.bind_param(prep_stmt, 2, comp[0])
        ibm_db.bind_param(prep_stmt, 3, comp[1])    
        ibm_db.bind_param(prep_stmt, 4, comp[2])
        ibm_db.execute(prep_stmt)
        

        return render_template('dashboard.html')
    elif request.method == 'GET':
        if session.get('email') == 'None':
            return render_template('signup.html')
        else:
            skills = ['Software Development','JavaScript', 'SQL' ,'AngularJS', 'Software Development Life Cycle (SDLC)','Agile Methodologies', 'Java', 'Dalim', 'jQuery', '.NET Framework', 'Requirements Analysis', 'PL/SQL', 'XML', 'HTML', 'Web Services', 'Node.js', 'Microsoft SQL Server', 'Oracle Database', 'C#', 'Unix', 'HTML5',' Cascading Style Sheets (CSS)', 'Web Development' ,'ASP.NET MVC', 'Language Integrated Query (LINQ)', 'ASP.NET' ,'Microsoft', 'Azure', 'TypeScript', 'Git', 'ASP.NET', 'Web API', 'Spring Boot', 'MySQL' ,'C++', 'Core Java','Choose a Skill']
            return render_template('Resume.html', required = session.get('email') ,skills=skills)


def render_picture(data):

    render_pic = base64.b64encode(data).decode('ascii') 
    return render_pic


        
@app.route('/dashboard',methods = ['GET'])
def dashboard():
    return render_template('dashboard.html')


app.add_url_rule('/dashboard', dashboard, dashboard) 



