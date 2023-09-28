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
                curr.execute(
                    'SELECT id, name FROM urls ORDER BY id DESC;'
                )
                query_urls = curr.fetchall()

                curr.execute(
                    """
                    SELECT DISTINCT ON (url_id) url_id, status_code, created_at
                        FROM url_checks
                        ORDER BY url_id DESC, created_at DESC;
                    """
                )
                query_checks = curr.fetchall()

                sql_data = []
                try:
                    while query_urls:
                        while query_checks:
                            e1 = query_urls.pop(0)
                            e2 = query_checks[0]
                            if e1['id'] == e2['url_id']:
                                sql_data.append(e1 | e2)
                                query_checks.pop(0)
                            else:
                                sql_data.append(e1)
                        sql_data.extend(query_urls)
                except IndexError:
                    pass
                return sql_data

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

    def _get_url_id_by_name(self, normalized_url):
        with get_connection() as conn:
            with conn.cursor() as curr:
                curr.execute(
                    'SELECT id FROM urls WHERE name = %s', (normalized_url,)
                )
                url_id = curr.fetchone()['id']
                return url_id

    def get_url_id_by_name_or_false(self, normalized_url):
        """Return id if url_name in db, else False"""
        try:
            return self._get_url_id_by_name(normalized_url)
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
