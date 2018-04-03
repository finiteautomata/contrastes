import json
import tempfile

def build_tweet(text, user_id=111):
    return {
        "text": text,
        "user": {
            "id": str(user_id)
        }
    }

def build_tweet_file(tweets):
    """
    Build a .json containing given tweets
    """
    f = tempfile.NamedTemporaryFile(
        mode="w+", delete=False,
        prefix="tweets",
        suffix=".json")

    json.dump(tweets, f)

    f.close()
    return f.name
