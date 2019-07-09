import argparse
from dotenv import load_dotenv
from instagram_search import print_top_posts_and_comments
from vk_search import print_most_active_users


def create_parser():
    parser = argparse.ArgumentParser(description='Find top comments and commentators in social network')
    parser.add_argument('social', type=str, help='Social network for searching(instagram, vk or facebook)')
    return parser.parse_args()


if __name__ == "__main__":
    load_dotenv()
    parser = create_parser()
    soc_network = parser.social
    if soc_network == 'instagram':
        print_top_posts_and_comments()
    elif soc_network == 'vk':
        print_most_active_users()
