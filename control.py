from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

# Initialize the app from Flask
app = Flask(__name__)

# Configure MySQL
conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='root',
                       password='',
                       db='introduction_to_databases',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)


# Define a route to hello function
@app.route('/')
def hello():
    return render_template('index.html')
  
@app.route('/future_flights',  methods = ['GET', 'POST'])
def future_flights():
    # source_city = request.form['source_city']
    source_airport = request.form['source_airport']
    # destination_city = request.form['destination_city']
    destination_airport = request.form['destination_airport']

    cursor = conn.cursor()
    query = 'SELECT * FROM flight WHERE (departure_date > CURDATE() or (departure_date = CURDATE() and departure_time > CURTIME())) and departure_airport = %s and arrival_airport = %s'
    cursor.execute(query, (source_airport, destination_airport))
    data = cursor.fetchall()
    cursor.close()
    return render_template('index.html', flights = data)

# Define a route to flight_status function.
@app.route('/flight_status', methods = ['GET', 'POST'])
def flight_status():
    airline_name = request.form['airline_name']
    flight_number = request.form['flight_number']
    arrival = request.form['arrival']
    departure = request.form['departure']

    cursor = conn.cursor()
    query = 'SELECT status FROM flight WHERE airline_name = %s and flight_number = %s and arrival_date = %s and departure_date = %s'
    cursor.execute(query, (airline_name, flight_number, arrival, departure))
    data = cursor.fetchall()
    cursor.close()
    return render_template('index.html', status = data)


# Define route for customer login
@app.route('/customer_login')
def customer_login():
    return render_template('customer_login.html')


# Define route for customer register
@app.route('/customer_register')
def customer_register():
    return render_template('customer_register.html')


# Authenticates the customer login
@app.route('/customer_loginAuth', methods=['GET', 'POST'])
def customer_loginAuth():
    # grabs information from the forms
    email = request.form['email']
    password = request.form['password']

    # cursor used to send queries
    cursor = conn.cursor()
    # executes query
    query = 'SELECT * FROM customer WHERE email = %s and password = md5(%s)'
    cursor.execute(query, (email, password))
    # stores the results in a variable
    data = cursor.fetchone()
    # use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if (data):
        # creates a session for the the user
        # session is a built in
        session['email'] = email
        return redirect(url_for('customer_home'))
    else:
        # returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('customer_login.html', error=error)


# # Authenticates the customer register
@app.route('/customer_registerAuth', methods=['GET', 'POST'])
def customer_registerAuth():
    # grabs information from the forms
    email = request.form['email']
    name = request.form['name']
    password = request.form['password']
    buil_num = request.form['building_number']
    street = request.form['street']
    city = request.form['city']
    state = request.form['state']
    phone_number = request.form['phone_number']
    passport_number = request.form['passport_number']
    expiration_dat = request.form['expiration_date']
    passport_country = request.form['passport_country']
    date_of_birth = request.form['date_of_birth']

    # cursor used to send queries
    cursor = conn.cursor()
    # executes query
    query = 'SELECT * FROM customer WHERE email = %s'
    cursor.execute(query, (email))
    # stores the results in a variable
    data = cursor.fetchone()
    # use fetchall() if you are expecting more than 1 data row
    error = None
    if (data):
        # If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('customer_register.html', error=error)
    else:
        ins = 'INSERT INTO customer VALUES(%s, %s, md5(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(ins, (email, name, password, buil_num, street, city, state, phone_number, passport_number, expiration_dat, passport_country, date_of_birth))
        conn.commit()
        cursor.close()
        return render_template('index.html')


@app.route('/customer_home')
def customer_home():
    email = session['email']
    cursor = conn.cursor();
    query = 'SELECT * FROM customer WHERE email = %s'
    cursor.execute(query, (email))
    data1 = cursor.fetchall()
    for each in data1:
        print(each['email'])
    cursor.close()
    return render_template('customer_home.html', email=email)


# Define route for airline staff login
@app.route('/airline_staff_login')
def airline_staff_login():
    return render_template('airline_staff_login.html')


# Define route for airline staff register
@app.route('/airline_staff_register')
def airline_staff_register():
    return render_template('airline_staff_register.html')


