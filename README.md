# Pari_Bansal_AIMLD_VMS
Volunteer Management System 

## Team Members
- Pari Bansal  
- Anushka Singh  
- Arpita Roy  
- Kaashvi Gupta

## 📽️ Video Explanation
[Watch the Project Demo](https://drive.google.com/file/d/1_SLykODGgbQOROSKCNYXjUgRd-TzApn3/view?usp=drive_link)

# Volunteer Management System

This is a Volunteer Management System built using **Python Flask**, **SQLite**, and **HTML/CSS**. It allows admins to manage events and volunteers to register, participate, and receive certificates for events.

---

## Features

- Admin login & event management
- Volunteer signup/login
- Register/Unregister for events
- Role selection during event registration
- View registered/upcoming events
- Certificate eligibility tracking (Enhancements)

---

## 🛠️ Technologies Used

- Python 3
- Flask
- SQLite
- HTML/CSS (Jinja2 Templates)
- Werkzeug (for password hashing)

---

## Installation & Setup

### 1. Clone the Repository

'''bash
git clone  https://github.com/PariBansal/Pari_Bansal_AIML4_VMS
cd Pari_Bansal_AIML4_VMS

### 2. Create Virtual Env
python -m venv venv

### 3. Activate Virtual Environment
Windows: venv\Scripts\activate
Linux/ MacOS: source venv/bin/activate

### 4. Install Dependencies
pip install -r requirements.txt

### 5. Configuration
Set Flask environment variables:

Windows: 
set FLASK_APP=vms.py
set FLASK_ENV=development

Linux/ MacOS: 
export FLASK_APP=vms.py
export FLASK_ENV=development

### 5. Run the application
python vms.py
flask run
Then visit http://localhost:5000 in your browser.
