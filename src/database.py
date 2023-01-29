import pymysql
import pymysql.cursors
from datetime import datetime
from setting import setting


class Database:
    def __init__(self):
        self.host = setting['DB_HOST']
        self.user = setting['DB_USER']
        self.pw = setting['DB_PASSWORD']
        self.db = setting['DB_NAME']
        self.connection = None
        self.cursor = None

        try:
            self.connection = pymysql.connect(host=self.host, user=self.user, password=self.pw, database=self.db)
            self.cursor = self.connection.cursor(pymysql.cursors.DictCursor)
            print('[알림] 데이터베이스 연결에 성공했습니다.')
        except Exception as e:
            print(f"[알림] 데이터베이스 연결에 실패했습니다.\n{e}\n")

    def __del__(self):
        if self.connection is not None:
            self.connection.close()
            print('[알림] DB 연결을 끊었습니다.')

    def is_connected(self):
        if self.connection is not None:
            self.connection.ping()
            return True
        return False

    def update_auction_item_price(self, name: str, price: int):
        if not self.is_connected(): return

        date = datetime.now().strftime('%Y-%m-%d')
        today_price = self.get_auction_today_item_price(name)

        if today_price < 0:
            sql = 'INSERT INTO auction (date, name, price) values (%s, %s, %s) '
            self.cursor.execute(sql, (date, name, price))
        else:
            sql = 'UPDATE auction SET price=%s WHERE date=%s and name=%s'
            self.cursor.execute(sql, (price, date, name))
        self.connection.commit()

    def get_auction_today_item_price(self, name: str) -> int:
        if not self.is_connected(): return -1

        date = datetime.now().strftime('%Y-%m-%d')
        sql = 'SELECT * FROM auction WHERE date=%s and name=%s'
        self.cursor.execute(sql, (date, name))
        row = self.cursor.fetchone()

        if row is None:
            return -1
        return row['price']

    def get_auction_latest_item_price(self, name) -> dict or None:
        if not self.is_connected(): return None

        sql = 'SELECT * ' \
              'FROM auction ' \
              'WHERE name=%s ' \
              'ORDER BY date DESC ' \
              'LIMIT 1'
        self.cursor.execute(sql, name)
        row = self.cursor.fetchone()
        return row

    def get_auction_second_latest_item_info(self, name) -> dict or None:
        if not self.is_connected(): return None

        sql = 'SELECT * ' \
              'FROM auction ' \
              'WHERE name=%s ' \
              'ORDER BY date DESC ' \
              'LIMIT 1, 1'
        self.cursor.execute(sql, name)
        row = self.cursor.fetchone()
        return row


database = Database()