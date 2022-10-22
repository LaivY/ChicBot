# # Import common module
# import json, pymysql
# from datetime import datetime
#
# # Import my module
# from ini import ini
#
# class Connection:
#     def __init__(self):
#         self.host = ini['host']
#         self.user = ini['user']
#         self.pw = ini['password']
#         self.db = ini['database']
#         self.conn = None
#         self.cur = None
#
#         try:
#             self.conn = pymysql.connect(host=self.host, user=self.user, password=self.pw, database=self.db)
#             self.cur = self.conn.cursor(pymysql.cursors.DictCursor)
#             print('[알림] DB에 성공적으로 연결되었습니다.')
#         except Exception as e:
#             print(f"[알림] DB 연결 중 오류가 발생했습니다 :: {e}")
#
#     def __del__(self):
#         if self.conn is not None:
#             self.conn.close()
#             print('[알림] DB 연결을 끊었습니다.')
#
#     def isConnected(self):
#         if self.conn is not None:
#             self.conn.ping()
#             return True
#         return False
#
#     # Search
#     def getEpicRanks(self):
#         if not self.isConnected(): return
#
#         sql = 'DELETE FROM epicRank WHERE date <= LAST_DAY(NOW() - interval 1 month)'
#         self.cur.execute(sql)
#         self.conn.commit()
#
#         sql = 'SELECT * FROM epicRank WHERE date > LAST_DAY(NOW() - interval 1 month) AND date <= LAST_DAY(NOW())'
#         self.cur.execute(sql)
#         return self.cur.fetchall()
#
#     def getEpicRank(self, server, name):
#         if not self.isConnected(): return
#
#         sql = f'SELECT * FROM epicRank WHERE server=%s and name=%s'
#         self.cur.execute(sql, (server, name))
#         return self.cur.fetchone()
#
#     def updateEpicRank(self, server, name, count, channel):
#         if not self.isConnected(): return
#
#         date = datetime.now().strftime('%Y-%m-%d')
#         epicRank = self.getEpicRank(server, name)
#
#         if epicRank is None:
#             sql = 'INSERT INTO epicRank (date, server, name, count, channel) values (%s, %s, %s, %s, %s)'
#             self.cur.execute(sql, (date, server, name, count, channel))
#         else:
#             sql = 'UPDATE epicRank SET date=%s, count=%s, channel=%s WHERE server=%s and name=%s'
#             self.cur.execute(sql, (date, count, channel, server, name))
#         self.conn.commit()
#
#     # Auction
#     def getTodayPrice(self, name):
#         if not self.isConnected(): return
#
#         date = datetime.now().strftime('%Y-%m-%d')
#         sql = f"SELECT * FROM auction WHERE date=%s and name=%s"
#         self.cur.execute(sql, (date, name))
#         rs = self.cur.fetchone()
#         return None if rs is None else rs['price']
#
#     def getLatestPrice(self, name):
#         if not self.isConnected(): return
#
#         try:
#             sql = 'SELECT * FROM auction WHERE name=%s'
#             self.cur.execute(sql, name)
#             rs = self.cur.fetchall()
#             return rs[-1]
#         except: return None
#
#     def getPrevPrice(self, name):
#         if not self.isConnected(): return
#
#         try:
#             sql = 'SELECT * FROM auction WHERE name=%s'
#             self.cur.execute(sql, name)
#             rs = self.cur.fetchall()
#             return rs[-2]
#         except: return None
#
#     def updateAuctionPrice(self, itemName, price):
#         if not self.isConnected(): return
#
#         date = datetime.now().strftime('%Y-%m-%d')
#         todayPrice = self.getTodayPrice(itemName)
#
#         if todayPrice is None:
#             sql = 'INSERT INTO auction (date, name, price) values (%s, %s, %s) '
#             self.cur.execute(sql, (date, itemName, price))
#         else:
#             sql = 'UPDATE auction SET price=%s WHERE date=%s and name=%s'
#             self.cur.execute(sql, (price, date, itemName))
#         self.conn.commit()
#
#     # Account
#     def iniAccount(self, did):
#         if not self.isConnected(): return
#
#         sql = 'INSERT INTO account values (%s, %s, %s, %s)'
#         self.cur.execute(sql, (did, 10000000, datetime(9999, 12, 31), 0))
#         self.conn.commit()
#
#     def getAccount(self, did):
#         if not self.isConnected(): return
#
#         sql = f'SELECT * FROM account WHERE did=%s'
#         self.cur.execute(sql, did)
#         return self.cur.fetchone()
#
#     def getAccounts(self):
#         if not self.isConnected(): return
#
#         sql = f'SELECT * FROM account'
#         self.cur.execute(sql)
#         return self.cur.fetchall()
#
#     def getGold(self, did):
#         if not self.isConnected(): return
#
#         try: return self.getAccount(did)['gold']
#         except: return None
#
#     def gainGold(self, did, gold):
#         if not self.isConnected(): return
#
#         old = self.getGold(did)
#         new = max(old + gold, 0)
#
#         sql = 'UPDATE account SET gold=%s WHERE did=%s'
#         self.cur.execute(sql, (new, did))
#         self.conn.commit()
#
#     def updateDailyCheck(self, did):
#         if not self.isConnected(): return
#
#         today = datetime.now().strftime('%Y-%m-%d')
#         account = self.getAccount(did)
#         if account is None:
#             self.iniAccount(did)
#
#         sql = 'UPDATE account SET checkDate=%s, checkCount=%s WHERE did=%s'
#         self.cur.execute(sql, (today, account['checkCount'] + 1, did))
#         self.conn.commit()
#
#     # Reinforce
#     def setReinforce(self, did, itemId=None, itemName=None, value=None, _max=None, _try=None):
#         if not self.isConnected(): return
#
#         reinforce = self.getReinforce(did)
#         if reinforce is None:
#             sql = 'INSERT INTO reinforce values (%s, %s, %s, %s, %s, %s)'
#             _max = {
#                 'itemName': itemName,
#                 'value': 0
#             }
#             _try = {
#                 'success': 0,
#                 'fail': 0,
#                 'destroy': 0
#             }
#             self.cur.execute(sql, (did, itemId, itemName, value,
#                                    json.dumps(_max, ensure_ascii=False), json.dumps(_try, ensure_ascii=False)))
#         else:
#             sql = 'UPDATE reinforce SET itemId=%s, itemName=%s, value=%s, max=%s, try=%s WHERE did=%s'
#             itemId = reinforce['itemId'] if itemId is None else itemId
#             itemName = reinforce['itemName'] if itemName is None else itemName
#             value = reinforce['value'] if value is None else value
#             _max = reinforce['max'] if _max is None else json.dumps(_max, ensure_ascii=False)
#             _try = reinforce['try'] if _try is None else json.dumps(_try, ensure_ascii=False)
#             self.cur.execute(sql, (itemId, itemName, value, _max, _try, did))
#         self.conn.commit()
#
#     def getReinforce(self, did):
#         if not self.isConnected(): return
#
#         sql = 'SELECT * FROM reinforce WHERE did=%s'
#         self.cur.execute(sql, did)
#         return self.cur.fetchone()
#
#     def getReinforces(self):
#         if not self.isConnected(): return
#
#         sql = f"SELECT * FROM reinforce"
#         self.cur.execute(sql)
#         return self.cur.fetchall()
#
# # Global connection
# c = Connection()