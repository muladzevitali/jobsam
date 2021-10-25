from unittest import TestCase
import os

import redis


class TestRedisConnection(TestCase):
    def setUp(self) -> None:
        self.connection = redis.Redis(host=os.environ.get('REDIS_HOST'), port=os.environ.get('REDIS_PORT'), db=0,
                                      password=os.environ.get('REDIS_PASSWORD'))

    def test_set(self):
        print('Testing redis connection', self.connection.connection_pool)
        self.connection.set('test', 1)
        self.assertEqual(self.connection.get('test'), b'1')
