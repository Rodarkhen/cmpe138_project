from flask import render_template, redirect, url_for, session
from app import myapp_obj
from .forms import LoginForm, RegistrationForm

@myapp_obj.route('/')
def home():
    # Display library catalog and search functionality
    return render_template('home.html')

@myapp_obj.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Process login form submission
        # Example:
        # username = form.username.data
        # password = form.password.data
        # Check username and password against database
        # If authentication successful, set session and redirect
        # Else, return error message
        return redirect(url_for('home'))
    return render_template('login.html', form=form)

@myapp_obj.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Process registration form submission
        # Example:
        # username = form.username.data
        # password = form.password.data
        # Confirm password = form.confirm_password.data
        # Validate and create user account
        # Redirect to login page or dashboard upon successful registration
        return redirect(url_for('login'))
    return render_template('register.html', form=form)
