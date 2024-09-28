from flask import Flask,render_template,request,session,redirect
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'enithaJR'
app.config['MYSQL_DB'] = 'login'
app.secret_key = '2685'

mysql = MySQL(app)

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    # render_template('index.html')
    msg = 'Something went wrong'
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        user = request.form['username']
        pswd = request.form['password']
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("select * from accounts where username = %s and password = %s", (user, pswd,))
            account = cursor.fetchone()
            if account:
                # session['loggedin'] = True
                # session['id'] = account['id']
                # session['username'] = account['username']
                msg='Logged in successfully'
                print(msg)
                return render_template('home.html' ,msg=msg)
            else:
                msg = 'Incorrect username/password!'
        except MySQLdb.Error as e:
            msg = 'Database error: {}'.format(e)
    print(msg)
    return render_template('index.html', msg=msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = 'Something went wrong'
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            if not username or not password:
                msg = 'Please fill out the form!'
                print(msg)
                return render_template('register.html', msg=msg)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('select * from accounts where username = %s',(username,))
            account = cursor.fetchone()
            if account:
                msg = 'Account already exists!'
            else:
                cursor.execute('insert into accounts(username,password) values(%s,%s)',(username,password,))
                mysql.connection.commit()
                msg = 'You have successfully registered!'
                print(msg)
                return redirect(url_for('login'))
    print(msg)
    return render_template('register.html', msg=msg)

if __name__ == '__main__':
    app.run(debug=True)