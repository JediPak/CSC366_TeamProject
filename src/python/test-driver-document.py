from sqlalchemy import create_engine

import unittest

class TestDBSetup(unittest.TestCase):

    def setUp(self):
        engine = create_engine(
            'postgresql://postgres:testtest@db.caoodninwjvh.us-east-2.rds.amazonaws.com:5432/postgres'
        )
        self.conn = engine.connect()

    def test1(self):
        for row in self.conn.execute("SELECT * from test;").fetchall():
            print(row)
        
if __name__ == '__main__':
    unittest.main()
    