
import sqlite3

DB_NAME = "movies.db"


def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_name TEXT NOT NULL,
            genre TEXT NOT NULL,
            rating REAL NOT NULL,
            release_year INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def add_movie(name, genre, rating, year):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO movies
        (movie_name, genre, rating, release_year)
        VALUES (?, ?, ?, ?)
    """, (name, genre, rating, year))

    conn.commit()
    conn.close()


def get_movies():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM movies")
    data = cursor.fetchall()

    conn.close()
    return data


def get_total_movies():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM movies")
    total = cursor.fetchone()[0]

    conn.close()
    return total


def get_average_rating():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT AVG(rating) FROM movies")
    result = cursor.fetchone()[0]

    conn.close()
    return result or 0


def get_highest_rated_movie():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM movies
        ORDER BY rating DESC
        LIMIT 1
    """)

    movie = cursor.fetchone()
    conn.close()

    return movie


def get_genre_summary():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT genre, COUNT(*)
        FROM movies
        GROUP BY genre
    """)

    data = cursor.fetchall()
    conn.close()

    return data