# Authenticates the airline staff login
@app.route('/airline_staff_loginAuth', methods=['GET', 'POST'])
def airline_staff_loginAuth():
    # grabs information from the forms
    username = request.form['username']
    password = request.form['password']

    # cursor used to send queries
    cursor = conn.cursor()
    # executes query
    query = 'SELECT * FROM airline_staff WHERE username = %s and password = md5(%s)'
    cursor.execute(query, (username, password))
    # stores the results in a variable
    data = cursor.fetchone()
    # use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if (data):
        # creates a session for the the user
        # session is a built in
        session['username'] = username
        return redirect(url_for('airline_staff_home'))
    else:
        # returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('airline_staff_login.html', error=error)


# Authenticates the airline staff register
@app.route('/airline_staff_registerAuth', methods=['GET', 'POST'])
def airline_staff_registerAuth():
    # grabs information from the forms
    username = request.form['username']
    airline_name = request.form['airline_name']
    password = request.form['password']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    date_of_birth = request.form['date_of_birth']

    # cursor used to send queries
    cursor = conn.cursor()
    # executes query
    query = 'SELECT * FROM airline_staff WHERE username = %s'
    cursor.execute(query, (username))
    # stores the results in a variable
    data = cursor.fetchone()
    # use fetchall() if you are expecting more than 1 data row
    error = None
    if (data):
        # If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('airline_staff_register.html', error=error)
    else:
        ins = 'INSERT INTO airline_staff VALUES(%s, %s, md5(%s), %s, %s, %s)'
        cursor.execute(ins, (username, airline_name, password, first_name, last_name, date_of_birth))
        conn.commit()
        cursor.close()
        return render_template('index.html')


@app.route('/airline_staff_home', methods=['GET', 'POST'])
def airline_staff_home():
    username = session['username']
    cursor = conn.cursor();
    query = 'SELECT * FROM airline_staff WHERE username = md5(%s)'
    cursor.execute(query, (username))
    data1 = cursor.fetchall()
    for each in data1:
        print(each['username'])
    cursor.close()
    return render_template('airline_staff_home.html', username=username)
  
#################################################################################################################

# Define route for airline staff add flight
@app.route('/airline_staff_view_flights')
def airline_staff_view_flights():
    return render_template('airline_staff_view_flights.html')


@app.route('/airline_staff_view_flights_next_month')
def airline_staff_view_flights_next_month():
    username = session['username']
    cursor = conn.cursor()
    query = 'SELECT * FROM flight, airline_staff WHERE airline_staff.username = %s and flight.airline_name = airline_staff.airline_name and (departure_date < CURRENT_DATE + 30 or (departure_date = CURRENT_DATE + 30 and departure_time < CURRENT_TIME))'
    cursor.execute(query, (username))
    data = cursor.fetchall()
    cursor.close()
    return render_template('airline_staff_view_flights_next_month.html', flight=data)


# Define route for airline staff flights custom date range
@app.route('/airline_staff_view_flights_custom_date_range')
def airline_staff_view_flights_custom_date_range():
    return render_template('airline_staff_view_flights_custom_date_range.html')


@app.route('/view_flights_custom_date_range', methods=['GET', 'POST'])
def view_flights_custom_date_range():
    username = session['username']
    departure_date_start = request.form['departure_date_start']
    departure_date_end = request.form['departure_date_end']

    cursor = conn.cursor()
    query = 'SELECT * FROM flight, airline_staff WHERE airline_staff.username = %s and flight.airline_name = airline_staff.airline_name and departure_date BETWEEN %s AND %s'
    cursor.execute(query, (username, departure_date_start, departure_date_end))
    data = cursor.fetchall()
    cursor.close()
    return render_template('airline_staff_view_flights_custom_date_range.html', flight=data, username=username)


# Define route for airline staff view flights customers
@app.route('/airline_staff_view_flights_customers')
def airline_staff_view_flights_customers():
    return render_template('airline_staff_view_flights_customers.html')


@app.route('/view_flights_customers', methods=['GET', 'POST'])
def view_flights_customers():
    username = session['username']
    flight_number = request.form['flight_number']
    departure_date = request.form['departure_date']
    departure_time = request.form['departure_time']
    cursor = conn.cursor()
    query = 'SELECT name_on_card as name FROM ticket, airline_staff WHERE airline_staff.username = %s and ticket.airline_name = airline_staff.airline_name and flight_number = %s and departure_date = %s and departure_time = %s'
    cursor.execute(query, (username, flight_number, departure_date, departure_time))
    data = cursor.fetchall()
    cursor.close()
    return render_template('airline_staff_view_flights_customers.html', ticket=data)
  
  
