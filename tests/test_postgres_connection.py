import psycopg2
import os
from unittest import TestCase


class TestPostgresConnection(TestCase):
    def setUp(self) -> None:
        self.uri = "dbname='%s' user='%s' host='%s' password='%s' connect_timeout=1" % (os.environ.get('POSTGRES_DB'),
                                                                                        os.environ.get('POSTGRES_USER'),
                                                                                        os.environ.get('POSTGRES_HOST'),
                                                                                        os.environ.get(
                                                                                            'POSTGRES_PASSWORD'),
                                                                                        )

    def test_postgres_connection(self):
        print('Testing postgres connection', )
        try:
            conn = psycopg2.connect(self.uri)
            conn.close()
            print(conn)
            return True
        except psycopg2.OperationalError:
            raise ConnectionError('Error connecting to postgres')
