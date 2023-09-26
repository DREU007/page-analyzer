import os
import datetime
from contextlib import contextmanager

import psycopg2
import psycopg2.pool
import psycopg2.extras

from dotenv import load_dotenv


load_dotenv()


def init_db_pool():
    global db_pool
    DATABASE_URL = os.getenv('DATABASE_URL')
    CONFIG = {
        'minconn': 1,
        'maxconn': 20,
        'cursor_factory': psycopg2.extras.RealDictCursor,
        'dsn': DATABASE_URL
    }
    db_pool = psycopg2.pool.SimpleConnectionPool(**CONFIG)


@contextmanager
def get_connection():
    if 'db_pool' not in globals():
        init_db_pool()
    try:
        conn = db_pool.getconn()
        yield conn
        conn.commit()
    except Exception as error:
        conn.rollback()
        raise error
    finally:
        db_pool.putconn(conn)


class DB:
    def get_urls_data(self):
        with get_connection() as conn:
            with conn.cursor() as curr:
                curr.execute("""
                SELECT DISTINCT ON (urls.id) urls.id,
                    urls.name, url_checks.status_code, url_checks.created_at
                    FROM urls LEFT JOIN url_checks
                        ON urls.id = url_checks.url_id
                ORDER BY urls.id DESC;
                """)
                sql_data = curr.fetchall()
                return sql_data

    # TODO: Delete?
    def get_existing_urls(self):
        with get_connection() as conn:
            with conn.cursor() as curr:
                curr.execute('SELECT name FROM urls;')
                sql_data = curr.fetchall()
                if sql_data:
                    return [row['name'] for row in sql_data]
                return []

    def get_url_data(self, url_id):
        with get_connection() as conn:
            with conn.cursor() as curr:
                curr.execute("SELECT * FROM urls WHERE id = %s", (url_id,))
                url_data = curr.fetchone()
                return url_data

    def get_url_name(self, url_id):
        with get_connection() as conn:
            with conn.cursor() as curr:
                curr.execute('SELECT name FROM urls WHERE id = %s', (url_id,))
                sql_data = curr.fetchone()
                return sql_data['name']

    def get_url_id_by_name(self, normalized_url):
        with get_connection() as conn:
            with conn.cursor() as curr:
                curr.execute(
                    'SELECT id FROM urls WHERE name = %s', (normalized_url,)
                )
                url_id = curr.fetchone()['id']
                return url_id

    def is_url_name_in_db(self, normalized_url):
        try:
            return bool(self.get_url_id_by_name(normalized_url))
        except TypeError:
            return False

    def get_checks_data(self, url_id):
        with get_connection() as conn:
            with conn.cursor() as curr:
                curr.execute("""
                    SELECT * FROM url_checks WHERE url_id = %s ORDER BY id DESC
                    """, (url_id,)
                )
                sql_data = curr.fetchall()
                return sql_data

    def insert_url(self, normalized_url):
        with get_connection() as conn:
            with conn.cursor() as curr:
                curr.execute(
                    'INSERT INTO urls (name, created_at) VALUES (%s, %s)'
                    'RETURNING id;',
                    (normalized_url, datetime.date.today().isoformat())
                )
                return curr.fetchone()['id']

    def insert_check(
            self, url_id, status_code, h1, title, description
    ):
        with get_connection() as conn:
            with conn.cursor() as curr:
                curr.execute(
                    """
                    INSERT INTO url_checks (
                        url_id, status_code, created_at, h1, title, description
                    )
                    VALUES (%s, %s, %s, %s, %s, %s);
                    """,
                    (
                        url_id,
                        status_code,
                        datetime.date.today().isoformat(),
                        h1,
                        title,
                        description
                    )
                )
