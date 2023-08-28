import os
import datetime

import psycopg2
import psycopg2.pool
import psycopg2.extras

from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
CONFIG = {
    'minconn': 1,
    'maxconn': 20,
    'cursor_factory': psycopg2.extras.RealDictCursor,
    'dsn': DATABASE_URL
}


def get_connection():
    return psycopg2.pool.SimpleConnectionPool(**CONFIG)


class DB:
    def get_urls_data(self, conn_pool):
        with conn_pool.getconn() as conn:
            curr = conn.cursor()
            curr.execute("""
            SELECT DISTINCT ON (urls.id) urls.id,
                urls.name, url_checks.status_code, url_checks.created_at
                FROM urls LEFT JOIN url_checks ON urls.id = url_checks.url_id
            ORDER BY urls.id DESC;
            """)
            sql_data = curr.fetchall()
        return sql_data

    def get_existing_urls(self, conn_pool):
        with conn_pool.getconn() as conn:
            curr = conn.cursor()
            curr.execute('SELECT name FROM urls;')
            sql_data = curr.fetchall()
            if sql_data:
                return [row['name'] for row in sql_data]
        return []

    def get_url_data(self, conn_pool, url_id):
        with conn_pool.getconn() as conn:
            curr = conn.cursor()
            curr.execute("SELECT * FROM urls WHERE id = %s", (url_id,))
            url_data = curr.fetchone()
        return url_data

    def get_url_id_by_name(self, conn_pool, normalized_url):
        with conn_pool.getconn() as conn:
            curr = conn.cursor()
            curr.execute(
                'SELECT id FROM urls WHERE name = %s', (normalized_url,)
            )
            url_id = curr.fetchone()['id']
        return url_id

    def get_url_name(self, conn_pool, url_id):
        with conn_pool.getconn() as conn:
            curr = conn.cursor()
            curr.execute('SELECT name FROM urls WHERE id = %s', (url_id,))
            sql_data = curr.fetchone()
        return sql_data['name']

    def get_checks_data(self, conn_pool, url_id):
        with conn_pool.getconn() as conn:
            curr = conn.cursor()
            curr.execute("""
                SELECT * FROM url_checks WHERE url_id = %s ORDER BY id DESC
                """, (url_id,)
            )
            sql_data = curr.fetchall()
            return sql_data

    def insert_url(self, conn_pool, normalized_url):
        with conn_pool.getconn() as conn:
            curr = conn.cursor()
            curr.execute(
                'INSERT INTO urls (name, created_at) VALUES (%s, %s);',
                (normalized_url, datetime.date.today().isoformat())
            )
            conn.commit()

    def insert_check(
            self, conn_pool, url_id, status_code, h1, title, description
    ):
        with conn_pool.getconn() as conn:
            curr = conn.cursor()
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
            conn.commit()
