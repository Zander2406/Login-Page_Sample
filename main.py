from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/testlogin"
db = SQLAlchemy(app)


class Accounts_Details(db.Model):
    username = db.Column(db.String(25), primary_key=True)
    email = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(30), nullable=False)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    users = Accounts_Details.query.all()
    if request.method == 'POST':
        guest = request.form.get('username')
        guest_password = request.form.get('password')
        for user in users:
            message = "This user doesn't exist. Please check your username or Sign Up"
            if guest == user.username:
                if guest_password == user.password:
                    return render_template('dashboard.html')
                else:
                    message = "You have entered the wrong password"
    return render_template('login.html', message=message)


@app.route('/create', methods=['GET', 'POST'])
def create_account():
    error = None
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            if password != confirm_password:
                error = "Please enter password again"
            else:
                entry = Accounts_Details(username=username, email=email, password=password)
                db.session.add(entry)
                db.session.commit()
                error = "Created account successfully"
    except IntegrityError:
        error = "Username already taken"
    return render_template('create_account.html', error=error)


app.run(debug=True)