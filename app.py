from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

# Connect to the PostgreSQL DB
def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST"),
        database=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        port=os.environ.get("DB_PORT", "5432")
    )

@app.route('/')
def home():
    return "Shubha Mangal API is live!"

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    try:
        userid = data['userid']
        password = data['password']
        firstName = data['firstName']
        lastName = data['lastName']
        gender = data['gender']
        dob = data['dob']
        maritalStatus = data['maritalStatus']
        motherTongue = data['motherTongue']
        religion = data['religion']
        caste = data['caste']
        subCaste = data['subCaste']
        email = data['email']
        mobile = data['mobile']

        conn = get_db_connection()
        cur = conn.cursor()

        # Check if user already exists
        cur.execute("SELECT 1 FROM users WHERE userid = %s", (userid,))
        if cur.fetchone():
            return jsonify({'status': 'fail', 'message': 'User ID already exists'}), 400

        # Insert all fields
        cur.execute("""
            INSERT INTO users (
                userid, password, firstName, lastName, gender, dob, maritalStatus,
                motherTongue, religion, caste, subCaste, email, mobile
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            userid, password, firstName, lastName, gender, dob, maritalStatus,
            motherTongue, religion, caste, subCaste, email, mobile
        ))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'status': 'success'})

    except Exception as e:
        return jsonify({'status': 'fail', 'error': str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    userid = data.get('userid')
    password = data.get('password')

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM users WHERE userid = %s AND password = %s", (userid, password))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'fail', 'message': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'status': 'fail', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
