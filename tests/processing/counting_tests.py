import unittest
from contrastes.processing import get_counters

def build_tweet(text, user_id=111):
    return {
        "text": text,
        "user": {
            "id": str(user_id)
        }
    }

class GetCountersTest(unittest.TestCase):
    def test_one_tweet_generate_freqdist_counts(self):
        tweets = [build_tweet("hola a todos, hola", user_id="1234")]

        fd, _ = get_counters(tweets)

        self.assertEqual(dict(fd), {
            "a": 1,
            "hola": 2,
            "todos": 1,
        })

    def test_one_tweet_generate_users_dict(self):
        tweets = [build_tweet("hola a todos, hola", user_id="1234")]

        _, users = get_counters(tweets)

        self.assertDictEqual(users, {
            "hola": {"1234"},
            "a": {"1234"},
            "todos": {"1234"}
        })

    def test_two_tweets_frequency(self):
        tweets = [
            build_tweet("hola a todos, hola #BuenMiercoles", user_id="1234"),
            build_tweet("hola amigos especialmente a @johndoe",
                        user_id="12345")
        ]

        fd, _ = get_counters(tweets)

        self.assertEqual(dict(fd), {
            "a": 2,
            "hola": 3,
            "todos": 1,
            "amigos": 1,
            "especialmente": 1
        })

    def test_two_tweets_users(self):
        tweets = [
            build_tweet("hola a todos, hola #BuenMiercoles", user_id="1234"),
            build_tweet("hola amigos especialmente a @johndoe",
                        user_id="12345")
        ]

        _, users = get_counters(tweets)

        self.assertDictEqual(users, {
            "hola": {"1234", "12345"},
            "a": {"1234", "12345"},
            "todos": {"1234"},
            "especialmente": {"12345"},
            "amigos": {"12345"},
        })
