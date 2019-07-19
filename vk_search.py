import datetime
import os
import requests
import logging
from dotenv import load_dotenv
from instagram_search import filter_comments_by_period


VK_NAME = 'cocacola'
VK_API = 'https://api.vk.com/method/'
API_V = 5.101
VK_PARAMS = {
    'v': API_V,
    'count': 100,
    'offset': 0,
}
PERIOD = 14

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
VK_LOGGER = logging.getLogger('VK Logger')


def get_group_id(token, vk_name, method='groups.getById'):
    VK_PARAMS.update({'group_id': vk_name, 'access_token': token})
    url = '{}{}'.format(VK_API, method)
    response = requests.get(url, params=VK_PARAMS).json()
    if 'error' in response:
        VK_LOGGER.error(response['error'])
        return None
    return -response['response'][0]['id']


def get_all_data(token, url, posts_limit=None):
    all_data = []
    offset, counter = 0, 1

    while offset < counter:
        VK_PARAMS.update({'offset': offset})
        response = requests.get(url, params=VK_PARAMS).json()
        if 'error' in response:
            return all_data

        data = response['response']['items']
        all_data.extend(data)
        counter = posts_limit or response['response']['count']
        offset += 100
    return all_data


def get_all_posts(token, vk_group_id, method='wall.get', posts_limit=None):
    VK_PARAMS.update(
        {'access_token': token, 'filter': 'owner', 'owner_id': vk_group_id})
    url = '{}{}'.format(VK_API, method)

    all_posts = get_all_data(token, url, posts_limit=posts_limit)

    return all_posts


def get_all_comments(token, vk_post_id, vk_group_id, method='wall.getComments'):
    VK_PARAMS.update(
        {'access_token': token, 'owner_id': vk_group_id, 'post_id': vk_post_id})
    url = '{}{}'.format(VK_API, method)

    all_comments = get_all_data(token, url)
    return all_comments


def get_filtered_comments(comments, days=PERIOD):
    all_comments = [(
        comment.get('from_id'),
        datetime.datetime.utcfromtimestamp(comment.get('date'))
    ) for comment in comments]
    filtered_comments = filter_comments_by_period(
        comments=all_comments,
        days=days,
        filter_index=1
    )
    return filtered_comments


def get_all_likers(token, vk_post_id, vk_group_id, method='likes.getList'):
    VK_PARAMS.update({
        'access_token': token,
        'owner_id': vk_group_id,
        'item_id': vk_post_id,
        'type': 'post',
        'filter': 'likes',
    })
    url = '{}{}'.format(VK_API, method)

    all_likers = get_all_data(token, url)
    return all_likers


def print_vk_most_active_users(group_name=VK_NAME, posts_limit=None):
    vk_token = os.getenv('VK_TOKEN')

    vk_group_id = get_group_id(vk_token, group_name)
    if vk_group_id is None:
        exit()

    active_commentators = []
    all_likers = []

    posts = get_all_posts(vk_token, vk_group_id)
    post_ids = [post['id'] for post in posts]
    for post_id in post_ids:
        comments = get_all_comments(vk_token, post_id, vk_group_id)
        filtered_comments = get_filtered_comments(comments)
        active_commentators.extend([user for user, time in filtered_comments])

        likers = get_all_likers(vk_token, post_id, vk_group_id)
        all_likers.extend(likers)
    most_active_users = set(active_commentators) & set(all_likers)
    print(
        f'Самые активные пользователи ВК за {PERIOD} дней:', most_active_users, sep='\n')


if __name__ == "__main__":
    load_dotenv()
    print_vk_most_active_users()
