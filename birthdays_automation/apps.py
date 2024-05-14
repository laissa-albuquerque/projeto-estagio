from django.apps import AppConfig

class BirthdaysConfig(AppConfig):
    name = 'birthdays_automation'

    def ready(self):
        import birthdays_automation.cleanup
