from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
# AUTHENTICATION
router.register(r'auth/login', views.LoginViewSet, basename='auth-login')
router.register(r'auth/register', views.RegistrationViewSet,
                basename='auth-register')
router.register(r'auth/refresh', views.RefreshViewSet, basename='auth-refresh')

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.home, name='home'),
    path('sort/<query>', views.sort, name='sort'),
    # path('', views.ProductListView.as_view(), name='home'),
    path('search/<query>', views.search, name='search'),
    path('post/<id>/', views.post, name='post'),
    path('profile/<username>/', views.profile, name='profile'),
    path('saved/', views.saved, name='saved'),
    path('menu/', views.menu, name='menu'),
    path('map/', views.map, name='map'),
    path('user-add-post/', views.user_add_post, name='user_add_post'),
    path('load-data/', views.load_data, name='load-data'),
    path('load-username/', views.load_username, name='load_username'),
    path('profile-data/', views.profile_data, name='profile_data'),
    path('search-data/', views.search_data, name='search_data'),
    path('home-data/', views.home_data, name='home_data'),
    path('post-data/', views.post_data, name='post_data'),
    path('like-view/', views.like_view, name='like_view'),

    path('user-auth/', views.user_auth, name='user_auth'),
    path('get-coord/', views.get_coord, name='get-coord'),

    path('map-state/', views.map_state, name='map-state'),
    path('save-to-gemme/', views.save_to_gemme, name='save-to-gemme'),

    # react added
    path('api/feed/', views.feed, name='feed'),
    path('api/user/', views.user),
    path('api/saved-view/', views.saved_view),
    path('api/coords/', views.coords, name='coords'),


    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/checked/', views.dashboard_is_checked,
         name='dashboard_is_checked'),
    path('dashboard/ads/', views.dashboard_is_ad, name='dashboard_is_ad'),

    path('accounts/activate/<uidb64>/<token>', views.account_activate, name='account_activate'),

    path('accounts/login/', views.sign_in, name='login'),
    path('accounts/signup/', views.sign_up, name='signup'),
    path('accounts/logout/', views.sign_out, name='logout'),
]