# Define route for airline staff add flight
@app.route('/add_flight')
def airline_staff_add_flight():
    return render_template('airline_staff_add_flight.html')


# Authenticates the airline staff add flight
@app.route('/airline_staff_add_flightAuth', methods=['GET', 'POST'])
def airline_staff_add_flightAuth():
    # grabs information from the forms
    username = session['username']
    flight_number = request.form['flight_number']
    departure_date = request.form['departure_date']
    departure_time = request.form['departure_time']
    # airline_name = request.form['airline_name']
    airport_name = request.form['airport_name']
    airplane_id = request.form['airplane_id']
    airplane_owner_name = request.form['airplane_owner_name']
    departure_airport = request.form['departure_airport']
    arrival_airport = request.form['arrival_airport']
    arrival_time = request.form['arrival_time']
    arrival_date = request.form['arrival_date']
    base_price = request.form['base_price']
    status = request.form['status']

    # cursor used to send queries
    cursor = conn.cursor()

    airline_name = 'SELECT airline_name FROM airline_staff WHERE airline_staff.username = %s'
    cursor.execute(airline_name, (username))
    airline_name_ = cursor.fetchone()
    airline_name_ = airline_name_['airline_name']
    # executes query
    query = 'SELECT * FROM flight WHERE flight_number = %s and departure_date = %s and departure_time = %s and airline_name = %s'
    cursor.execute(query, (flight_number, departure_date, departure_time, airline_name_))
    # stores the results in a variable
    data = cursor.fetchone()
    # use fetchall() if you are expecting more than 1 data row
    error = None
    if (data):
        # If the previous query returns data, then user exists
        error = "This flight already exists"
        return render_template('add_flight.html', error=error)
    else:
        ins = 'INSERT INTO flight VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(ins, (
            flight_number, departure_date, departure_time, airline_name_, airport_name, airplane_id, airplane_owner_name,
            departure_airport, arrival_airport, arrival_time, arrival_date, base_price, status))
        conn.commit()
        cursor.close()
        return render_template('airline_staff_home.html')


# Define route for airline staff change flight status
@app.route('/airline_staff_change_flight_status')
def airline_staff_change_flight_status():
    return render_template('airline_staff_change_flight_status.html')


@app.route('/change_status', methods=['GET', 'POST'])
def change_status():
    status = request.form['status']
    flight_number = request.form['flight_number']
    departure_date = request.form['departure_date']
    departure_time = request.form['departure_time']
    airline_name = request.form['airline_name']

    cursor = conn.cursor()
    query = 'UPDATE flight SET status = %s WHERE flight_number = %s and departure_date = %s and departure_time = %s and airline_name = %s'
    cursor.execute(query, (status, flight_number, departure_date, departure_time, airline_name))
    data = cursor.fetchall()
    conn.commit()
    cursor.close()
    return render_template('airline_staff_home.html', flight=data)
      

@app.route('/add_airplane')
def airline_staff_add_airplane():
    return render_template('airline_staff_add_airplane.html')

@app.route('/airline_staff_add_airplaneAuth', methods=['GET', 'POST'])
def airline_staff_add_airplaneAuth():

    username = session['username']

    id = request.form['ID']
    capacity = request.form['capacity']
    manufacturer = request.form['manufacturer']
    manufactured_date = request.form['manufactured_date']

    cursor = conn.cursor()
    
    query = 'SELECT * FROM airplane, airline_staff WHERE airline_staff.username = %s and id = %s and airplane.airline_name = airline_staff.airline_name and capacity = %s and manufacturer = %s and manufactured_date = %s'
    cursor.execute(query, (username, id, capacity, manufacturer, manufactured_date))
    data = cursor.fetchone()
    error = None
    if (data):
        error = "This plane already exists"
        return render_template('airline_staff_add_airplane.html', error=error)
    else:
        airline_name_query = 'SELECT airline_name FROM airline_staff WHERE username = %s'
        cursor.execute(airline_name_query, username)
        airline_name = cursor.fetchone()
        airline_name = airline_name['airline_name']
        print(airline_name)
        ins = 'INSERT INTO airplane VALUES(%s, %s, %s, %s, %s)'
        cursor.execute(ins, (id, airline_name, capacity, manufacturer, manufactured_date))
        all_airplanes = 'SELECT * FROM airline_staff as staff, airplane WHERE username = %s and staff.airline_name = airplane.airline_name'
        cursor.execute(all_airplanes, (session['username']))
        data = cursor.fetchall()
        conn.commit()
        cursor.close()
        return render_template('airline_staff_add_airplane.html', airplanes = data)

