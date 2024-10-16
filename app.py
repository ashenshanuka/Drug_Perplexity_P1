from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from datetime import datetime

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'pharmacy_perplexity_db'

mysql = MySQL(app)

app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM drugs")
    drugs = cur.fetchall()
    cur.close()
    return render_template('index.html', drugs=drugs)

@app.route('/add', methods=['GET', 'POST'])
def add_drug():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']
        expiration_date = request.form['expiration_date']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO drugs (name, quantity, price, expiration_date) VALUES (%s, %s, %s, %s)",
                    (name, quantity, price, expiration_date))
        mysql.connection.commit()
        cur.close()

        flash('Drug added successfully', 'success')
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_drug(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']
        expiration_date = request.form['expiration_date']

        cur.execute("UPDATE drugs SET name=%s, quantity=%s, price=%s, expiration_date=%s WHERE id=%s",
                    (name, quantity, price, expiration_date, id))
        mysql.connection.commit()
        flash('Drug updated successfully', 'success')
        return redirect(url_for('index'))

    cur.execute("SELECT * FROM drugs WHERE id = %s", (id,))
    drug = cur.fetchone()
    cur.close()
    return render_template('edit.html', drug=drug)

@app.route('/delete/<int:id>')
def delete_drug(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM drugs WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    flash('Drug deleted successfully', 'success')
    return redirect(url_for('index'))

@app.route('/search', methods=['GET', 'POST'])
def search_drug():
    if request.method == 'POST':
        search_term = request.form['search_term']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM drugs WHERE name LIKE %s OR id = %s", (f'%{search_term}%', search_term))
        drugs = cur.fetchall()
        cur.close()
        return render_template('search.html', drugs=drugs, search_term=search_term)
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)