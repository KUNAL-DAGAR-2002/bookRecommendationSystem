# Book Recommendation System Web App

## Introduction

This web app is designed to provide personalized book recommendations based on a dataset sourced from Kaggle. The dataset consists of three tables: `book.csv`, `users.csv`, and `ratings.csv`.

## Dataset

- `book.csv`: Contains information about books, including book ID, title, author, and other relevant details.
- `users.csv`: Contains user information.
- `ratings.csv`: Contains user ratings for various books.

## Web App Features

### Personalized Recommendations

- **Endpoint:** `/recommend/{book_name}`
- **Description:** Get personalized book recommendations based on the provided book name based on Euclidean distance.

### Filter by Author

- **Endpoint:** `/author`
- **Description:** Filter books by a specific author to discover more titles from the same author.

### Top 50 Books

- **Endpoint:** `/top_50`
- **Description:** Retrieve a list of the top 50 books based on certain criteria based on number of votes and ratings.

### Top 100 Books (Index Page)

- **Endpoint:** `/`
- **Description:** Display the top 100 books on the index page.
