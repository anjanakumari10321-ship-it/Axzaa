import os

class Config(object):
    BOT_TOKEN = os.environ.get("BOT_TOKEN", '9173305278:AAEHBCzbJfLinhxRYCb-BizLbK4mGTEiHw4')
    API_ID = int(os.environ.get("API_ID", '33490515'))
    API_HASH = os.environ.get("API_HASH", '378e1c46ebe4f29292a91260866df8a4')
    AUTH_USER = os.environ.get('AUTH_USERS', '732392395').split(',')
    AUTH_USERS = [int(user_id) for user_id in AUTH_USER]
    HOST = "https://drm-api-six.vercel.app"
    CREDIT = "SBA™"#Here You Can Change with Your Name  or any custom name or title you prefer
