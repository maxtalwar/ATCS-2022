import pytest
from models import User, Tag, Tweet
import twitter as t

# test functions
def test_user_repr():
    user = User(username="test_user", password="test_password")
    assert user.__repr__() == "@test_user"

def test_tag_repr():
    tag = Tag(id=1, content="example_tag")
    assert tag.__repr__() == "#example_tag"

def test_tweet_repr():
    user = User(username="BillGates", password="example_password")
    tweet = Tweet(id=1, content="Hello World!", user=user, timestamp="2023-03-21 19:59:05.353242")
    tweet.tags = [Tag(id=1, content="hello"), Tag(id=2, content="woo"), Tag(id=3, content="first")]
    assert tweet.__repr__() == "@BillGates\nHello World!\n#hello #woo #first\n2023-03-21 19:59:05.353242"