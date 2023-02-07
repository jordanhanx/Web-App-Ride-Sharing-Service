from django.urls import path

from . import views

app_name = "basic"
urlpatterns = [
    path("", views.welcomeView, name="welcome_page"),

    path("signup/", views.signupView, name="signup_page"),
    path("login/", views.loginView, name="login_page"),
    path("logout/", views.logoutView, name="logout_page"),

    path("profile/", views.profileView, name="profile_page"),
    path("profile/<int:pk>/update",
         views.UpdateProfile.as_view(), name="profile_update"),
    path("password/", views.PswdChgView.as_view(), name="change_password"),

    path("driver/register/", views.AddDriver.as_view(), name="driver_register"),
    path("driver/<int:pk>/update",
         views.UpdateDriver.as_view(), name="driver_update"),
    path("driver/delete/", views.deleteDriverView, name="driver_delete"),

    path("ride/", views.ownerRideView, name="ride_page"),
    path("ride/add/", views.AddRide.as_view(), name="ride_add"),
    path("ride/<int:pk>/update/", views.UpdateRide.as_view(), name="ride_update"),
    path("ride/delete/", views.deleteRideView, name="ride_delete"),
    path("ride/<int:ride_id>/detail/",
         views.showRideDetialView, name="ride_detail"),


    path("drive/", views.driverRideView, name="drive_page"),
    path("drive/claim/", views.claimRideView, name="claim_ride"),
    path("drive/complate/", views.completeRideView, name="complete_ride"),


    path("share/", views.sharerRideView, name="share_page"),
    path("share/join/", views.joinRideView, name="join_ride"),
    path("share/exit/", views.exitRideView, name="exit_ride")
]
