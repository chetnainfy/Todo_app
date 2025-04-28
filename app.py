# creating flask app
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__) # this creates the Flask app

# this connect to database
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# this creates the home page
@app.route('/') # sets the url path /, which is home page
# this is the function that runs when the home page is accessed
def index(): 
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM todos').fetchall()
    conn.close()
    return render_template('index.html', todos=posts)

# this creates the add page
@app.route('/add', methods=['POST']) # this handles the form submission from the add page
def add():
    task= request.form.get('task') # get the task the user entered in the form
    # insert the task into the database
    conn = get_db_connection()
    # new_todo = request.form['todo']
    conn.execute('INSERT INTO todos (task) VALUES (?)', (task,))
    conn.commit() # commit the changes to the database
    conn.close()
    return redirect(url_for('index')) # redirect to the home page after adding the task

@app.route('/delete/<int:todo_id>') # sets up a URL like /delete1, etc.
def delete(todo_id):
    conn= get_db_connection()
    conn.execute('DELETE FROM todos WHERE id = ?',(todo_id)) # delete todo item with that id
    conn.commit()
    conn.close()
    return redirect(url_for('index')) # sfter deleting redirects back to home page

if __name__ == '__main__': # only run the app if file is run directly( not if its imported somewhere else)
    app.run(debug= True) # means id you change code, Flask automatically reloads, and it shows detailed error messages id anything goes wrong
    




