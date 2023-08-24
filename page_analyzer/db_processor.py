import datetime


class DB:
    def __init__(self, conn, curr):
        self.conn = conn
        self.curr = curr

    def get_urls_data(self):
        self.curr.execute("""
        SELECT DISTINCT ON (urls.id) urls.id,
            urls.name, url_checks.status_code, url_checks.created_at
            FROM urls LEFT JOIN url_checks ON urls.id = url_checks.url_id
        ORDER BY urls.id DESC;
        """)
        sql_data = self.curr.fetchall()
        return sql_data

    def get_existing_urls(self):
        self.curr.execute('SELECT name FROM urls;')
        sql_data = self.curr.fetchall()
        if sql_data:
            return [row['name'] for row in sql_data]
        return []

    def get_url_data(self, url_id):
        self.curr.execute("SELECT * FROM urls WHERE id = %s", (url_id,))
        url_data = self.curr.fetchone()
        return url_data

    def get_url_id_by_name(self, normalized_url):
        self.curr.execute(
            'SELECT id FROM urls WHERE name = %s', (normalized_url,)
        )
        url_id = self.curr.fetchone()['id']
        return url_id

    def get_url_name(self, url_id):
        self.curr.execute('SELECT name FROM urls WHERE id = %s', (url_id,))
        sql_data = self.curr.fetchone()
        return sql_data['name']

    def get_checks_data(self, url_id):
        self.curr.execute("""
             SELECT * FROM url_checks WHERE url_id = %s ORDER BY id DESC
             """, (url_id,)
             )
        sql_data = self.curr.fetchall()
        return sql_data

    def insert_url(self, normalized_url):
        self.curr.execute(
            'INSERT INTO urls (name, created_at) VALUES (%s, %s);',
            (normalized_url, datetime.date.today().isoformat())
        )
        self.conn.commit()

    def insert_check(self, url_id, status_code, h1, title, description):
        self.curr.execute("""
            INSERT INTO url_checks (
                url_id, status_code, created_at, h1, title, description
            )
            VALUES (%s, %s, %s, %s, %s, %s);
            """, (
                url_id,
                status_code,
                datetime.date.today().isoformat(),
                h1,
                title,
                description
            )
        )
        self.conn.commit()
