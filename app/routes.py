from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User, Opportunity

# Define a Blueprint for routes
main = Blueprint('main', __name__)

# Home page route
@main.route('/')
def index():
    return render_template('index.html')


# Registration Route
@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Hash the password for security
        hashed_password = generate_password_hash(password, method='sha256')

        # Add the new user to the database
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html')


# Login Route
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the user exists in the database
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            # Store the user_id in the session after successful login
            session['user_id'] = user.id  # Store user_id in session

            flash('Login successful!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Login failed. Invalid email or password.', 'danger')

    return render_template('login.html')


# Dashboard Route
@main.route('/dashboard')
def dashboard():
    # Ensure the user is logged in before accessing the dashboard
    if 'user_id' not in session:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('main.login'))

    opportunities = Opportunity.query.all()  # Fetching all opportunities from the database
    return render_template('dashboard.html', opportunities=opportunities)


# Create Opportunity Route
@main.route('/create_opportunity', methods=['GET', 'POST'])
def create_opportunity():
    if 'user_id' not in session:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('main.login'))

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']

        # Create a new opportunity and add to the database
        new_opportunity = Opportunity(name=name, description=description)
        db.session.add(new_opportunity)
        db.session.commit()

        flash('Opportunity created successfully!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('create_opportunity.html')


# Logout Route
@main.route('/logout')
def logout():
    # Clear the user session (e.g., remove 'user_id' or other session variables)
    session.pop('user_id', None)  # Example: Remove the 'user_id' from session
    flash('You have been logged out.', 'success')  # Flash a success message
    return redirect(url_for('main.login'))  # Redirect to the login page after logout
