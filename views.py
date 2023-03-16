from flask import *
from models import *
from fileMethods import *

def sign_in():
    status = True
    if request.method == "POST":
        users = Users.query.filter_by(username=request.form['username'], password=request.form['password']).first()

        if (users):
            writeFile(request.form['username'])
            return redirect('/index')
        else:
            status = False
    return render_template('sign_in.html', status=status)