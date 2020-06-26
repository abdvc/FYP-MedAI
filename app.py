from flask import Flask, render_template, url_for, request, redirect, session

app = Flask(__name__)
app.secret_key = "lightupskecher"

@app.route('/', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        session["email"] = request.form["inputEmail"]
        return redirect(url_for("home"))
    else:
        if "email" in session:
            return redirect(url_for("home"))
        return render_template('login.html')

@app.route('/home')
def home():
    if check_session():
        return render_template('home.html')
    else:
        return redirect(url_for("login"))

@app.route('/entry')
def entry():
    if check_session():
        return render_template('entry.html')
    else:
        return redirect(url_for("login"))

@app.route('/pathist')
def pathist():
    if check_session():
        return render_template('pathist.html')
    else:
        return redirect(url_for("login"))

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/dochist')
def dochist():
    return render_template('dochist.html')

@app.route('/logout')
def logout():
    session.pop("email", None)
    return redirect(url_for("login"))

def check_session():
    if "email" in session:
        return True
    else:
        False

if __name__ == "__main__":
    app.run(debug=True)