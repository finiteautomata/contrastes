def build_tweet(text, user_id=111):
    return {
        "text": text,
        "user": {
            "id": str(user_id)
        }
    }
