import os
import sys
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask.ext.cors import CORS, cross_origin
from datetime import datetime

app = Flask(__name__)
# connect to SQL database with username, password and address
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

class Users(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Text)
	address = db.Column(db.Text)

	def __init__(self, name, address):
		self.name = name
		self.address = address

	def __repr__(self):
		return '<name %r>' % self.name

# Normal HTML landing page
@app.route('/')
def homepage():
	the_time = datetime.now()

	return """
	<h1>Hellow World</h1>
	<p>It is currently {time}.</p>
	""".format(time=the_time)

# Define HTTP API endpoint for external connections from web/mobile apps
@app.route('/user', methods = ['GET'])
@cross_origin()
def get_user():
	print("Loading data file into database...")
	for line in open('data_file.csv'):
		name, address = line.split(',')
		new_user = Users(name, address)
		db.session.add(new_user)

	db.session.commit()
	print("Data commited to database.")

	user_id = request.args.get('user_id')
	user = Users.query.filter_by(id=int(user_id)).first().__dict__
	print(user)

	user_json = {
		name: user['name'],
		address: user['address']
	}
	
	return jsonify(user=user_json)

if __name__ == '__main__':

	print("Starting Python web server")
	app.run(debug=True, use_reloader=True)



