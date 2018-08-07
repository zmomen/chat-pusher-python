from flask import Flask, render_template, request, jsonify, make_response, json
from flask_cors import CORS
from pusher import pusher
import simplejson

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# configure pusher object
pusher = pusher.Pusher(
app_id='574024',
key='ed46e4b621ddf836602f',
secret='14cf8900bf3303333c2b',
cluster='us2',
ssl=True)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/admin')
def admin():
	return render_template('admin.html')

@app.route('/new/guest', methods=['POST'])
def guestUser():
	data = request.json
	pusher.trigger(u'general-channel', u'new-guest-details', { 
    	'name' : data['name'], 
	'email' : data['email']
	})
	return json.dumps(data)

@app.route("/pusher/auth", methods=['POST'])
def pusher_authentication():
	auth = pusher.authenticate(channel=request.form['channel_name'],socket_id=request.form['socket_id'])
	return json.dumps(auth)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
