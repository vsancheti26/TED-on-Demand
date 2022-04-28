from flask import Flask
from flask import render_template, request

app = Flask(__name__)
if __name__ == '__main__':
    app.run(debug=True)

# home page of our site
@app.route("/")  
def home():
	return render_template("index.html") 

@app.route('/', methods = ['POST'])
def form_post():
	user_input = request.form['promptInput']
	print(user_input)
	return render_template("result.html", prompt=user_input)

@app.route("/loading")  
def loading():
	return render_template("loading.html") 
