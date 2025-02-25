
from flask import Flask, render_template, request, jsonify
import sqlite3
import os
  
app = Flask(__name__) 
  
  
@app.route('/') 
@app.route('/home') 
def index(): 
    return render_template('index.html') 
  
connect = sqlite3.connect('database.db') 
connect.execute( 
    'CREATE TABLE IF NOT EXISTS FILES ( \
        id INTEGER PRIMARY KEY AUTOINCREMENT, \
        filename TEXT, \
        file_data BLOB NOT NULL)') 

@app.route('/save', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the file temporarily
    file_path = os.path.join("temp_upload", file.filename)
    file.save(file_path)

    # Read the file data
    with open(file_path, 'rb') as f:
        file_data = f.read()
        print(file_data)

    # Save the file data to the database
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute('INSERT INTO files (filename, file_data) VALUES (?, ?)', (file.filename, file_data))
    conn.commit()
    conn.close()

    # Remove the temporary file
    os.remove(file_path)

    return jsonify({'message': 'File uploaded and saved successfully'}), 201

@app.route('/files') 
def files(): 
    conn = sqlite3.connect('database.db') 
    cur = conn.cursor() 
    cur.execute('SELECT * FROM FILES') 
  
    data = cur.fetchall() 
    print(data)
    return render_template("files.html", data=data)  

  
if __name__ == '__main__': 
    app.run(debug=False) 