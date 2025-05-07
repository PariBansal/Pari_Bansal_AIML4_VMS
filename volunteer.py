# volunteer.py
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, flash
from vms_sql import *
from datetime import datetime
from werkzeug.security import check_password_hash

volunteer_blueprint = Blueprint('volunteer', __name__)

@volunteer_blueprint.route('/volunteer/volunteer_signup', methods=['POST'])
def volunteer_signup():
    if request.method == 'POST':
        # Get the form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        mobile = request.form['mobile']
        course = request.form['course']
        semester = request.form['semester']

        # Check if volunteer already exists
        if check_existing_user(email, mobile):
            return jsonify({"error": "A user with this email or mobile number already exists."}), 409

        try:
            volunteer_id = insert_volunteer(first_name, last_name, email, password, mobile, course, semester)
            session['volunteer_id'] = volunteer_id
            session['volunteer_name'] = first_name
            return jsonify({"message": "Volunteer registered successfully!", "volunteer_id": volunteer_id}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return render_template('volunteer_Signup.html')

@volunteer_blueprint.route('/volunteer/volunteer_dashboard')
def volunteer_dashboard():
    volunteer_name = session.get('volunteer_name', 'Guest')
    return render_template('volunteer_dashboard.html', volunteer_name=volunteer_name)

@volunteer_blueprint.route('/volunteer/profile')
def volunteer_profile():
    volunteer_id = session.get('volunteer_id')
    if not volunteer_id:
        return render_template('volunteer_SignIn.html')

    volunteer = get_volunteer_by_id(volunteer_id)
    return render_template('volunteer_profile.html', volunteer=volunteer)


@volunteer_blueprint.route('/volunteer/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    volunteer_id = session.get('volunteer_id')
    if not volunteer_id:
        return render_template('volunteer_SignIn.html')

    volunteer = get_volunteer_by_id(volunteer_id)

    if request.method == 'POST':
        data = {
            'first_name': request.form.get('first_name'),
            'last_name': request.form.get('last_name'),
            'mobile': request.form.get('mobile'),
            'course': request.form.get('course'),
            'semester': request.form.get('semester')
        }
        update_volunteer(volunteer_id, data)
        return redirect('/volunteer/profile')

    return render_template('edit_volunteer_profile.html', volunteer=volunteer)


@volunteer_blueprint.route('/volunteer/delete_profile', methods=['GET', 'POST'])
def delete_profile():
    volunteer_id = session.get('volunteer_id')
    if volunteer_id:
        delete_volunteer(volunteer_id)
        session.clear()
    return render_template('index.html')


@volunteer_blueprint.route('/logout')
def logout():
    session.clear()  # Clear all session data
    return render_template('index.html')

@volunteer_blueprint.route('/volunteer/upcoming_events')
def upcoming_events():
    volunteer_id = session.get('volunteer_id')
    if not volunteer_id:
        return render_template('volunteer_SignIn.html')

    conn = get_db_connection()
    events = conn.execute('SELECT * FROM events WHERE start_datetime >= ? ORDER BY start_datetime ASC', (datetime.now(),)).fetchall()
    registered = conn.execute('SELECT event_id FROM event_volunteer WHERE volunteer_id = ?', (volunteer_id,)).fetchall()
    conn.close()

    registered_event_ids = {row['event_id'] for row in registered}

    return render_template('volunteer_upcoming_events.html', events=events, registered_event_ids=registered_event_ids)

@volunteer_blueprint.route('/volunteer/register_event/<event_id>', methods=['POST'])
def register_event(event_id):
    volunteer_id = session.get('volunteer_id')
    if not volunteer_id:
        return render_template('volunteer_SignIn.html')

    role = request.form.get('role')
    if not role:
        flash('Please select a role before registering.', 'warning')
        return redirect('/volunteer/upcoming_events')

    conn = get_db_connection()
    existing = conn.execute('SELECT 1 FROM event_volunteer WHERE event_id = ? AND volunteer_id = ?', (event_id, volunteer_id)).fetchone()
    if existing:
        flash('You are already registered for this event.', 'info')
    else:
        conn.execute('INSERT INTO event_volunteer (event_id, volunteer_id, role, certificate) VALUES (?, ?, ?, ?)', (event_id, volunteer_id, role, False))
        conn.commit()
        flash('Successfully registered for the event as {}!'.format(role), 'success')
    conn.close()

    return redirect('/volunteer/upcoming_events')
    
@volunteer_blueprint.route('/volunteer/registered_events')
def registered_events():
    volunteer_id = session.get('volunteer_id')
    if not volunteer_id:
        return render_template('volunteer_SignIn.html')

    result = get_registered_events(volunteer_id)
    if not result['success']:
        return render_template('registered_events.html', events=[], error=result['message'], now=datetime.now())

    return render_template('registered_events.html', events=result['data'], now=datetime.now())

@volunteer_blueprint.route('/volunteer/unregister/<event_id>', methods=['POST'])
def unregister_event(event_id):
    volunteer_id = session.get('volunteer_id')
    if not volunteer_id:
        return render_template('volunteer_SignIn.html')
    
    result = unregister_from_event(volunteer_id, event_id)

    return redirect('/volunteer/registered_events')
        
@volunteer_blueprint.route('/volunteer/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM volunteers WHERE email = ?", (email,))
        volunteer = cursor.fetchone()
        conn.close()

        if volunteer and check_password_hash(volunteer['password'], password):  # Use `check_password_hash()` if hashed
            session['volunteer_id'] = volunteer['volunteer_id']
            session['volunteer_name'] = f"{volunteer['first_name']} {volunteer['last_name']}"
            return redirect('/volunteer/volunteer_dashboard')

        error = 'Invalid email or password.'
        return render_template('volunteer_signin.html', error=error)

    return render_template('volunteer_signin.html')