@app.route('/add_airport')
def airline_staff_add_airport():
    return render_template('airline_staff_add_airport.html')

@app.route('/airline_staff_add_airportAuth', methods=['GET', 'POST'])
def airline_staff_add_airportAuth():
    
    name = request.form['Name']
    city = request.form['City']
    country = request.form['Country']
    airport_type = request.form['airport_type']

    cursor = conn.cursor()

    query = 'SELECT * FROM airport WHERE name = %s and city = %s and country = %s and airport_type = %s'
    cursor.execute(query, (name, city, country, airport_type))
    data = cursor.fetchone()
    error = None
    if (data):
        error = "This airport already exists"
        return render_template('airline_staff_add_airport.html', error=error)
    else:
        ins = 'INSERT INTO airport VALUES(%s, %s, %s, %s)'
        cursor.execute(ins, (name, city, country, airport_type))
        show_all = 'SELECT * FROM airport'
        cursor.execute(show_all)
        data = cursor.fetchall()
        conn.commit()
        cursor.close()
        return render_template('airline_staff_add_airport.html', airports = data)
      
@app.route('/view_flight_ratings')
def airline_staff_check_flight_ratings():
    return render_template('airline_staff_flight_rating.html')

@app.route('/airline_staff_check_flight_ratings', methods = ['GET', 'POST'])
def check_flight_ratings():
    username = session['username']

    flight_number = request.form['flight_number']
    departure_date = request.form['departure_date']
    departure_time = request.form['departure_time']

    cursor = conn.cursor()
    airline_name_query = 'SELECT airline_name FROM airline_staff WHERE username = %s'
    cursor.execute(airline_name_query, username)
    airline_name = cursor.fetchone()
    airline_name = airline_name['airline_name']
    # Gets all the ratings of a flight 
    ratings = 'SELECT rate, comment FROM flown WHERE flight_number = %s and departure_date = %s and departure_time = %s and airline_name = %s'
    cursor.execute(ratings, (flight_number, departure_date, departure_time, airline_name))
    flight_ratings = cursor.fetchall()
    # Calculates the average rating of that specifc flight
    average = 'SELECT AVG(rate) as average_rate FROM flown, airline_staff WHERE airline_staff.username = %s and airline_staff.airline_name = flown.airline_name'
    cursor.execute(average, username)
    the_average = cursor.fetchone()
    cursor.close()
    error = None
    if (rating):
        return render_template('airline_staff_flight_rating.html', all_ratings = flight_ratings, average = the_average, username = username, error = error)
    else:
        error = 'Flight Does Not Exist'
        return render_template('airline_staff_flight_rating.html', username = username, error=error)
      

@app.route('/view_frequent_customers')
def airline_staff_view_frequent_customers():
    return render_template('airline_staff_frequent_customers.html')
    
@app.route('/airline_staff_frequent_customers', methods = ['GET', 'POST'])
def find_most_frequent_customer():
    username = username['username']
    cursor = conn.cursor()
    query = 'SELECT email, COUNT(*) FROM ticket WHERE departure_date > current_date - interval 1 year and departure_date <= current_date GROUP BY email '
    cursor.execute(query)
    frequent = cursor.fetchall()
    cursor.close()
    return render_template('airline_staff_frequent_customers.html', customers = frequent)


# Define route for airline staff view reports
@app.route('/airline_staff_view_reports')
def airline_staff_view_reports():
    username = session['username']
    return render_template('airline_staff_view_reports.html', username=username)


