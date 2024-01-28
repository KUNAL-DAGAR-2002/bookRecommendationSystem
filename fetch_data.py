import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def preprocess():
    import pandas as pd
    books = pd.read_csv("data/Books.csv")
    ratings = pd.read_csv("data/Ratings.csv")
    users = pd.read_csv("data/Users.csv")
    user_books = ratings.merge(books, on='ISBN')
    return user_books, books
    
def all(user_books, books):
    num_rating = user_books.groupby('Book-Title').count()['Book-Rating'].reset_index()
    num_rating.rename(columns={'Book-Rating':'Num_Rating'},inplace=True)
    new_user_book = user_books[['User-ID', 'Book-Rating', 'Book-Title']]
    average_rating = new_user_book.groupby('Book-Title').mean()['Book-Rating'].reset_index()
    average_rating.rename(columns={'Book-Rating':'Average_Rating'},inplace=True)
    popular_rating = num_rating.merge(average_rating,on='Book-Title')
    popular_books = popular_rating[popular_rating['Num_Rating']>=250]
    popular_books.sort_values(by='Average_Rating',ascending=False,inplace=True)
    popular_books = popular_books.iloc[0:100]
    top_100 = popular_books.merge(books,on='Book-Title')
    top_100.drop_duplicates('Book-Title',inplace=True)
    top_100.drop(['ISBN', 'Image-URL-S','Image-URL-L'],axis=1,inplace=True)
    top_100.sample(frac=1).reset_index(drop=True)
    book_name = list(top_100['Book-Title'])
    votes = list(top_100['Num_Rating'])
    ratings = list(top_100['Average_Rating'])
    for i in range(len(ratings)):
        ratings[i] = round(float(ratings[i]), 2)
    author = list(top_100['Book-Author'])
    publisher = list(top_100['Publisher'])
    year = list(top_100['Year-Of-Publication'])
    img = list(top_100['Image-URL-M'])
    
    return book_name, votes, ratings, author, publisher, year, img
def best_50(user_books, books):
    num_rating = user_books.groupby('Book-Title').count()['Book-Rating'].reset_index()
    num_rating.rename(columns={'Book-Rating':'Num_Rating'},inplace=True)
    new_user_book = user_books[['User-ID', 'Book-Rating', 'Book-Title']]
    average_rating = new_user_book.groupby('Book-Title').mean()['Book-Rating'].reset_index()
    average_rating.rename(columns={'Book-Rating':'Average_Rating'},inplace=True)
    popular_rating = num_rating.merge(average_rating,on='Book-Title')
    popular_books = popular_rating[popular_rating['Num_Rating']>=250]
    popular_books.sort_values(by='Average_Rating',ascending=False,inplace=True)
    popular_books = popular_books.iloc[0:50]
    top_50 = popular_books.merge(books,on='Book-Title')
    top_50.drop_duplicates('Book-Title',inplace=True)
    top_50.drop(['ISBN', 'Image-URL-S','Image-URL-L'],axis=1,inplace=True)
    book_name = list(top_50['Book-Title'])
    votes = list(top_50['Num_Rating'])
    ratings = list(top_50['Average_Rating'])
    for i in range(len(ratings)):
        ratings[i] = round(float(ratings[i]), 2)
    author = list(top_50['Book-Author'])
    publisher = list(top_50['Publisher'])
    year = list(top_50['Year-Of-Publication'])
    img = list(top_50['Image-URL-M'])
    
    return book_name, votes, ratings, author, publisher, year, img

def recommend(user_books):
    x = user_books.groupby('User-ID').count()['Book-Rating'] > 200
    good_user = x[x].index
    filtered_rating = user_books[user_books['User-ID'].isin(good_user)]
    y = filtered_rating.groupby('Book-Title').count()['Book-Rating'] >= 50
    famous_books = y[y].index
    final_rating = filtered_rating[filtered_rating['Book-Title'].isin(famous_books)]
    pivot_data = final_rating.pivot_table(index='Book-Title', columns='User-ID', values='Book-Rating')
    pivot_data.fillna(0, inplace=True)
    score = cosine_similarity(pivot_data)
    return pivot_data, score

