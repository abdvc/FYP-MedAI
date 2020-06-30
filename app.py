from flask import Flask, render_template, url_for, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "lightupskecher"
conn = sqlite3.connect("MedAi.db", check_same_thread=False)

def get_features(model_id):
    """
    can we get an alternate type for easier to understand input?
    """
    query = 'select name,type,feat_order from features where model_id = ?'
    cur = conn.execute(query,(model_id,))

    return cur.fetchall()

app.jinja_env.globals.update(get_features=get_features)

def add_features(model_id,features, feature_types, feat_order=None):

    feature_query = 'insert into features (name, type, model_id, feat_order) values (?,?,?,?)'
    i = 0
    for feature in features:
        if feat_order is None:
            if feature_types is None:
                conn.execute(feature_query,[feature,'string',model_id,i])
            else:
                conn.execute(feature_query,[feature,feature_types[i],model_id,i])
        else:
            if feature_types is None:
                conn.execute(feature_query,[feature,'string',model_id,feat_order[i]])
            else:
                conn.execute(feature_query,[feature,feature_types[i],model_id,feat_order[i]])
        i = i + 1
    conn.commit()

#TODO: validation
def add_model(model, model_name, desc, features=None,feature_types=None, feat_order=None, preprocess=None):
    model_query = 'insert into models (name,description,model) values (?,?,?)'
    conn.execute(model_query,[model_name,desc,model])
    conn.commit()

    get_id_query = 'select MAX(id) from models'
    cur = conn.execute(get_id_query)
    model_id = cur.fetchone()
    model_id = model_id[0]

    if features is not None:
        add_features(model_id,features,feature_types, feat_order)
    
    if preprocess is not None:
        preprocess_query = 'insert into preprocess (file_name,model_id) values (?,?)'
        conn.execute(preprocess_query,[preprocess, model_id])
    
    return model_id

#TODO: finish method
def convert_input():
    """
    convert input given through form into a model readable form. can be done through calling preprocess after converting to something like a dataframe
    additional arguements for further customization?
    """
    return None

# finish
def prediction():
    """
    give input to model for prediction

    """
    return None
    
def explain():
    """
    explain the results of the model prediction in this method

    """
    return None

@app.route('/', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form["inputEmail"]
        session["email"] = email
        res = conn.execute('SELECT * from Users where email=?', (email,)).fetchone()
        if res == None:
            return render_template('login.html', message="Email does not exist")
        elif res[3] == request.form["inputPassword"]:
            return redirect(url_for("home"))
        else:
            return render_template('login.html', message="Incorrect password")
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