from django.urls import include, path
from rest_framework import routers
from . import views
from django.http import HttpResponse
from django.views.generic import TemplateView

router = routers.DefaultRouter()
router.register(r'gamers', views.GamersViewSet, basename='Gamer')
router.register(r'games', views.GamesViewSet, basename='Game')
router.register(r'question', views.GamerQuestionViewSet, basename='GamerQuestion')
router.register(r'answers', views.AnswerViewSet, basename='Answer')
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

def smpl(rq):
    return HttpResponse("Redirect to Front `Create Game and Gamer` Api")

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/reg', include('rest_auth.registration.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('glogin', views.GLogin),
    path('api/', include(router.urls)),
    path('front', smpl)#lambda rq : HttpResponse("Redirect to Front `Create Game and Gamer` Api"))
]


#path('rest-auth/google', views.GoogleLogin.as_view(), name='gg_login'),
#path('glogin', TemplateView.as_view(template_name="index.html")),
