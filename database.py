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
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row

    new_post = Post(
        title='Sample Post',
        content='This is a sample post content.',
        author='Author Name',
    )

    insert_post(connection, new_post)

    print(get_posts(connection))

    connection.close()