@app.route('/airline_staff_view_reports_last_month')
def airline_staff_view_reports_last_month():
    username = session['username']
    cursor = conn.cursor()
    query = 'SELECT COUNT(*) as lastmonth FROM ticket, airline_staff WHERE airline_staff.username = %s and ticket.airline_name = airline_staff.airline_name and ticket.purchase_date > CURDATE() - interval 30 day'
    cursor.execute(query, (username))
    data = cursor.fetchall()
    cursor.close()
    return render_template('airline_staff_view_reports_last_month.html', ticket=data, username=username)


@app.route('/airline_staff_view_reports_last_year')
def airline_staff_view_reports_last_year():
    username = session['username']
    cursor = conn.cursor()
    query = 'SELECT COUNT(*) as lastyear FROM ticket, airline_staff WHERE airline_staff.username = %s and ticket.airline_name = airline_staff.airline_name and ticket.purchase_date > CURDATE() - interval 365 day'
    cursor.execute(query, (username))
    data = cursor.fetchall()
    cursor.close()
    return render_template('airline_staff_view_reports_last_year.html', ticket=data, username=username)


# Define route for airline staff view reports custom date range
@app.route('/airline_staff_view_reports_custom_date_range')
def airline_staff_view_reports_custom_date_range():
    username = session['username']
    return render_template('airline_staff_view_reports_custom_date_range.html', username=username)


@app.route('/view_reports_custom_date_range', methods=['GET', 'POST'])
def view_reports_custom_date_range():
    username = session['username']
    purchase_date_start = request.form['purchase_date_start']
    purchase_date_end = request.form['purchase_date_end']

    # cursor used to send queries
    cursor = conn.cursor()

    # query = 'SELECT count(DISTINCT ID) FROM ticket'
    query = 'SELECT COUNT(*) as daterange FROM ticket, airline_staff WHERE airline_staff.username = %s and ticket.airline_name = airline_staff.airline_name and purchase_date BETWEEN %s AND %s'
    cursor.execute(query, (username, purchase_date_start, purchase_date_end))
    data = cursor.fetchall()
    cursor.close()
    return render_template('airline_staff_view_reports_custom_date_range.html', ticket=data, username=username)
  

  
@app.route('/airline_staff_view_revenue')
def airline_staff_view_revenue():
    return render_template('/airline_staff_view_revenue.html')

@app.route('/view_revenue_last_month')
def airline_staff_view_revenue_last_month():
    return render_template('/airline_staff_view_revenue_last_month.html')

@app.route('/find_revenue_last month', methods = ['GET', 'POST'])
def view_earned_revenue_last_month():
    username = session['username']
    cursor = conn.cursor()
    query = 'SELECT sum(sold_price) as revenue FROM ticket, airline_staff WHERE airline_staff.username = %s and airline_staff.airline_name = ticket.airline_name and purchase_date > CURRENT_DATE - interval 1 month'
    cursor.execute(query, username)
    data = cursor.fetchone()
    # print(data)
    cursor.close()
    return render_template('airline_staff_view_revenue_last_month.html', earned_revenue = data, username = username)

@app.route('/view_revenue_last_year')
def airline_staff_view_revenue_last_year():
    return render_template('/airline_staff_view_revenue_last_year.html')

@app.route('/find_revenue_last_year', methods = ['GET', 'POST'])
def view_earned_revenue_last_year():
    username = session['username']
    cursor = conn.cursor()
    query = 'SELECT sum(sold_price) as "revenue" FROM ticket, airline_staff WHERE airline_staff.username = %s and airline_staff.airline_name = ticket.airline_name and purchase_date > CURRENT_DATE - interval 1 year'
    cursor.execute(query, username)
    data = cursor.fetchone()
    cursor.close()
    return render_template('airline_staff_view_revenue_last_year.html', earned_revenue = data, username = username)
      

@app.route('/customer_logout')
def customer_logout():
    session.pop('email')
    return redirect('/')


@app.route('/airline_staff_logout')
def airline_staff_logout():
    session.pop('username')
    return redirect('/')
  
# Monte's Functions:

@app.route('/customer_viewmyflights')
def customer_viewmyflights():
    email = session['email']
    cursor = conn.cursor();
    query = 'SELECT * FROM ticket WHERE email = %s and (departure_date > CURRENT_DATE or (departure_date = CURRENT_DATE and departure_time > CURRENT_TIME))'
    cursor.execute(query, (email))
    data1 = cursor.fetchall()
    return render_template('customer_viewmyflights.html', tickets=data1, email=email)
  
