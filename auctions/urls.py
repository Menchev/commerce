from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing_view, name="create_listing"),
    path("listing/<int:id>", views.listing_view, name="listing"),
    path("bid_update", views.bid_update, name="bid_update"),
    path("watchlist", views.watchlist_view, name="watchlist"),
]
