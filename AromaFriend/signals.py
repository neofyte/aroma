import django.dispatch


relationship_created = django.dispatch.Signal(providing_args=["relationship"])