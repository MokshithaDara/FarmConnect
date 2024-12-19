import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("farmers_marketplace.db")
cursor = conn.cursor()

# Fetch and print details from the 'users' table
cursor.execute('SELECT * FROM users')
users_data = cursor.fetchall()

print("Users Table:")
for user in users_data:
    print(user)

# Fetch and print details from the 'products' table
cursor.execute('SELECT * FROM products')
products_data = cursor.fetchall()

print("\nProducts Table:")
for product in products_data:
    print(product)

# Close the cursor and connection
cursor.close()
conn.close()