@app.route('/upcoming_flights', methods=['GET', 'POST'])
def upcoming_flights():
    return render_template("upcoming_flights.html")
  
@app.route('/upcoming_flights_auth', methods=['GET', 'POST'])
def upcoming_flights_auth():
    email = session['email']
    d_port = request.form['Departure_Airport']
    a_port = request.form['Arrival_Airport']
    d_date= request.form['Departure_Date']
    a_date = request.form['Arrival_Date']
    if not a_date:
        cursor = conn.cursor();
        query = 'SELECT * FROM flight WHERE departure_date = %s and arrival_airport = %s and departure_airport = %s'
        cursor.execute(query, (d_date, a_port, d_port))
        data1 = cursor.fetchall()
        if (data1):
            return render_template('upcoming_flights.html', flights=data1)
        else:
            error = "No Upcoming Flights Matching Description"
            return render_template('customer_home.html', error=error)
    else:
        cursor = conn.cursor();
        query = 'SELECT * FROM flight WHERE departure_date = %s and arrival_airport = %s and departure_airport = %s'
        cursor.execute(query, (d_date, a_port, d_port))
        data1 = cursor.fetchall()
        query = 'SELECT * FROM flight WHERE arrival_date = %s and arrival_airport = %s and departure_airport = %s'
        cursor.execute(query, (a_date, d_port, a_port))
        data2 = cursor.fetchall()
        if data1 and data2:
            return render_template('upcoming_twoways.html', username = email, flights = data1, returns=data2)
        else:
            error = "No Upcoming Flights Matching Description"
            return render_template('customer_home.html', error=error)

MAX_TICKET_NUM = 99999999
ticket_number = {"num": 0}

@app.route('/buy_flights', methods=['GET', 'POST'])
def buy_flights():
    # grabs information from the forms
    email = session['email']
    flight_num = request.form['flight_num']
    cursor = conn.cursor();
    query = 'SELECT * FROM flight WHERE flight_number = %s and (departure_date > CURRENT_DATE or (departure_date = CURRENT_DATE and departure_time > CURRENT_TIME))'
    cursor.execute(query, (flight_num))
    data1 = cursor.fetchall()
    if data1:
        data1 = data1[0]
        query = 'SELECT count(*) AS "flyers" FROM ticket WHERE flight_number = %s'
        cursor.execute(query, (flight_num))
        data2 = cursor.fetchall()
        query = 'SELECT * FROM airplane WHERE ID = %s'
        cursor.execute(query, (data1["airplane_id"]))
        data3 = cursor.fetchall()
        flyers=data2[0]["flyers"]
        if ticket_num["num"]>MAX_TICKET_NUM:
          ticket_num["num"]=0
        cap = data3[0]["capacity"]
        if flyers>cap:
            conn.commit()
            cursor.close()
            error = "Not enough room in the flight"
            return render_template('upcoming_flights.html', error=error)
        cost = data1["base_price"]
        if flyers / cap > .60:
            cost = int(cost)
            cost *= 1.25
        departure_date = data1["departure_date"]
        departure_time = data1["departure_time"]
        airline_name = data1["airline_name"]
        card_type = request.form['card_type']
        card_num = request.form['card_num']
        name_card = request.form['name_on_card']
        card_exp = request.form["card_exp"]
        ins = "INSERT INTO ticket VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,CURRENT_DATE,CURRENT_TIME)"
        cursor.execute(ins, (ticket_number["num"], flight_num, departure_date,departure_time, airline_name, email, cost, card_type, card_num, name_card, card_exp))
        conn.commit()
        cursor.close()
        return render_template('customer_home.html')
    else:
        error = "Flight does not exist"
        return render_template('upcoming_flights.html', error=error)


@app.route('/cancel_trip', methods=['GET', 'POST'])
def cancel_trip():
    return render_template('cancel_trip.html')

