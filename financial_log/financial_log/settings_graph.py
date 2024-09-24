from .settings import *

TEST = True

INSTALLED_APPS += ['django_extensions']

GRAPH_MODELS = {
    'app_labels': [
        'calender_app', 'diary_app', 'statistics_app', 'user_app', 'wallet_app', 'wordcloud_app'
    ],
    'all_applications': True,
    'group_models': True
}