import os
from urllib.parse import urlparse, parse_qsl
from collections import Counter
import requests
import datetime
import logging
from dotenv import load_dotenv
from instagram_search import filter_comments_by_period


FB_GROUP_ID = 379834139328901
FB_API = 'https://graph.facebook.com/v3.3/'
PERIOD = 30

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
FB_LOGGER = logging.getLogger('FB Logger')


def get_url_params(url):
    parameters = urlparse(url).query
    return dict(parse_qsl(parameters))


def get_all_posts(token):
    parameters = {
        'access_token': token,
    }
    url = f'{FB_API}{FB_GROUP_ID}/feed'
    posts = []
    response = requests.get(url, params=parameters).json()
    if 'error' in response:
        FB_LOGGER.error(response['error'])
        return []
    posts.extend(response['data'])

    while True:
        if not response['data']:
            break
        url_next = response.get('paging').get('next')
        parameters.update(get_url_params(url_next))
        response = requests.get(url, params=parameters).json()
        posts.extend(response['data'])

    return posts


def get_data_from_post(token, post_id, method):
    url = f'{FB_API}{post_id}/{method}'
    parameters = {
        'access_token': token,
    }
    response = requests.get(url, params=parameters).json()

    if 'error' in response:
        FB_LOGGER.error(response['error'])
        return []
    return response['data']


def get_filtered_commentators(comments_list, days=PERIOD):
    users = []
    for comment in comments_list:
        if comment.get('from'):
            users.append(
                (comment['from']['id'],
                 datetime.datetime.strptime(comment['created_time'], '%Y-%m-%dT%H:%M:%S+0000'))
            )

    filtered_users = filter_comments_by_period(users, days)
    return set([user for user, time in filtered_users])


def count_reactions(reactions):
    users = {}
    for reaction in reactions:
        user = reaction.get('id')
        user_reactions = reaction.get('type')
        if user not in users:
            users[user] = [user_reactions]
        else:
            users[user].append(user_reactions)

    for user_id in users:
        users[user_id] = dict(Counter(users[user_id]))

    return users


def print_fb_most_active_users():
    fb_token = os.getenv('FB_TOKEN')
    all_comments = []
    all_reactions = []

    posts = get_all_posts(fb_token)
    if not posts:
        exit()

    post_ids = [post['id'] for post in posts]
    for post_id in post_ids:
        post_comments = get_data_from_post(fb_token, post_id, 'comments')
        all_comments.extend(post_comments)

        post_reactions = get_data_from_post(fb_token, post_id, 'reactions')
        all_reactions.extend(post_reactions)

    active_users = get_filtered_commentators(all_comments)
    print(f'Комментаторы за {PERIOD} дней:', active_users, sep='\n')
    active_reacters = count_reactions(all_reactions)
    print(f'Реакции пользователей:', active_reacters, sep='\n')


if __name__ == "__main__":
    load_dotenv()
    print_fb_most_active_users()
