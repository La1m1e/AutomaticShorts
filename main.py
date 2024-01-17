import threading
import praw
from audio import ttsaudio
from video import video
from subtitles import subtitles
from YTUpload import upload
from getcredentials import credentials
from webinterface import *
threading.Thread(target=openchrome).start()
print('Browser thread started')
file_pathc = 'credentials.txt'
if not os.path.isfile(file_pathc):
    with open(file_pathc, 'w') as file:
        file.write("reddit_client_id:\nreddit_client_secret:\nreddit_username:\nreddit_password:\nreddit_user_agent"
                   ":\nelevenlabs_api_key:\nwhisperapi_key:\nopenai_api_key:")

upvoted_post_ids_file = 'upvoted_post_ids.txt'
downvoted_post_ids_file = 'downvoted_post_ids.txt'

reddit = praw.Reddit(
    client_id=credentials('reddit_client_id'),
    client_secret=credentials('reddit_client_secret'),
    username=credentials('reddit_username'),
    password=credentials('reddit_password'),
    user_agent=credentials('reddit_user_agent')
)


def get_new_votes():
    upvoted_posts = []
    downvoted_posts = []

    for submission in reddit.user.me().upvoted(limit=1):
        upvoted_posts.append(submission)

    for submission in reddit.user.me().downvoted(limit=1):
        downvoted_posts.append(submission)

    return upvoted_posts, downvoted_posts


def get_post_info(submission, include_top_comment=True):
    post_info = {
        'title': submission.title,
        'text': submission.selftext,
        'top_comment': None
    }

    if include_top_comment:
        submission.comments.replace_more(limit=0)
        top_comment = get_top_comment(submission.comments.list())
        post_info['top_comment'] = top_comment.body if top_comment else None

    return post_info


def get_top_comment(comments):
    non_bot_comments = [comment for comment in comments if not is_bot(comment)]

    if non_bot_comments:
        return max(non_bot_comments, key=lambda comment: comment.ups, default=None)

    return None


def is_bot(comment):
    return comment.author and "bot" in comment.author.name.lower()


def load_vote_post_ids(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return set(file.read().splitlines())
    return set()


def save_vote_post_ids(file_path, vote_post_ids):
    with open(file_path, 'w') as file:
        file.write('\n'.join(vote_post_ids))


def process_all(title, text, comment):
    ttsaudio(title, text, comment)
    time.sleep(1)
    video()
    time.sleep(1)
    subtitles()
    time.sleep(1)


def main():
    upvoted_post_ids = load_vote_post_ids(upvoted_post_ids_file)
    downvoted_post_ids = load_vote_post_ids(downvoted_post_ids_file)
    while True:
        upvoted_posts, downvoted_posts = get_new_votes()
        for submission in upvoted_posts:
            post_id = submission.id

            if post_id not in upvoted_post_ids:
                upvoted_post_ids.add(post_id)
                save_vote_post_ids(upvoted_post_ids_file, upvoted_post_ids)

                post_info = get_post_info(submission)

                title = post_info['title']
                text = post_info['text']
                comment = 'Subscribe for more'
                process_all(title, text, comment)
                upload(title, text, comment)

        for submission in downvoted_posts:
            post_id = submission.id
            if post_id not in downvoted_post_ids:
                downvoted_post_ids.add(post_id)
                save_vote_post_ids(downvoted_post_ids_file, downvoted_post_ids)

                post_info = get_post_info(submission, include_top_comment=True)

                title = post_info['title']
                text = post_info['text']
                comment = post_info['top_comment'] + '<break time="0.8s" /> subscribe for more'
                process_all(title, text, comment)
                upload(title, text, comment)
        time.sleep(10)


if __name__ == "__main__":
    main()
