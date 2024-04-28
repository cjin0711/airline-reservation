#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
from datetime import datetime
import pymysql.cursors

#Initialize the app from Flask
app = Flask(__name__)
# Lets Flask connect the CSS to the HTML 
app.static_folder = 'static'

#Configure MySQL. For mine port is 3306 and no password 
conn = pymysql.connect(host='localhost',
					   port = 3306,
                       user='root',
                       password='',
                       db='airline reservation',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Define a route for home page
@app.route('/')
def home():
	return render_template('index.html')

#Define route for customer login
@app.route('/customer_login')
def customer_login():
	return render_template('customer_login.html')

#Define route for customer register
@app.route('/customer_register')
def customer_register():
	return render_template('customer_register.html')

#Define route for staff login
@app.route('/staff_login')
def staff_login():
	return render_template('staff_login.html')

#Define route for staff register
@app.route('/staff_register')
def staff_register():
	return render_template('staff_register.html')

#Authenticates the login for Customers 
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
	#grabs information from the forms
	email = request.form['email']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM Customer WHERE email = %s and the_password = %s'
	cursor.execute(query, (email, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['email'] = email
		return redirect(url_for('home'))
		#return render_template('customer)
	else:
		#returns an error message to the html page
		error = 'Invalid login information'
		return render_template('customer_login.html', error=error)

#Authenticates the registration for Customers
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
	#grabs information from the forms
	email = request.form['email']
	password = request.form['password']
	first_name = request.form['first_name']
	last_name = request.form['last_name']
	building_num = request.form['building_num']
	street = request.form['street']
	apt_num = request.form['apt_num']
	city = request.form['city']
	the_state = request.form['state']
	zip_code = request.form['zip-code']
	passport_num = request.form['pass_num']
	passport_expiration = request.form['pass_exp']
	pass_country = request.form['pass_country']
	dob = request.form['dob']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM Customer WHERE email = %s'
	cursor.execute(query, (email))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('customer_register.html', error = error)
	else:
		ins = 'INSERT INTO Customer VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
		cursor.execute(ins, (email, password, first_name, last_name, building_num, street, apt_num, city, the_state, zip_code, passport_num, passport_expiration, pass_country, dob))
		conn.commit()
		cursor.close()
		return render_template('index.html')

#Authenticates the login for Staff
@app.route('/loginAuthStaff', methods=['GET', 'POST'])
def loginAuthStaff():
	#grabs information from the forms
	username = request.form.get('username')
	password = request.form.get('password')

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM Airline_Staff WHERE username = %s and the_password = %s'
	cursor.execute(query, (username, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = username
		return redirect(url_for('home'))
	else:
		#returns an error message to the html page
		error = 'Invalid login information'
		return render_template('staff_login.html', error=error)

#Authenticates the registration for Customers
@app.route('/registerAuthStaff', methods=['GET', 'POST'])
def registerAuthStaff():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']
	first_name = request.form['first_name']
	last_name = request.form['last_name']
	dob = request.form['dob']
	airline_name = request.form['airline_name']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM airline_staff WHERE username = %s'
	cursor.execute(query, (username))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('staff_register.html', error = error)
	else:
		ins = 'INSERT INTO airline_staff VALUES(%s, %s, %s, %s, %s, %s)'
		cursor.execute(ins, (username, password, first_name, last_name, dob, airline_name))
		conn.commit()
		cursor.close()
		return render_template('index.html')


@app.route('/flights', methods=['GET', 'POST'])
def flights():
	selected = request.form.get('flight_type')
	source = request.form['source']
	destination = request.form['destination']
	depart_date = request.form['departure_date']
	return_date = request.form.get('return_date')

	#convert from string to date type
	depart_dated = datetime.strptime(depart_date, '%Y-%m-%d').date()
	return_dated = datetime.strptime(return_date, '%Y-%m-%d').date()

	cursor = conn.cursor()

	"""
	#remove arrival_time, depart_airport, arrival_airport later
	leaving = '''SELECT flight_status, airline_name, flight_number, depart_date, arrival_date, arrival_time, depart_airport, arrival_airport
				 FROM flight 
				 WHERE (depart_date > CURDATE() OR (depart_date = CURDATE() AND depart_time > CURTIME())) AND 
				 depart_airport = %s AND arrival_airport = %s'''
	"""
	leaving = '''SELECT flight_status, airline_name, flight_number, depart_date, arrival_date, arrival_time, depart_airport, arrival_airport
				 FROM flight 
				 WHERE depart_date = %s AND (depart_date > CURDATE() OR (depart_date = CURDATE() AND depart_time > CURTIME())) AND 
				 depart_airport = %s AND arrival_airport = %s'''

	cursor.execute(leaving, (depart_dated, source, destination))
		
	#look for all future flights with specified time and airports
	leaving_data = cursor.fetchall()

	#one way trip chosen
	if selected == 'one-way':

		cursor.close()

		#if there are returned results
		if leaving_data:
			#print("Number of Flights: " + str(len(flight_data)))
			#for i in flight_data:
			#	print(i)
			return render_template('flights.html', flights = leaving_data, trip = "one-way")
		
		#if there are no results
		else:
			none_found = "No Available Flights Found."
			return render_template('flights.html', nothing = none_found)
	
	#round trip chosen
	else:
		#return flight is after departure flight (same day return flight is tackled below)
		returning = '''SELECT flight_status, airline_name, flight_number, depart_date, arrival_date, arrival_time, depart_airport, arrival_airport
					   FROM flight 
					   WHERE depart_date = %s AND depart_airport = %s AND arrival_airport = %s'''

		#source and destination flipped for return flight
		cursor.execute(returning, (return_dated, destination, source))

		returning_data = cursor.fetchall()

		round_trips = []
		
		#compare each going flight with each return flight to check if compatible
		for i in leaving_data:
			for j in returning_data:
				#edge case: if same day round trip, but departure time of return flight is earlier than arrival time of going flight
				if (i['arrival_date'] == j['depart_date']) and (i['arrival_time'] <= j['depart_time']):
					pass
				#if return flight occurs after arrival of going flight
				elif i['arrival_date'] < j['depart_date']:
					round_trips.append((i, j))

		if not round_trips:
			none_found = "No Available Flights Found."
			return render_template('flights.html', nothing = none_found)
		
		return render_template('flights.html', flights = round_trips, trip = "round-trip")

	
	
	
	  
	  					
@app.route('/logout')
def logout():
	session.pop('email')
	return redirect('/')



		
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)