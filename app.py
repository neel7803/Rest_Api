import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def Welcome():
    return render_template('index.html')
  
@app.route('/home')
def greet():  
    return f'Hello,scascass!'
@app.route('/about')
def about():
    return 'This is a simple Flask API example.'


if __name__ == '__main__':
    app.run(debug=True)