from flask import Flask,render_template


app = Flask(__name__)

@app.route('/register')
def register():
    return render_template('Registeration.html')
