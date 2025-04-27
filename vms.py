from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Initialize database from vms.sql
def init_db():
    if not os.path.exists('volunteers.db'):
        conn = sqlite3.connect('volunteers.db')
        with open('vms.sql', 'r') as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()

@app.route('/')
def home():
    return render_template('volunty.html')

@app.route('/api/register', methods=['POST'])
def register_volunteer():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    role = data.get('role')

    if not name or not email or not phone or not role:
        return jsonify({"error": "All fields are required."}), 400

    try:
        conn = sqlite3.connect('volunteers.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO volunteers (name, email, phone, role) VALUES (?, ?, ?, ?)', (name, email, phone, role))
        conn.commit()
        conn.close()

        return jsonify({"message": "Volunteer registered successfully!"}), 201

    except sqlite3.IntegrityError:
        return jsonify({"error": "Email or phone number already exists."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/volunteers', methods=['GET'])
def get_volunteers():
    conn = sqlite3.connect('volunteers.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, email, phone, role FROM volunteers')
    rows = cursor.fetchall()
    conn.close()

    volunteers = [{"id": row[0], "name": row[1], "email": row[2], "phone": row[3], "role": row[4]} for row in rows]
    return jsonify(volunteers)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
