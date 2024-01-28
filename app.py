from flask import Flask, request, jsonify, render_template
from fetch_data import best_50, recommend_title, author, all, preprocess
import pandas as pd


app = Flask(__name__)

user_books, books = preprocess()
@app.route("/", methods=['GET'])
def home():
    book_name, votes, ratings, author, publisher, year, img = all(user_books,books)
    length = len(book_name)
    return render_template('index.html',length=length,book_name=book_name,votes=votes,ratings=ratings,author=author,year=year,publisher=publisher,img=img)

@app.route("/recommend",methods=['POST'])
def recommend():
    if request.method == "POST":
        book_title = request.form.get('recommend')
        book_name,author,year,publisher,img = recommend_title(user_books,book_title)
        length = len(book_name)
        if length == 0:
            return render_template('recomend.html',message=f"Sorry we don't have {book_title} related books or please mention the exact name",length=length)
        return render_template('recomend.html',book_name=book_name,author=author,year=year,publisher=publisher,img=img,length=length)

@app.route("/topAuthors",methods=['POST'])
def topAuthor():
    if request.method == "POST":
        author_name = request.form.get('author')
        book_name, ratings, year, publisher, img = author(user_books,author_name)
        length = len(book_name)
        if length == 0:
            return render_template('author.html',message=f"Sorry we don't have the books of {author_name}",length=length)
        return render_template('author.html',book_name=book_name, ratings=ratings,year=year,publisher=publisher,img=img,length=length,author=author_name)

@app.route("/top50",methods=['POST'])
def top50():
    if request.method=="POST":
        book_name, votes, ratings, author, publisher, year, img = best_50(user_books, books)
        length = len(book_name)
        return render_template('top.html',length=length,book_name=book_name,votes=votes,ratings=ratings,author=author,year=year,publisher=publisher,img=img)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

