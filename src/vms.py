from flask import Flask, render_template
import secrets
from volunteer import volunteer_blueprint
from admin import admin_blueprint
from vms_sql import init_db

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# Initialize the database (called once when the app is started)
init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup')
def signup_form():
    return render_template('volunteer_Signup.html')  # Render the Signup form
    
@app.route('/signin')
def signin_form():
    return render_template('volunteer_SignIn.html')  # Render the SignIn form     

# Admin Login Page
@app.route('/admin_signin')
def admin_form():
    return render_template('admin_login.html')    

# Register the blueprints
app.register_blueprint(volunteer_blueprint) #, url_prefix='/volunteer')
app.register_blueprint(admin_blueprint)    

if __name__ == '__main__':
    app.run(debug=True)
