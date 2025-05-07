from flask import Blueprint, render_template, request, redirect, session, jsonify
from vms_sql import check_admin, insert_event, get_all_events, get_event_by_id, update_event_by_id, delete_event, get_all_volunteers
from datetime import datetime

admin_blueprint = Blueprint('admin', __name__)

# Admin Login API
@admin_blueprint.route('/admin/login', methods=['POST'])
def admin_login():
    admin_id = request.form['admin_id']
    password = request.form['password']

    if not admin_id or not password:
        return jsonify({'error': 'All fields are required.'})

    if check_admin(admin_id, password):
        session['admin_id'] = admin_id
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Invalid Admin ID or Password.'})

# Admin Dashboard
@admin_blueprint.route('/admin/dashboard')
def admin_dashboard():
    if 'admin_id' not in session:
        return redirect('/admin_signin')
    return render_template('admin_dashboard.html')
    
# Route to render the Create Event Page
@admin_blueprint.route('/admin/create_event', methods=['GET'])
def show_create_event_form():
    if 'admin_id' not in session:
        return redirect('/admin_signin')  # Protect access
    return render_template('create_event.html')

# API Route to handle form submission
@admin_blueprint.route('/admin/create_event', methods=['POST'])
def create_event():
    event_name = request.form.get('event_name')
    description = request.form.get('description')
    start_datetime_str = request.form.get('start_datetime')
    end_datetime_str = request.form.get('end_datetime')
    address = request.form.get('address')

    if not all([event_name, description, start_datetime_str, end_datetime_str, address]):
        return jsonify({'error': 'All fields are required.'})

    try:
        # Parse the datetime strings to datetime objects
        start_datetime = datetime.strptime(start_datetime_str, '%Y-%m-%dT%H:%M')
        end_datetime = datetime.strptime(end_datetime_str, '%Y-%m-%dT%H:%M')
    except ValueError:
        return jsonify({'error': 'Invalid date/time format.'})

    if start_datetime >= end_datetime:
        return jsonify({'error': 'Start date/time must be before end date/time.'})
        
    if start_datetime < datetime.now():
        return jsonify({'error': 'Start date/time cannot be in the past.'})

    try:
        event_id = insert_event(event_name, description, start_datetime_str, end_datetime_str, address)

        return jsonify({'success': True, 'event_id': event_id})
    except Exception as e:
        print(e)
        return jsonify({'error': 'Failed to create event. Please try again.'})


# View All Events
@admin_blueprint.route('/admin/view_events')
def view_events():
    events = get_all_events()
    return render_template('View_Events.html', events=events)
    

# Edit Event Page
@admin_blueprint.route('/admin/edit_event/<event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    if 'admin_id' not in session:
        return redirect('/admin_signin')

    if request.method == 'POST':
        event_name = request.form['event_name']
        description = request.form['description']
        start_datetime = request.form['start_datetime']
        end_datetime = request.form['end_datetime']
        address = request.form['address']

        update_event_by_id(event_id, event_name, description, start_datetime, end_datetime, address)
        return redirect('/admin/view_events') 

    event = get_event_by_id(event_id)
    if not event:
        return "Event not found", 404

    return render_template('edit_event.html', event=event)    
    
@admin_blueprint.route('/admin/delete_event_route/<event_id>', methods=['DELETE'])
def delete_event_route(event_id):
    try:
        delete_event(event_id)  # Call DB function
        return jsonify({'success': True})
    except Exception as e:
        print(e)
        return jsonify({'success': False, 'error': str(e)})    
        
@admin_blueprint.route('/admin/view_volunteers')
def view_volunteers():
    volunteers = get_all_volunteers()
    return render_template('view_volunteers.html', volunteers=volunteers)     

@admin_blueprint.route('/admin/admin_logout')
def admin_logout():
    session.pop('admin_id', None)   # Remove admin session
    session.pop('admin_name', None) # If you're storing admin name
    return render_template('index.html')   # Redirect to admin login page    