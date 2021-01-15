from flask import Flask, request, session
from flask_bcrypt import Bcrypt
from flask_mysqldb import MySQL
import os

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'lolilol123LOL'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'game_db'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(12)
session = { 'id' : None }

mysql = MySQL(app)

@app.route('/users',methods=['GET'])
def getUsers():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute("SELECT id,email,webpg,crypto,systlin,thsignalamp,thsignalpha,thgraph FROM users")
        results = cur.fetchall()
        return str(results)
    return "0"

@app.route('/me',methods=['GET'])
def getSessionId():
    if request.method == 'GET':
        return str(session['id'])
    return "0"

@app.route('/data',methods=['GET'])
def getData():
    if request.method == 'GET' and session['id'] != None:
        cur = mysql.connection.cursor()
        cur.execute("SELECT webpg,crypto,systlin,thsignalamp,thsignalpha,thgraph FROM users WHERE id=%s",[session['id']])
        results = cur.fetchall()
        return str(results)
    return "0"

@app.route('/register',methods=['POST'])
def register():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        #Fetch form data
        userDetails = request.form
        email = userDetails['email']
        password = userDetails['password']
        if(email != "" and email != None and password != "" and password != None):
            cur.execute("SELECT * FROM users WHERE email=%s",[email])
            results = cur.fetchall()
            if len(results) == 0:
                hash = bcrypt.generate_password_hash(password,10).decode('utf-8')
                cur.execute("INSERT INTO users (email,password,webpg,crypto,systlin,thsignalamp,thsignalpha,thgraph) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(email,hash,1,0,0,0,0,1))
                mysql.connection.commit()
                return "1"
            else:
                return "0"
    return "0"

@app.route('/login',methods=['POST'])
def login():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        #Fetch form data
        userDetails = request.form
        email = userDetails['email']
        password = userDetails['password']
        if(email != "" and email != None and password != "" and password != None):
            cur.execute("SELECT * FROM users WHERE email=%s",[email])
            results = cur.fetchall()
            if len(results) == 1:
                if bcrypt.check_password_hash(results[0]['password'],password):
                    session['id'] = results[0]['id']
                    return "1"
            else:
                return "0"
    return "0"

@app.route('/logout')
def logout():
    session['id'] = None
    print("Logged out")
    return "Logout success"

@app.route('/destroy',methods=['DELETE'])
def nuke():
    if request.method == 'DELETE':
        cur = mysql.connection.cursor()
        cur.execute("DROP TABLE users")
        cur.execute("CREATE TABLE users (id SERIAL PRIMARY KEY NOT NULL AUTO_INCREMENT, email TEXT, password TEXT, webpg INTEGER, crypto INTEGER, systlin INTEGER, thsignalamp INTEGER, thsignalpha INTEGER, thgraph INTEGER)")
        return '1'
    return '0'

# WebPG routes
@app.route('/updatewebpg',methods=['PUT'])
def updateWebPG():
    if request.method == 'PUT' and session['id'] != None:
        cur = mysql.connection.cursor()
        userDetails = request.form
        currentLevel = userDetails['level']
        cur.execute("SELECT webpg FROM users WHERE id=%s",[session['id']])
        result = cur.fetchall()
        if len(result) == 1:
            if int(currentLevel) > int(result[0]['webpg']) and int(currentLevel) < 5:
                cur.execute("UPDATE users SET webpg = %s WHERE id=%s",(int(currentLevel),session['id']))
                mysql.connection.commit()
            return "1"
    return '0'

# Crypto routes
@app.route('/updatecrypto',methods=['PUT'])
def updateCrypto():
    if request.method == 'PUT' and session['id'] != None:
        cur = mysql.connection.cursor()
        userDetails = request.form
        currentScore = userDetails['score']
        cur.execute("SELECT crypto FROM users WHERE id=%s",[session['id']])
        result = cur.fetchall()
        if len(result) == 1:
            cur.execute("UPDATE users SET crypto = %s WHERE id=%s",(int(currentScore)%8,session['id']))
            mysql.connection.commit()

            return "1"
    return '0'

# SystLin routes
@app.route('/updatesyst',methods=['PUT'])
def updateSyst():
    if request.method == 'PUT' and session['id'] != None:
        cur = mysql.connection.cursor()
        userDetails = request.form
        currentScore = userDetails['score']
        cur.execute("SELECT systlin FROM users WHERE id=%s",[session['id']])
        result = cur.fetchall()
        if len(result) == 1:
            if int(currentScore) > int(result[0]['systlin']):
                cur.execute("UPDATE users SET systlin = %s WHERE id=%s",(int(currentScore),session['id']))
                mysql.connection.commit()
            return "1"
    return '0'

@app.route('/systhighscore',methods=['GET'])
def getHighscore():
    if request.method == 'GET' and session['id'] != None:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id,systlin FROM users ORDER BY systlin DESC LIMIT 5")
        results = cur.fetchall()
        print(results)
        return str(results)
    return "0"

# ThSignal routes
@app.route('/updatethsamp',methods=['PUT'])
def updateSignalAmp():
    if request.method == 'PUT' and session['id'] != None:
        cur = mysql.connection.cursor()
        userDetails = request.form
        currentScore = userDetails['score']
        cur.execute("SELECT thsignalamp FROM users WHERE id=%s",[session['id']])
        result = cur.fetchall()
        if len(result) == 1:
            if int(currentScore) > int(result[0]['thsignalamp']):
                cur.execute("UPDATE users SET thsignalamp = %s WHERE id=%s",(int(currentScore),session['id']))
                mysql.connection.commit()
            return "1"
    return '0'

@app.route('/updatethspha',methods=['PUT'])
def updateSignalPha():
    if request.method == 'PUT' and session['id'] != None:
        cur = mysql.connection.cursor()
        userDetails = request.form
        currentScore = userDetails['score']
        cur.execute("SELECT thsignalpha FROM users WHERE id=%s",[session['id']])
        result = cur.fetchall()
        if len(result) == 1:
            if int(currentScore) > int(result[0]['thsignalpha']):
                cur.execute("UPDATE users SET thsignalpha = %s WHERE id=%s",(int(currentScore),session['id']))
                mysql.connection.commit()
            return "1"
    return '0'

# ThGraph routes
@app.route('/updatethg',methods=['PUT'])
def updateGraph():
    if request.method == 'PUT' and session['id'] != None:
        cur = mysql.connection.cursor()
        userDetails = request.form
        currentLevel = userDetails['level']
        cur.execute("SELECT thgraph FROM users WHERE id=%s",[session['id']])
        result = cur.fetchall()
        if len(result) == 1:
            if int(currentLevel) > int(result[0]['thgraph']) and int(currentLevel) < 5:
                cur.execute("UPDATE users SET thgraph = %s WHERE id=%s",(int(currentLevel),session['id']))
                mysql.connection.commit()
            return "1"
    return '0'


if __name__ == "__main__":
    app.run(debug=True)