import base64
import random
from flask import Flask,render_template,request,session
import ibm_db,re
import MailboxValidator





conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=b1bc1829-6f45-4cd4-bef4-10cf081900bf.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32304;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=khc44923;PWD=VMdkxmMxV1Z30kOH",'','')


app = Flask(__name__)
val = random.randint(100000, 999999)
app.secret_key = str(val) 


e = {}

@app.route('/sign-up',methods = ['POST','GET'])
@app.route('/')
def signup():
    if request.method == 'POST':
        e['email'] = request.form['email']
        e['mobno'] = request.form['mobile number']
        e['username'] = request.form['username']
        
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
        d['school'] = request.form['dcourse']
        d['year'] = request.form ['dyear']
        d['marks'] = request.form['dmarks']

        ug = {}
        ug['school'] = request.form['ugcollege']
        ug['year'] = request.form ['ugyear']
        ug['degree'] = request.form['ugdegree']
        ug['cgpa'] = request.form['ugcgpa']

        pg = {}
        pg['school'] = request.form['ugcollege']
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



