from flask import Flask, render_template, request, redirect, flash
import mysql.connector
import re
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="contact_form_db"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        if not re.match(r'^[A-Za-z\s]+$', name):
            flash('Name should contain only alphabetic characters', 'error')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email format', 'error')
        elif len(message) < 10:
            flash('Message should be at least 10 characters long', 'error')
        else:
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute('''INSERT INTO contact_form_submissions (name, email, subject, message) VALUES (%s, %s, %s, %s)''', (name, email, subject, message))
                conn.commit()
                cursor.close()
                conn.close()

                flash('Your message has been sent successfully!', 'success')
                return redirect('/')
            else:
                flash('Failed to connect to the database. Please check your credentials.', 'error')


    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
 