from django.apps import AppConfig


class CommunicationsConfig(AppConfig):
    name = 'fix_the_news.communications'

    def ready(self):
        """ method just to import the signals """
        import fix_the_news.communications.signals
