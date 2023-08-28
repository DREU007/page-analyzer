import datetime

import psycopg2
import psycopg2.pool
import psycopg2.extras


DEFAULT_CFG = {
    'minconn': 1,
    'maxconn': 20,
    'cursor_factory': psycopg2.extras.RealDictCursor
}


class DB:
    def __init__(self, **options):
        config = DEFAULT_CFG | options
        self.conn_pool = psycopg2.pool.SimpleConnectionPool(
            **config
        )

#    def get_connection(self, func):
#        with self.conn_pool.getconn() as conn:
#            try:
#                curr = conn.curr()
#
#

    def get_urls_data(self):
        with self.conn_pool.getconn() as conn:
            curr = conn.cursor()
            curr.execute("""
            SELECT DISTINCT ON (urls.id) urls.id,
                urls.name, url_checks.status_code, url_checks.created_at
                FROM urls LEFT JOIN url_checks ON urls.id = url_checks.url_id
            ORDER BY urls.id DESC;
            """)
            sql_data = curr.fetchall()
        return sql_data

    def get_existing_urls(self):
        with self.conn_pool.getconn() as conn:
            curr = conn.cursor()
            curr.execute('SELECT name FROM urls;')
            sql_data = curr.fetchall()
            if sql_data:
                return [row['name'] for row in sql_data]
        return []

    def get_url_data(self, url_id):
        with self.conn_pool.getconn() as conn:
            curr = conn.cursor()
            curr.execute("SELECT * FROM urls WHERE id = %s", (url_id,))
            url_data = curr.fetchone()
        return url_data

    def get_url_id_by_name(self, normalized_url):
        with self.conn_pool.getconn() as conn:
            curr = conn.cursor()
            curr.execute(
                'SELECT id FROM urls WHERE name = %s', (normalized_url,)
            )
            url_id = curr.fetchone()['id']
        return url_id

    def get_url_name(self, url_id):
        with self.conn_pool.getconn() as conn:
            curr = conn.cursor()
            curr.execute('SELECT name FROM urls WHERE id = %s', (url_id,))
            sql_data = curr.fetchone()
        return sql_data['name']

    def get_checks_data(self, url_id):
        with self.conn_pool.getconn() as conn:
            curr = conn.cursor()
            curr.execute("""
                SELECT * FROM url_checks WHERE url_id = %s ORDER BY id DESC
                """, (url_id,)
            )
            sql_data = curr.fetchall()
            return sql_data

    def insert_url(self, normalized_url):
        with self.conn_pool.getconn() as conn:
            curr = conn.cursor()
            curr.execute(
                'INSERT INTO urls (name, created_at) VALUES (%s, %s);',
                (normalized_url, datetime.date.today().isoformat())
            )
            conn.commit()

    def insert_check(self, url_id, status_code, h1, title, description):
        with self.conn_pool.getconn() as conn:
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
