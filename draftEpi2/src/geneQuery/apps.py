from django.apps import AppConfig
# from dal.test.utils import OwnedFixtures
from django.db.models.signals import post_migrate

class GenequeryConfig(AppConfig):
    name = 'geneQuery'


class TestApp(AppConfig):
    name = 'linked_data'

    # def ready(self):
    #     post_migrate.connect(OwnedFixtures(), sender=self)