@app.route('/cancel_trip_auth', methods=['GET', 'POST'])
def cancel_trip_auth():
    email = session['email']
    ticket_ID = request.form["Ticket_ID"]
    cursor = conn.cursor();
    query = 'SELECT * FROM ticket WHERE email = %s and departure_date > CURRENT_DATE and ID = %s'
    cursor.execute(query, (email, ticket_ID))
    data1 = cursor.fetchall()

    if data1:
        dele = 'DELETE FROM ticket WHERE ID = %s'
        cursor.execute(dele, (ticket_ID))
        conn.commit()
        cursor.close()
        return render_template("customer_home.html")
    else:
        error = "You don't have that ticket"
        return render_template("cancel_trip.html", error=error)

@app.route('/rating', methods=['GET', 'POST'])
def rating():
    return render_template('rating.html')

@app.route('/rating_auth', methods=['GET', 'POST'])
def rating_auth():
    email = session['email']
    flight_num = request.form["flight_num"]
    rating = request.form["rating"]
    comment = request.form["comment"]
    cursor = conn.cursor();
    query = 'SELECT * FROM ticket WHERE email = %s and flight_number=%s and (departure_date < CURRENT_DATE or (departure_date = CURRENT_DATE and departure_time < CURRENT_TIME))'
    cursor.execute(query, (email, flight_num))
    data1 = cursor.fetchall()
    if data1:
        data1 = data1[0]
        ins = 'INSERT INTO flown VALUES(%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(ins, (email, flight_num, data1["departure_date"], data1["departure_time"], rating, comment, data1["airline_name"]))
        conn.commit()
        cursor.close()
        return render_template("customer_home.html")
    else:
        error = "You did not take this flight"
        return render_template("rating.html", error=error)
      
MONTH_DICT = {"01": "January", "02": "February", "03": "March", "04": "April", "05": "May", "06": "June", "07": "July",
              "08": "August", "09": "September", "10": "October", "11": "November", "12": "December"}
@app.route('/track_spending', methods=['GET', 'POST'])
def track_spending():
    email = session['email']
    cursor = conn.cursor();
    query = 'SELECT * FROM ticket WHERE email = %s and purchase_date > CURDATE() - interval 6 month'
    cursor.execute(query, (email))
    data1 = cursor.fetchall()
    if data1:
        query = 'SELECT sum(sold_price) AS "total" FROM ticket WHERE email = %s and purchase_date > CURDATE() - interval 365 day'
        cursor.execute(query, (email))
        data2 = cursor.fetchall()
        total = data2[0]["total"]
        monthly_spending = {}
        for val in data1:
            cur_month = str(val["purchase_date"])[5:7]
            month = MONTH_DICT[cur_month]
            if month in monthly_spending:
                monthly_spending[month] += int(val["sold_price"])
            else:
                monthly_spending[month] = int(val["sold_price"])
        print(monthly_spending)
        conn.commit()
        cursor.close()
        return render_template("track_spending.html", total=total, monthly_spending=monthly_spending, email=email)
    else:
        conn.commit()
        cursor.close()
        total = "No money spent"
        return render_template("track_spending.html", total=total, email=email)


@app.route('/track_spending_range', methods=['GET', 'POST'])
def track_spending_range():
    return render_template("track_spending_range.html")


@app.route('/track_spending_range_auth', methods=['GET', 'POST'])
def track_spending_range_auth():
    email = session['email']
    cursor = conn.cursor();
    start = request.form["start"]
    end = request.form["end"]
    query = 'SELECT * FROM ticket WHERE email = %s and purchase_date BETWEEN %s AND %s'
    cursor.execute(query, (email, start, end))
    data1 = cursor.fetchall()
    if data1:
        query = 'SELECT sum(sold_price) as "total" FROM ticket WHERE BETWEEN %s AND %s'
        cursor.execute(query, (email, start, end))
        data2 = cursor.fetchall()
        total = data2[0]["total"]
        monthly_spending = {}
        for val in data1:
            cur_month = str(val["purchase_date"])[5:7]
            month = MONTH_DICT[cur_month]
            if month in monthly_spending:
                monthly_spending[month] += int(val["sold_price"])
            else:
                monthly_spending[month] = int(val["sold_price"])
        return render_template("track_spending_range.html", total=total, monthly_spending=monthly_spending, email=email)
    else:
        error = "No money spent in that range"
        return render_template("track_spending_range.html", error=error, email=email)

app.secret_key = 'some key that you will never guess'
# Run the app on localhost port 5000
# debug = True -> you don't have to restart flask
# for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True)
