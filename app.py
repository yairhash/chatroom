from flask import Flask , render_template , url_for , redirect , request ,jsonify ,session
app = Flask(__name__)
app.secret_key='c5fa941f05e5bb9239e0ef64a09663b2aaee3f8bca283a36'
from user import User
from mongo import Db
from passlib.hash import pbkdf2_sha256
import uuid


db=Db()
 

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/signup_login',methods=['POST','GET'])
def signup_login():
    if 'email' in session:
        return render_template('dashboard.html',online_user=online_user)
    return render_template('signup_login.html')



@app.route('/signup',methods=['POST','GET'])
def signup():
    new_user=User(uuid.uuid4().hex,request.form['name'],request.form['age'],request.form['email'],request.form['password'])
    if request.method=='POST': 
        user_after_validation=db.insert_to_db(new_user)
        if user_after_validation:
            session['email']=new_user.email
            return  redirect('dashboard')
        return 'user already exist'
    return render_template('signup.html')


@app.route('/checkuserexists',methods=['POST'])
def checkuserexists():   
    user_email=request.form['email']
    is_exist=db.check_user_exist(user_email)
    return jsonify(is_exist),200

   
@app.route('/login', methods=['POST'])
def login():
    _id,name,age,email,password=db.get_user_from_db(request.form['email'])
    user_from_db=User(_id,name,age,email,password)
    verify_password=pbkdf2_sha256.verify(request.form['password'],user_from_db.password)
    if request.form['email']==user_from_db.email and verify_password:
        session['email']=user_from_db.email   
        global online_user
        online_user=User(user_from_db._id,user_from_db.name,user_from_db.age,request.form['email'],request.form['password'])
        return redirect(url_for('dashboard'))
    return 'wrong password/name combination'    
        
    
@app.route('/dashboard',methods=['POST','GET'])
def dashboard():
    if 'email' in session:
        return render_template('dashboard.html',online_user=online_user)
    return 'something went wrong'
    
@app.route('/signout',methods=['POST','GET'])
def signout():
    if 'email' in session:
        session.clear()
        return redirect('/')
        

    
if __name__ == '__main__':
    app.run(debug=True) 