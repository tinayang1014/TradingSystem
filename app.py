from flask import Flask, render_template, json, request
# from flask_socketio import SocketIO, emit
# from werkzeug import generate_password_hash, check_password_hash
from random import random
# from time import sleep
# from threading import Thread, Event
# import Database, Socket



app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'
# socketio = SocketIO(app)

# #random number Generator Thread
# thread = Thread()
# thread_stop_event = Event()

# export FLASK_DEBUG=1

# db = Database.Database()

#####################################
###### Comment Out Before Run #######
# @app.before_first_request
# def activate_job():
#     # print("in activate_job")
#     def run_job(stock):
#         while True:
#             s = Socket.Socket(stock)
#             time.sleep(30)

#     for i in ["BTC-USD", "LTC-USD", "ETH-USD"]:
#         thread = Thread(target=run_job, args=(i,))
#         thread.start()

#####################################

@app.route('/')
def main():
    sym = db.get_data("select * from symbol")
    db.close()
    return render_template('index.html', symbol = sym)


@app.route('/signUp')
def signUp():
    return render_template('signUp.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/trade')
def trade():
    return render_template('trade.html')


@app.route('/portfolio')
def protfoilo():
    return render_template('protfolio.html')



# class RandomThread(Thread):
#     def __init__(self):
#         self.delay = 1
#         super(RandomThread, self).__init__()

#     def randomNumberGenerator(self):
#         """
#         Generate a random number every 1 second and emit to a socketio instance (broadcast)
#         Ideally to be run in a separate thread?
#         """
#         #infinite loop of magical random numbers
#         print("Making random numbers")
#         while not thread_stop_event.isSet():
#             number = round(random()*10, 3)
#             print(number)
#             socketio.emit('newnumber', {'number': number}, namespace='/test')
#             sleep(self.delay)

#     def run(self):
#         self.randomNumberGenerator()


# @socketio.on('connect', namespace='/test')
# def test_connect():
#     # need visibility of the global thread object
#     global thread
#     print('Client connected')

#     #Start the random number generator thread only if the thread has not been started before.
#     if not thread.isAlive():
#         print("Starting Thread")
#         thread = RandomThread()
#         thread.start()
#     Socket.Socket("BTC-USD")

# @socketio.on('disconnect', namespace='/test')
# def test_disconnect():
#     print('Client disconnected')

if __name__ == '__main__':
    app.run(threaded = True)
    # t = Thread(target=Socket.Socket, args=('BTC-USD'))
    # t.start()
    # socketio.run(app, debug=True)
    # # socket = Socket.Socket("BTC-USD")
    # wst = threading.Thread(target=Socket.Socket, args=("BTC-USD",))
    # wst.daemon = False
    # wst.start()