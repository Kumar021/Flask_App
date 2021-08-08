import os
import logging
from logging.config import dictConfig
from flask import Flask , render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy  import SQLAlchemy
from flask_session import Session
from forms import ContactForm



logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

DATABSE_FILE = "sqlite:///{}".format(os.path.join(PROJECT_DIR, "bookdatabase.db"))

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config["SESSION_PERMANENT"] = False 
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = DATABSE_FILE
db = SQLAlchemy(app)


#models 
app.logger.info("Creating books models table")
class Book(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(80), unique=True, nullable=False)

	def __repr__(self):
		return self.title



@app.route("/", methods=["GET", "POST"])
def home():
	if request.method == 'POST':
		app.logger.info("Call post method")
		book = Book(title=request.form.get("book_name"))
		db.session.add(book)
		db.session.commit()
		app.logger.info("Books name added successfull!")
	books = Book.query.all()
	app.logger.info("Get all books and send to template!")
	return render_template("home.html", books=books)

@app.route("/update/<int:id>/", methods=["GET", "POST"])
def update(id):
	books = Book.query.all()
	book = Book.query.filter_by(id=id).first()
	if request.method  == 'POST':
		title = request.form.get("title")
		book = Book.query.filter_by(id=id).first()
		book.title = title 
		db.session.commit()
		flash("Books name updated successfull!")  
		app.logger.info("Books name updated successfull!")
		return render_template("home.html", books=books)
	return render_template("home.html", book=book, books=books, title="update")


@app.route("/delete/<int:id>/", methods=["GET", "POST"])
def delete(id):
	books = Book.query.all()
	if id is not None and isinstance(id, int):
		book = Book.query.filter_by(id=id).first()
		db.session.delete(book)
		db.session.commit()
		flash("Books deleted successfull!") 
		app.logger.info("{} is deleted!".format(book.title))
		return redirect("/")
	return render_template("home.html", book=book, books=books, title="update")



@app.route("/contact/", methods=["GET", "POST"])
def contact():
	form = ContactForm()
	if form.validate_on_submit():
		print("form: ", request.form)
		print("name: ", form.name.data)
		return render_template("contact.html", form=form) 
	return render_template("contact.html", form=form)


@app.route('/set/')
def set():
	session['key'] = 'value'
	return 'ok'

@app.route('/get/')
def get():
	return session.get('key', 'not set')

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)