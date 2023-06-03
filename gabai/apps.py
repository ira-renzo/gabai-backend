from django.apps import AppConfig
from firebase_admin import credentials, initialize_app


class GabaiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gabai'

    def ready(self):
        cred = credentials.Certificate('serviceAccountKey.json')
        initialize_app(cred, {
            'databaseURL': "https://gabai-44874-default-rtdb.asia-southeast1.firebasedatabase.app/"
        })