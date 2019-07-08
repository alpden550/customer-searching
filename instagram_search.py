import datetime
import os
from collections import Counter
from instabot import Bot
from dotenv import load_dotenv


SEARCH = 'cocacolarus'
PERIOD = 90


def create_bot():
    login = os.getenv('INST_LOGIN')
    password = os.getenv('INST_PSWRD')
    bot = Bot()
    bot.login(username=login, password=password)
    return bot


def get_comments_from_post(bot, post):
    comments = []
    for raw_comment in bot.get_media_comments_all(post):
        user_id = raw_comment.get('user_id')
        time_created = datetime.datetime.utcfromtimestamp(raw_comment.get('created_at_utc'))
        comments.append([user_id, time_created])
    return comments


def filter_comments_by_period(comments, days, filter_index=1):
    today = datetime.datetime.now().replace(microsecond=0)
    period = datetime.timedelta(days=days)
    old_date = today - period

    return list(filter(lambda x: x[filter_index] >= old_date, comments))


def print_top_posts_and_comments(search=SEARCH, period=PERIOD):
    bot = create_bot()
    all_posts = bot.get_total_user_medias(search)
    all_comments = []
    post_comments = {}

    for post in all_posts:
        comments = get_comments_from_post(bot, post)
        filtered_comments = filter_comments_by_period(comments, period)
        if len(filtered_comments) > 0:
            post_comments[post] = len(filtered_comments)
        all_comments.extend([comment[0] for comment in filtered_comments])

    commentators = dict(Counter(all_comments))
    print(f'Пост : количество комментариев за последние {PERIOD} дней:', post_comments, sep='\n')
    print()
    print(f'Комментатор : количество комментариев за последние {PERIOD} дней:', commentators, sep='\n')


if __name__ == "__main__":
    load_dotenv()
    print_top_posts_and_comments()
