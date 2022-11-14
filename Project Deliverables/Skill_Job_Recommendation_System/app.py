from flask import Flask,render_template,request
import ibm_db
import MailboxValidator



conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=b1bc1829-6f45-4cd4-bef4-10cf081900bf.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32304;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=khc44923;PWD=VMdkxmMxV1Z30kOH",'','')


app = Flask(__name__)



e = {}

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
            return render_template('signup.html', message=a+" Email not Valid.")

    elif request.method == 'GET':
        return render_template('signup.html')



def verify_mail():
    mbv = MailboxValidator.EmailValidation('H4F1G609ZLDB1JVNTIT9')
    results = mbv.validate_email(e['email'])
    if results['status'] == True:
        return True
    else:
        return results['error_message']




@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register',methods = ['POST','GET'])
def register():
    if request.method == 'POST':
        return render_template('dashboard.html')
    elif request.method == 'GET':
        skills = ['Software Development','JavaScript', 'SQL' ,'AngularJS', 'Software Development Life Cycle (SDLC)','Agile Methodologies', 'Java', 'Dalim', 'jQuery', '.NET Framework', 'Requirements Analysis', 'PL/SQL', 'XML', 'HTML', 'Web Services', 'Node.js', 'Microsoft SQL Server', 'Oracle Database', 'C#', 'Unix', 'HTML5',' Cascading Style Sheets (CSS)', 'Web Development' ,'ASP.NET MVC', 'Language Integrated Query (LINQ)', 'ASP.NET' ,'Microsoft', 'Azure', 'TypeScript', 'Git', 'ASP.NET', 'Web API', 'Spring Boot', 'MySQL' ,'C++', 'Core Java','Choose a Skill']
        return render_template('Resume.html', skills=skills)
        
@app.route('/dashboard',methods = ['GET'])
def dasboard():
    return render_template('dashboard.html')



