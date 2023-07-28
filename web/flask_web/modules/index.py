# This file is part of https://github.com/jainamoswal/Flask-Example.
# Usage covered in <IDC lICENSE>
# Jainam Oswal. <jainam.me> 


# Import Libraries 
from app import app

from flask import   render_template
# Define route "/" & "/<name>"
@app.route("/test")
@app.route("/test/<name>")
def index(name='Anonymous'):
    return f"Hello {name}!!"


@app.route('/')
@app.route('/index2')
def index2():
    name = 'Rosalia'
    return render_template('index.html', title='Welcome', username=name)
