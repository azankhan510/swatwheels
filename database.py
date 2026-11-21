import sqlite3 

DB_name = "swat_wheels.db"

def get_connection():
   return sqlite3 . connect(DB_name)

def create_tables():
   conn = get_connection()
   cursor = conn.cursor()
   cursor.execute(''' create table if not exists users (id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL,
   cnic TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
     phone TEXT NOT NULL,
      password TEXT NOT NULL,
       bio TEXT NOT NULL, 
        type TEXT NOT NULL,
         establishment_year TEXT,
         showroom_address TEXT)''')
   conn.commit()
   print("user table completed!")

   cursor.execute(''' create table if not exists cars (id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand TEXT NOT NULL,
    engine_cc TEXT NOT NULL,
    year TEXT NOT NULL,
    model TEXT NOT NULL,
    fuel TEXT NOT NULL,
    price TEXT NOT NULL,
    transmission TEXT NOT NULL,
    condition TEXT NOT NULL, 
    milage TEXT NOT NULL,
    location TEXT NOT NULL)''') 

   cursor.execute('''CREATE TABLE IF NOT EXISTS showrooms(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   username TEXT NOT NULL,
   cnic TEXT NOT NULL,
   email TEXT NOT NULL,
   account_type TEXT NOT NULL,
   establishment_year TEXT NOT NULL,
   showroom_address TEXT NOT NULL,
   password TEXT NOT NULL,
   phone TEXT NOT NULL,
   bio TEXT
   )''')

   print ("showroom table completed!")

   conn.commit()
   conn.close()
   print("car table completed!")
   conn.close()

def add_user(username, cnic, email, phone, password, bio, type, establishment_year=None, showroom_address=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users(username, cnic, email, phone, password, bio, type, establishment_year, showroom_address) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (username, cnic, email, phone, password,bio, type, establishment_year, showroom_address))
    conn.commit()
    conn.close()
    print(f"user {username} saved successfully!")

def get_user(username, password):
         conn = get_connection()
         cursor = conn.cursor()
         cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
         user = cursor.fetchone()
         conn.close()
         return user

def add_car_db (brand, engine_cc, year, model, fuel, price, transmission, condition, milage, location):
      conn = get_connection()
      cursor = conn.cursor()
      cursor.execute("INSERT INTO cars (brand, engine_cc, year, model, fuel, price, transmission, condition, milage, location) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                      (brand, engine_cc, year, model, fuel, price, transmission, condition, milage, location))
      conn.commit()
      conn.close()
      print(f"car {brand} {model} saved successfully!")

def get_all_cars():     
       conn = get_connection()
       conn.row_factory = sqlite3.Row
       cursor = conn.cursor()
       cursor.execute('SELECT * FROM cars')
       cars = cursor.fetchall()
       conn.close()
       return cars


if __name__ == "__main__":
    create_tables()

                        


