from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_title = db.Column(db.String(100))
    author = db.Column(db.String(100))
    genre = db.Column(db.String(100))
    rating = db.Column(db.Integer)
    review = db.Column(db.Text)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    books = Book.query.all()
    return render_template("home.html", books=books)

@app.route("/clear", methods=["POST"])
def clear_db():
    Book.query.delete()
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/delete/<int:entry_id>", methods=["POST"])
def delete_entry(entry_id):
    entry = Book.query.get_or_404(entry_id)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/submit", methods=["POST"])
def submit():
    book_title = request.form.get("book-title")
    author = request.form.get("author")
    genre = request.form.get("genre")
    rating = request.form.get("rating")
    review = request.form.get("review")

    book = Book(book_title=book_title, author=author, genre=genre, rating=rating, review=review)
    db.session.add(book)
    db.session.commit()

    return redirect(url_for("home"))
        

if __name__ == "__main__":
    app.run(debug=True)