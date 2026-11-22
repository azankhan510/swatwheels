from operator import add

from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3
import os
from database import add_car_db
from database import get_all_cars, get_connection
from database import add_user , get_user
app = Flask(__name__)
app.secret_key = "swatwheels123"

users_list = []
cars_list = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def registaration():
    if request.method == 'POST':
        acc_type = int(request.form['acc_type'])
        if acc_type == 1:
            username = request.form['username']
            cnic = request.form['cnic']
            email = request.form['email']
            phone = request.form['phone']
            password = request.form['password']
            bio = request.form ['bio']          
            add_user(username, cnic, email, phone, password, bio)
            return redirect ("/login")
        elif acc_type == 2:
            username = request.form['username']
            cnic = request.form['cnic']
            email = request.form['email']
            phone = request.form['phone']
            account_type = request.form['account_type']
            establishment_year = request.form['establishment_year']
            showroom_address = request.form['showroom_address']
            password = request.form['password']
            bio = request.form['bio']
            add_user = (username, cnic, email, phone, establishment_year,
                        showroom_address, account_type, password, bio,
                          "showroom")
            return redirect ("/login")
        
        else:
            return "invalid account type!"
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def loginuser():
    if request.method == 'POST':
        ec = request.form['cnic']
        ep = request.form['password']
        for i in users_list:
            if ec == i["cnic"] and ep == i["password"]:
                session['current_user'] = i
                return redirect(url_for('dashboard'))
        return "invalid username or password! <a href='/login'>Dobara</a>"
    return render_template('login.html')

def dashboard():
    if "user" not in session:
       return redirect("/login")

    return render_template ("dashboard.html", user=session.get("user"))


@app.route('/available car')
def view_available_cars():
    cars_list = get_all_cars()
    return render_template ("available_car.html", cars=cars_list)

@app.route('/search', methods = ['GET','POST'])
def search_cars():

    brand = request.args.get("brand","")
    engine_cc = request.args.get("engine_cc","")
    year = request.args.get("year","")
    model = request.args.get("model","")
    budget = request.args.get("budget","")
    fuel = request.args.get("fuel","")
    transmission = request.args.get("transmission","")

    print("===== SEARCH CARS =====")
    print("searching for :", brand)
    print("searching for :",engine_cc)
    print("searching for :", year)
    print("searching for :", model)
    print("searching for :", budget)
    print("searching for :",fuel)
    print("searching for:",transmission)

    return render_template ("search.html")

@app.route('/add_car', methods = ['get','post'])
def add_car():
    print("======ADD YOUR CAR======")

    if request.method == 'POST':
        brand = request.form['brand']
        engine_cc = request.form['engine_cc']
        year = request.form['year']
        model = request.form['model']
        fuel = request.form['fuel']
        price = request.form['price']
        transmission = request.form['transmission']
        condition = request.form['condition']
        milage = request.form['milage']
        location = request.form['location']

        owner = session.get ("user")
        add_car_db(brand, engine_cc, year, model, fuel, price, transmission, condition, milage, location)
        return redirect("/dashboard")

    return render_template("add_car.html")


@app.route("/my_listing")
def my_listing():
    print("===== MY CAR LISTINGS")

    if not cars_list:
        return "you have not added any car yet!"
        

    else:
        for car in cars_list:
            print("brand:", car ["brand"])
            print("engine_cc:", car ["engine_cc"])
            print("year:", car ["year"])
            print("model:", car ["model"])
            print("fuel:", car ["fuel"])
            print("price:", car ["price"])
            print("transmission:", car ["transmission"])
            print("condition:", car ["condition"])
            print("milage:", car ["milage"])
            print("location:", car ["location"])

        return render_template("my listing.html", car = cars_list)
    

@app.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    user = session.get('current_user')
    if not user:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        user['username'] = request.form['username']
        user['cnic'] = request.form['cnic']
        user['email'] = request.form['email']
        user['phone'] = request.form['phone']
        user['bio'] = request.form['bio']
        if 'establishment_year' in user:
            user['establishment_year'] = request.form['establishment_year']
            user['showroom_address'] = request.form['showroom_address']
        return redirect(url_for('dashboard'))
    
    return render_template('edit_profile.html', user=user)

def add_car_db(brand, engine_cc, year, model,fuel, price, transmission, condition , milage, location):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cars(brand, engine_cc, year, model, fuel, price, transmission, condition, milage, location)values(?,?,?,?,?,?)",
                   (brand, engine_cc, year, price, model, fuel, transmission, condition, milage, location))
    conn.commit()
    conn.close()

@app.route('/delete-car-listing/<int:id>', methods=['POST'])
def delete_car_listing(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM cars WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))

@app.route('/profile')
def profile():
    user = session.get('current_user')
    if not user:
        return redirect(url_for('loginuser'))
    return render_template('profile.html', user=user)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        confirm = request.form['confirm']
        if confirm == "y" or confirm == "Y":
            session.pop('current_user', None)
            return "you have been logout! <br><a href='/'>Home</a>"
        else:
            return "still logged in! <br><a href='/profile'>Profile</a>"
    return render_template('logout.html')


@app.route("/my profile")
def my_profile():
    user = session.get(user)
    if not user:
       return redirect ("/login")
    return render_template("my_profile.html", user = user)

@app.route("/update_profile", methods = ["GET" , "POST"])
def update_profile():

    user = session.get ("user")

    if not user :
        return redirect ("/login")
    return render_template("update_profile.html", user = user)



@app.route('/add_showroom', methods= ['GET', 'POST'])
def add_showroom():
    if request.method == 'POST':
        name = request.form ['name']
        owner_name = request.form ['owner_name']
        city = request.form ['city']
        location = request.form ['location']
        phone = request.form ['phone']

        conn = sqlite3.connect("swatwheels.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO showrooms(name, owner_name, city, location, phone) VALUES(?, ?, ?, ?, ?,)",
        (name, owner_name, city, location, phone))
        conn.commit()
        conn.close()
        return "showroom added!"
    return render_template ("add_showroom.html")

def save_image(file):
        if file and file.filename != '':
                 

            if __name__ == '__main__':
             port = int (os. environ.get('port',5000))
             app.run(host='0.0.0.0', port=port, debug= True)

