from flask import Flask, request, render_template, redirect, url_for, session
import os
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
            record = {"username": username, "cnic": cnic, "email": email, "phone": phone, "password": password, "bio": bio}
            users_list.append(record)
            return "individual account registered successfully! <br><a href='/login'>Login Karo</a>"
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
            record = {"username": username, "cnic": cnic, "email": email, "phone": phone, "establishment_year": establishment_year, "showroom_address": showroom_address, "password": password, "type": account_type.lower().strip(), "bio": bio}
            users_list.append(record)
            return "showroom or company account registered successfully! <br><a href='/login'>Login Karo</a>"
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

@app.route('/dashboard')
def dashboard():
    user = session.get('current_user')
    if not user:
        return redirect(url_for('loginuser'))
        
    return render_template('dashboard.html', user=user, cars=cars_list)

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

@app.route('/delete-car-listing/<int:index>', methods=['POST'])
def delete_car_listing(index):
    if 0 <= index < len(cars_list):
        del cars_list[index]
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

@app.route('/list-car', methods=['GET', 'POST'])
def add_car():
    if request.method == 'POST':
        car = {
           'company': request.form['company'], 
            'title': request.form['title'],
            'price': request.form['price'],
            'model': request.form['model'],
            'city': request.form['city']
        }
        cars_list.append(car)
        return redirect(url_for('home'))
    return render_template('add_car.html')

if __name__ == '__main__':
    port = int (os. environ.get('port',5000))
    app.run(host='0.0.0.0', port=port, debug= True)
