from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# ---------------- DASHBOARD ----------------
@app.route('/')
def dashboard():
    conn = get_db_connection()
    tenants = conn.execute('SELECT * FROM tenants').fetchall()
    conn.close()
    return render_template('dashboard.html', tenants=tenants)

# ---------------- ADD TENANT ----------------
@app.route('/add_tenant', methods=('GET', 'POST'))
def add_tenant():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        rent = request.form['rent']

        conn = get_db_connection()
        conn.execute(
            'INSERT INTO tenants (name, phone, rent) VALUES (?, ?, ?)',
            (name, phone, rent)
        )
        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('add_tenant.html')

# ---------------- ADD PAYMENT ----------------
@app.route('/add_payment/<int:tenant_id>', methods=('GET', 'POST'))
def add_payment(tenant_id):
    conn = get_db_connection()
    tenant = conn.execute(
        'SELECT * FROM tenants WHERE id = ?', (tenant_id,)
    ).fetchone()

    if request.method == 'POST':
        amount = request.form['amount']
        expected_date = request.form['expected_date']
        notes = request.form['notes']
        status = request.form['status']

        payment_date = None
        receipt_number = None

        if status == "Paid":
            payment_date = datetime.now().strftime("%Y-%m-%d")
            receipt_number = "RCPT" + datetime.now().strftime("%Y%m%d%H%M%S")

        conn.execute('''
            INSERT INTO payments
            (tenant_id, amount, payment_date, expected_date, status, notes, receipt_number)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            tenant_id,
            amount,
            payment_date,
            expected_date,
            status,
            notes,
            receipt_number
        ))

        conn.commit()
        conn.close()
        return redirect('/history/' + str(tenant_id))

    conn.close()
    return render_template('add_payment.html', tenant=tenant)

# ---------------- MARK PAID ----------------
@app.route('/mark_paid/<int:payment_id>')
def mark_paid(payment_id):
    conn = get_db_connection()

    receipt_number = "RCPT" + str(payment_id) + str(datetime.now().strftime("%Y%m%d%H%M%S"))

    conn.execute('''
        UPDATE payments
        SET status = "Paid",
            payment_date = ?,
            receipt_number = ?
        WHERE id = ?
    ''', (datetime.now().strftime("%Y-%m-%d"), receipt_number, payment_id))

    conn.commit()
    conn.close()

    return redirect('/')

# ---------------- VIEW HISTORY ----------------
@app.route('/history/<int:tenant_id>')
def history(tenant_id):
    conn = get_db_connection()

    tenant = conn.execute(
        'SELECT * FROM tenants WHERE id = ?', (tenant_id,)
    ).fetchone()

    payments = conn.execute(
        'SELECT * FROM payments WHERE tenant_id = ?', (tenant_id,)
    ).fetchall()

    conn.close()

    return render_template('history.html', tenant=tenant, payments=payments)

if __name__ == '__main__':
    app.run(debug=True)
