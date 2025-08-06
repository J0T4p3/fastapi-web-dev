import sqlite3
from sqlite3 import Connection

from models import Post, Posts


def get_posts(connection: Connection) -> Posts:
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM posts')

    return Posts(posts=[Post(**row) for row in cursor.fetchall()])


def get_post_by_id(connection: Connection, post_id: int) -> Post:
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM posts WHERE id = ?', (post_id,))
    return cursor.fetchone()


def insert_post(connection: Connection, post: Post,) -> None:
    with connection:
        cursor = connection.cursor()
        cursor.execute(
            '''
            INSERT INTO posts (title, content, author, created_at, updated_at)
            VALUES (:title, :content, :author, datetime('now'), datetime('now'));
            ''',
            post.model_dump(
                # Use model_dump to convert Post to dict
                exclude_unset=True, exclude_defaults=True,)
        )
        print("Post inserted successfully")


if __name__ == '__main__':
    # Create the database and table if they don't exist
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row

    # Create the posts table
    cursor = connection.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        '''
    )
    connection.commit()

    # Create multiple posts for testing
    from database import insert_post, get_posts
    for i in range(5):
        post = Post(title=f"Post {i+1}", content=f"This is the content of post {i+1}.", author=f"Author{i+1}")
        insert_post(connection, post)
    print("New posts created successfully")

    print("All posts in the database:")
    for post in get_posts(connection).posts:
        print(post)

    connection.close()
