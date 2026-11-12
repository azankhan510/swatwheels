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
       type TEXT NOT NULL,
        establishment_year TEXT,
        showroom_address TEXT)''')
   conn.commit()
   conn.close()
   print("user table completed!")

def add_user(username, cnic, email, phone, password, type, establishment_year=None, showroom_address=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, cnic, email, phone, password, type, establishment_year, showroom_address) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (username, cnic, email, phone, password, type, establishment_year, showroom_address))
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

if __name__ == "__main__":
    create_tables()

                        


