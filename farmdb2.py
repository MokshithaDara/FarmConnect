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

# Specify the user IDs you want to delete
user_ids_to_delete = [12, 13,14, 15]

# Delete the specified users from the 'users' table
for user_id in user_ids_to_delete:
    cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))

# Fetch and print updated details from the 'users' table
cursor.execute('SELECT * FROM users')
updated_users_data = cursor.fetchall()

print("\nUpdated Users Table:")
for user in updated_users_data:
    print(user)

# Fetch and print details from the 'products' table
cursor.execute('SELECT * FROM products')
products_data = cursor.fetchall()

print("\nProducts Table:")
for product in products_data:
    print(product)

# Specify the product IDs you want to delete
product_ids_to_delete = []

# Delete the specified products from the 'products' table
for product_id in product_ids_to_delete:
    cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))

# Fetch and print updated details from the 'products' table
cursor.execute('SELECT * FROM products')
updated_products_data = cursor.fetchall()

print("\nUpdated Products Table:")
for product in updated_products_data:
    print(product)

# Commit the changes and close the cursor and connection
conn.commit()
cursor.close()
conn.close()
