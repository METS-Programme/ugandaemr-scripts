import MySQLdb


class Database:
    host = 'localhost'
    user = 'openmrs'
    password = 'openmrs'
    db = 'openmrs'

    def __init__(self):
        self.connection = MySQLdb.connect(self.host, self.user, self.password, self.db)
        self.cursor = self.connection.cursor()

    def insert(self, q, d):
        try:
            self.cursor.execute(q, d)
            self.connection.commit()
            return self.cursor.lastrowid

        except MySQLdb.Error, e:
            self.connection.rollback()
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            except IndexError:
                print "MySQL Error: %s" % str(e)

    def insert_bulk(self, q, data):
        try:
            chunks = [data[x:x + 500] for x in xrange(0, len(data), 500)]
            for c in chunks:
                self.cursor.executemany(q, c)
                self.connection.commit()
        except MySQLdb.Error, e:
            self.connection.rollback()
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            except IndexError:
                print "MySQL Error: %s" % str(e)

    def query(self, query):
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query)
        return cursor.fetchall()

    def query_one(self, query):
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query)
        return cursor.fetchone()

    def __del__(self):
        self.connection.close()
