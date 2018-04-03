import unittest
from ..factories import build_tweet
from contrastes.processing import get_counters, merge_counters


class TwoUsersMergeCountersTest(unittest.TestCase):
    def setUp(self):
        tweets_one = [
            build_tweet(text="hola a todos", user_id="1"),
            build_tweet(text="#BuenViernes todos, hola a! Buen Viernes", user_id="2"),
        ]
        tweets_two = [
            build_tweet(text="a todos, hola", user_id="1"),
        ]

        fd1, users1 = get_counters(tweets_one)
        fd2, users2 = get_counters(tweets_two)

        self.fd, self.users = merge_counters([fd1, fd2], [users1, users2])

    def test_fds(self):
        self.assertEqual(dict(self.fd), {
            "a": 3,
            "hola": 3,
            "todos": 3,
            "buen": 1,
            "viernes": 1,
        })

    def test_users(self):
        self.assertEqual(self.users, {
            "a": {"1", "2"},
            "hola": {"1", "2"},
            "todos": {"1", "2"},
            "buen": {"2"},
            "viernes": {"2"},
        })