def recommend_title(user_books,book_title):
    try:
        x = user_books.groupby('User-ID').count()['Book-Rating'] > 200
        good_user = x[x].index
        filtered_rating = user_books[user_books['User-ID'].isin(good_user)]
        y = filtered_rating.groupby('Book-Title').count()['Book-Rating'] >= 50
        famous_books = y[y].index
        final_rating = filtered_rating[filtered_rating['Book-Title'].isin(famous_books)]
        pivot_data = final_rating.pivot_table(index='Book-Title', columns='User-ID', values='Book-Rating')
        pivot_data.fillna(0, inplace=True)
        score = cosine_similarity(pivot_data)
        index = np.where(pivot_data.index == book_title)[0]
        index = index[0]
        similar_books = sorted(list(enumerate(score[index])), key=lambda x: x[1], reverse=True)[1:6]
        book_name = []
        author = []
        year = []
        publisher = []
        img = []
        for i in similar_books:
            book_index = i[0]        
            book_name.append(pivot_data.index[book_index])
            author.append(user_books[user_books['Book-Title'] == pivot_data.index[book_index]].iloc[0, 4])
            year.append(user_books[user_books['Book-Title'] == pivot_data.index[book_index]].iloc[0, 5])
            publisher.append(user_books[user_books['Book-Title'] == pivot_data.index[book_index]].iloc[0, 6])
            img.append(user_books[user_books['Book-Title'] == pivot_data.index[book_index]].iloc[0, 8])
        return book_name,author,year,publisher,img
    except:
        book_name = list()
        author = list()
        year = list()
        publisher = list()
        img = list()
        
        return  book_name, author, year, publisher, img

def author(user_books,author_name):
    try:
        
        z = user_books.groupby('Book-Author').count()['Book-Title'] >= 10
        good_authors = z[z].index
        final_data = user_books[user_books['Book-Author'].isin(good_authors)]
        
        final_data.drop(['User-ID', 'ISBN'], axis=1, inplace=True)
        final_data.drop_duplicates(inplace=True)
        
        book_rating = final_data[['Book-Rating', 'Book-Title']]
        final_data.drop("Book-Rating", axis=1, inplace=True)
        final_data.drop_duplicates(inplace=True)
        
        book_rating = book_rating.groupby('Book-Title').mean()['Book-Rating'].reset_index()
        
        required = pd.merge(book_rating, final_data, on='Book-Title')
        
        required['Book-Author'] = required['Book-Author'].str.strip()
        required['Book-Author'] = required['Book-Author'].str.replace(' ', '')
        required['Book-Author'] = required['Book-Author'].str.replace('.', '')
        required['Book-Author'] = required['Book-Author'].str.lower()
        
        author_name = author_name.strip()
        author_name = author_name.replace(' ', '')
        author_name = author_name.replace('.', '')
        author_name = author_name.lower()
        temp = required[required['Book-Author'] == author_name]
        new = temp.sort_values(by='Book-Rating', ascending=False)
        final = new.iloc[0:10]
        
        book_name = list(final['Book-Title'])
        book_rating = list(final['Book-Rating'])
        for i in range(len(book_rating)):
            book_rating[i] = round(float(book_rating[i]), 2)
        year = list(final['Year-Of-Publication'])
        publisher = list(final['Publisher'])
        img = list(final['Image-URL-M'])
        
        return book_name, book_rating, year, publisher, img
    
    except:
        book_name = list()
        book_rating = list()
        year = list()
        publisher = list()
        img = list()
        
        return  book_name, book_rating, year, publisher, img
    

if __name__ == "__main__":
    print("In Main")