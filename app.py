from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_session import Session

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret'
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)

socketio = SocketIO(app, manage_session=False)


@app.route('/', methods=['GET', 'POST'])    
def index():
    return render_template('index.html')

@app.route('/teacher', methods=['GET', 'POST'])
def teacher():
    if(request.method=='POST'):
        username = "Teacher"
        room = 6061
        #Store the data in session
        session['username'] = username
        session['room'] = room
        return render_template('index2.html', session = session,name="Teacher")
    else:
        if(session.get('username') is not None):
            return render_template('index2.html', session = session,name="Teacher")
        else:
            return redirect(url_for('index'))


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if(request.method=='POST'):
        username = "Admin"
        room = 6061
        #Store the data in session
        session['username'] = username
        session['room'] = room
        
        return render_template('chat.html', session = session,name="Admin")
        
    else:
        if(session.get('username') is not None):
            return render_template('chat.html', session = session,name="Admin")
        else:
            return redirect(url_for('index'))

@app.route('/student', methods=['GET', 'POST'])
def student():
    if(request.method=='POST'):
        username = "Student"
        room = 6061
        #Store the data in session
        session['username'] = username
        session['room'] = room
        return render_template('chat.html', session = session,name="Student")
        
    else:
        if(session.get('username') is not None):
            return render_template('chat.html', session = session,name="Student")
        else:
            return redirect(url_for('index'))

@socketio.on('join', namespace='/chat')
def join(message):
    room = session.get('room')
    join_room(room)
    emit('status', {'msg':  session.get('username') + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    room = session.get('room')
    emit('message', {'msg': session.get('username') + ' : ' + message['msg']}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    room = session.get('room')
    username = session.get('username')
    leave_room(room)
    session.clear()
    emit('status', {'msg': username + ' has left the room.'}, room=room)


if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0', port=5000)