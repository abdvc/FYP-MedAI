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
    if "email" in session:
        return render_template('home.html')
    else:
        return redirect(url_for("login"))

@app.route('/logout')
def logout():
    session.pop("email", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
