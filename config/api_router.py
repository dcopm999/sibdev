from customers import views as customer_views
from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("customers", customer_views.CustomerViewSet)

app_name = "api"
urlpatterns = router.urls
