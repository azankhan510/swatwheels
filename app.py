from operator import add, is_

from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3
import os
import time
from werkzeug.utils import secure_filename
from database import add_car_db
from database import get_all_cars, get_connection
from database import add_user , get_user
app = Flask(__name__)
app.secret_key = "swatwheels123"
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

users_list = []
cars_list = []

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
        if file and file.filename!= '':
            filename = secure_filename(file.filename)
            new_name = str(int(time.time())) + "_" + filename
            path = os.path.join(app.config['UPLOAD_FOLDER'], new_name)
            file.save(path)
            return "uploads/" + new_name
        return None

def update_profile_photo(user_id, file):
    path = save_image(file)
    if path:
            conn = sqlite3.connect('car_market.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET profile_photo = ? WHERE id = ?"(path,user_id))
            conn.commit()
            conn.close
            return True
    return False

def update_cover_photo(user_id, file):
            path =save_image(file)
            if path:
                conn = sqlite3.connect('car market.db')
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET cover_photo = ? WHERE id = ?", (path,user_id))
                conn.commit
                conn.close
                return True
            return False

def update_showroom_photo(showroom_id,file, is_cover=False):
            path = save_image(file)
            if path:
                conn = sqlite3.connect('car market.db')
                cursor = conn.cursor()
                if is_cover:
                    cursor.execute("UPDATE showrooms SET cover_photo = ? WHERE id = ?", (path, showroom_id))
                else:
                    cursor.execute("UPDATE showrooms SET showroom_photo = ?", (path, showroom_id))
                    conn.commit
                    conn.close
                    return True
                return False

def save_car_images(car_id, files):
            conn = sqlite3.connect('car_market.db')
            cursor = conn.cursor()
            for i, file in enumerate(file): 
                 path = save_image(file)
                 if path:
                    is_main = 1 if i == 0 else  0
                 cursor.execute("INSERT INTO car_images (car_id, image_path, is_main) VALUES(?,?,?)", (car_id, path, is_main)) 
                 conn.commit 
                 conn.close
                 return True

@app.route('/upload_profile', methods=['POST'])
def upload_profile():
    if 'user_id' not in session:
        return redirect('/login')
    file = request.files.get('profile_photo')
    update_profile_photo(session['user_id'], file)
    return redirect('/profile')


@app.route('/upload_cover', methods=['POST'])
def upload_cover():
    if 'user_id' not in session:
        return redirect('/login')
    file = request.files.get('cover_photo')
    update_cover_photo(session['user_id'], file)
    return redirect('/profile')

@app.route('/upload_showroom_photo/<int:showroom_id>', methods=['POST'])
def upload_showroom(showroom_id):
    file = request.files.get('showroom_photo')
    is_cover = request.form.get('is_cover') == 'yes'
    update_showroom_photo(showroom_id, file, is_cover)
    return redirect('/showroom/' + str(showroom_id))

@app.route('/upload_car_images/<int:car_id>', methods=['POST'])
def upload_car_images_route(car_id):
    files = request.files.getlist('car_images')
    save_car_images(car_id, files)
    return redirect('/car/' + str(car_id))   

def get_all_cars():
    conn = sqlite3.connect("swat_wheels.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM cars ORDER BY id DESC")
    cars = cur.fetchall()
    conn.close()
    return cars

def get_models_for_brand(brand):
    models = {
        "Daihatsu": ["Mira", "Mira ES", "Move", "Move Custom", "Tanto", "Cast", "Cast Style", "Terios Kid", "Hijet", "Cuore", "Boon", "Thor"],
        "Suzuki": ["Alto Japan", "Wagon R Japan", "Hustler", "Spacia", "Solio", "Every Wagon", "Every", "Swift Japan", "Mehran", "Cultus", "Bolan"],
        "Toyota": ["Passo", "Vitz", "Aqua", "Prius", "Camry", "Corolla", "Yaris", "Fortuner", "Hilux", "Land Cruiser", "C-HR", "Roomy", "Tank"],
        "Honda": ["N-Box", "N-One", "N-WGN", "Fit", "Vezel", "Freed", "City", "Civic", "Accord"],
        "Kia": ["Sportage", "Picanto", "Sorento", "Stonic", "Carnival", "Morning"],
        "Hyundai": ["Tucson", "Elantra", "Sonata", "Santa Fe", "Porter", "Eon"]
    }
    return models.get(brand, [])

def search_cars_db(brand="", model="", budget="", fuel="", transmission=""):
    conn = sqlite3.connect("swat_wheels.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    query = "SELECT * FROM cars WHERE 1=1"
    params = []

    if brand:
        query += " AND brand = ?"
        params.append(brand)
    if model:
        query += " AND model = ?"
        params.append(model)
    if fuel:
        query += " AND fuel = ?"
        params.append(fuel)
    if transmission:
        query += " AND transmission = ?"
        params.append(transmission)
    if budget == "under_10":
        query += " AND price < 1000000"
    elif budget == "10_20":
        query += " AND price BETWEEN 1000000 AND 2000000"
    elif budget == "20_30":
        query += " AND price BETWEEN 2000000 AND 3000000"

    cur.execute(query, params)
    cars = cur.fetchall()
    conn.close()
    return cars

@app.route('/')
def home():
    cars = get_all_cars()
    shwrooms = get_all_showrooms()
    return render_template('index.html', cars=cars, showrooms=shwrooms)

def get_all_showrooms():
    conn = sqlite3.connect("swat_wheels.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM showrooms ORDER BY id DESC")
    showrooms = cur.fetchall()
    conn.close()
    return showrooms

def get_showroom_by_id(showroom_id):
    conn = sqlite3.connect("swat_wheels.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM showrooms WHERE id = ?", (showroom_id,))
    showroom = cur.fetchone()
    conn.close()
    return showroom

def get_cars_by_showroom(showroom_id):
    conn = sqlite3.connect("swat_wheels.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM cars WHERE showroom_id = ?", (showroom_id,))
    cars = cur.fetchall()
    conn.close()
    return cars

@app.route('/showroom/<int:showroom_id>')
def showroom_detail(showroom_id):
    showroom = get_showroom_by_id(showroom_id)
    cars = get_cars_by_showroom(showroom_id)
    return render_template('showroom.html', showroom=showroom, cars=cars)

if __name__ == '__main__':
             port = int (os. environ.get('port',5000))
             app.run(host='0.0.0.0', port=port, debug= True)

