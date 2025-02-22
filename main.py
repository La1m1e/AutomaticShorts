import praw
import json
import time
import os
from dotenv import load_dotenv

import TextHandler

# Reddit API credentials (replace with your own)
load_dotenv()
SEEN_UPVOTES = "seen_upvotes.json"

# Load previously seen upvotes
def load_seen_upvotes():
    try:
        with open(SEEN_UPVOTES, "r") as file:
            return set(json.load(file))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()

def save_seen_upvotes(upvote_ids):
    with open(SEEN_UPVOTES, "w") as file:
        json.dump(list(upvote_ids), file)

# Authenticate with Reddit
def authenticate():
    return praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        username=os.getenv("REDDIT_USERNAME"),
        password=os.getenv("REDDIT_PASSWORD"),
        user_agent=os.getenv("USER_AGENT"),
        redirect_uri="http://localhost:8080",
    )

# Get newly upvoted posts
def get_new_upvotes(reddit):
    seen_upvotes = load_seen_upvotes()
    new_upvotes = []

    for post in reddit.user.me().upvoted(limit=1):  # Fetch latest 10 upvoted posts
        if post.id not in seen_upvotes:
            new_upvotes.append(post)
            seen_upvotes.add(post.id)

    save_seen_upvotes(seen_upvotes)
    return new_upvotes

# Main loop
def main():
    reddit = authenticate()
    print("Bot started...")

    while True:
        new_upvotes = get_new_upvotes(reddit)

        if new_upvotes:
            for post in new_upvotes:
                TextHandler.text(f"{post.title} {post.selftext}")
        time.sleep(5)

if __name__ == "__main__":
    main()
