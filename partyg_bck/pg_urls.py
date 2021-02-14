from django.urls import include, path
from rest_framework import routers
from django.views.generic import TemplateView
from . import views

router = routers.DefaultRouter()
router.register(r'gamers', views.GamersViewSet)
router.register(r'games', views.GamesViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/reg', include('rest_auth.registration.urls')),

    #path('rest-auth/google', views.GoogleLogin.as_view(), name='gg_login'),
    #path('glogin', TemplateView.as_view(template_name="index.html")),
    path('glogin', views.GLogin),
    path('', views.MySocialLogin),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]