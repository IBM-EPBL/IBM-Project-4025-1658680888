from flask import Flask, render_template
 

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
 

if __name__ == '__main__':
    app.run()