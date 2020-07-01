from flask import Flask, render_template, url_for, request, redirect, session, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = "lightupskecher"
conn = sqlite3.connect("MedAi.db", check_same_thread=False)

def model_list():
    query = "select id, name, description from models"

    cur = conn.execute(query)

    return cur.fetchall()

def get_features(model_id):
    """
    can we get an alternate type for easier to understand input?
    """
    query = 'select name,type,feat_order from features where model_id = ?'
    cur = conn.execute(query,(model_id,))

    return cur.fetchall()

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
    with open(model, 'rb') as f:
        clf = pickle.load(f)
    loaded_model = pickle.dumps(clf)
    model_query = 'insert into models (name,description,model) values (?,?,?)'
    conn.execute(model_query,[model_name,desc,loaded_model])
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

#login page
@app.route('/', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form["inputEmail"]
        res = conn.execute('SELECT * from Users where email=?', (email,)).fetchone()
        if res == None:
            return render_template('login.html', message="Email does not exist")
        elif res[3] == request.form["inputPassword"]:
            session["email"] = email
            session["admin"] = res[4]
            session["name"] = res[1]
            if res[4] == 1:
                return redirect(url_for("admin"))
            else:
                return redirect(url_for("home"))
        else:
            return render_template('login.html', message="Incorrect password")
    else:
        if "email" in session:
            return redirect(url_for("home"))
        return render_template('login.html', message="  ")

#route to doctor home page
@app.route('/home')
def home():
    if check_session():
        if check_admin() == 0:
            return render_template('home.html')
        else:
            return redirect(url_for("admin"))
    else:
        return redirect(url_for("login"))

#route to data entry page
@app.route('/entry')
def entry():
    if check_session():
        if check_admin() == 0:
            return render_template('entry.html')
        else:
            return redirect(url_for("admin"))
    else:
        return redirect(url_for("login"))

#route to patient history
@app.route('/pathist')
def pathist():
    if check_session():
        if check_admin() == 0:
            return render_template('pathist.html')
        else:
            return redirect(url_for("admin"))
    else:
        return redirect(url_for("login"))

#route to admin home page
@app.route('/admin')
def admin():
    if check_session():
        if check_admin() == 1:
            return render_template('admin.html')
        else:
            return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))

#route to doctor history page
@app.route('/dochist')
def dochist():
    if check_session():
        if check_admin() == 1:
            return render_template('dochist.html')
        else:
            return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))

#login function
@app.route('/logout')
def logout():
    session.pop("email", None)
    session.pop("name", None)
    session.pop("admin", None)
    return redirect(url_for("login"))

@app.route('/entry/_get_data/', methods=['POST'])
def _get_data():
    return jsonify({'data': render_template('response.html')})

#method to check if session is valid
def check_session():
    if "email" in session:
        return True
    else:
        False

#Method to check if the user is an admin or doctor
def check_admin():
    if session["admin"] == 1:
        return True
    else:
        return False

app.jinja_env.globals.update(get_features=get_features)
app.jinja_env.globals.update(model_list=model_list)

if __name__ == "__main__":
    app.run(debug=True)