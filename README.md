# Seaching the most active users in FB, Instagram and VK

This script can find out the most active users in three social networks: VK, Facebook, and Instagram.
The searching period on Instagram 90 days, on VK – 14 days, on Facebook 30 days.

## How to install

1. You have to have Instagram account.

2. Get VK's [service key](https://vk.com/dev/access_token?f=3.%20Сервисный%20ключ%20доступа)

3. Create FB's application and get [access token](https://developers.facebook.com/tools/explorer/)

Create file .env in the root and write in it:

```.env
INST_LOGIN = your Instagram login
INST_PSWRD = your Instagram password
VK_TOKEN=vk's group token
FB_TOKEN=fb's application token
```

Python3 must be already installed.

Should use virtual env for project isolation.

Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:

```bash
pip install -r requirements.txt
```

## How to use

Run scripts in terminal with correct argument (`vk`, `instagram`, `facebook`)

```bash
python customer_search.py facebook
```

## Output example

```bash
Комментаторы за 30 дней:
{'2582914478431232'}
Реакции пользователей:
{'2582914478431232': {'ANGRY': 2, 'SAD': 2}}
```

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
