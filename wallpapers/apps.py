from django.apps import AppConfig


class WallpapersConfig(AppConfig):
    name = 'wallpapers'

    def ready(self):
        import wallpapers.signals  # noqa
