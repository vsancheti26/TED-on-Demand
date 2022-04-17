from flask import Flask
from flask import render_template

app = Flask(__name__)


# home page of our site
@app.route("/")  
def home():
	return render_template("index.html") 
