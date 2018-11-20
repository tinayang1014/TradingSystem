from flask import Flask, render_template, json, request
import mysql.connector as mc
from werkzeug import generate_password_hash, check_password_hash

# mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'tinayang'
# app.config['MYSQL_DATABASE_DB'] = 'TradingSys'
# app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
# mysql.init_app(app)

connection=mc.connect(user='root',
    password='tinayang',
    host='127.0.0.1',
    database='TradingSys',
    auth_plugin='mysql_native_password')

@app.route('/')
def main():
    print('in main')
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    print('in showsignup')
    return render_template('signup.html')


@app.route('/signUp',methods=['POST','GET'])
def signUp():
    print('in signup')
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']
        print(_name)
        print(_email)
        print(_password)

        # validate the received values
        if (_name is not None) and (_email is not None) and (_password is not None):
            
            # All Good, let's call MySQL
            
            print('in if')
            cursor = connection.cursor()
            # _hashed_password = generate_password_hash(_password)
            # cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
            # data = cursor.fetchall()

            # if len(data) is 0:
            #     conn.commit()
            #     return json.dumps({'message':'User created successfully !'})
            # else:
            #     return json.dumps({'error':str(data[0])})
            cursor.close() 
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})
        
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        connection.close()
    
    return render_template('index.html')

if __name__ == "__main__":
    app.run(port=5002)
