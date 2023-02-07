from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import CreateView, UpdateView

from .forms import SignupForm, LoginForm, ProfileForm, PswdChgForm, DriverForm, RideRequestForm, SharerForm
from .models import Driver, Ride, Sharer
from django.core.mail import send_mail
from naive_uber import settings
# Create your views here.


################################ WELCOME #########################################
def welcomeView(request):
    return render(request, "basic/welcome.html")


################################ SIGN UP/IN #########################################
def signupView(request):
    # POST
    if request.method == "POST":
        form = SignupForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            confirm_password = form.cleaned_data['password2']
            email = form.cleaned_data['email']
            if password == confirm_password:
                user = User.objects.create_user(
                    username=username, email=email, password=password)
                user.save()
                return HttpResponseRedirect(reverse("basic:login_page"))
            form.add_error("confirm_password", "Passwords didn't match")
        context = {"form": form, "title": "Sign up"}
        return render(request, "basic/submit_form.html", context)
    # GET
    form = SignupForm()
    context = {"form": form, "title": "Sign up"}
    return render(request, "basic/submit_form.html", context)


def loginView(request):
    # POST
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("basic:welcome_page"))
            form.add_error("password", "Invalid username or password")
        context = {"form": form, "title": "Login"}
        return render(request, "basic/submit_form.html", context)
    # GET
    form = LoginForm()
    context = {"form": form, "title": "Login"}
    return render(request, "basic/submit_form.html", context)


@login_required
def logoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse("basic:welcome_page"))


################################ PROFILE #########################################
@login_required
def profileView(request):
    if hasattr(request.user, 'driver'):
        driver = request.user.driver
    else:
        driver = None
    context = {"user": request.user, "driver": driver}
    return render(request, "basic/profile.html", context)


class UpdateProfile(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = User
    form_class = ProfileForm
    template_name = "basic/submit_form.html"
    success_url = reverse_lazy("basic:profile_page")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Profile update"
        return context

    def get_success_url(self):
        if hasattr(self.request.user, 'driver'):
            self.request.user.driver.first_name = self.request.user.first_name
            self.request.user.driver.last_name = self.request.user.last_name
            self.request.user.driver.save()
        return reverse_lazy("basic:profile_page")


class PswdChgView(LoginRequiredMixin, PasswordChangeView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    form_class = PswdChgForm
    template_name = "basic/submit_form.html"
    success_url = reverse_lazy("basic:profile_page")

################################ DRIVER REGISTRATION #########################################


class AddDriver(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Driver
    form_class = DriverForm
    template_name = "basic/submit_form.html"
    # success_url = reverse_lazy("basic:profile_page")

    def get_initial(self):
        return {
            'user': self.request.user,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Driver registration"
        return context

    def get_success_url(self):
        self.request.user.first_name = self.object.first_name
        self.request.user.last_name = self.object.last_name
        self.request.user.save()
        return reverse_lazy("basic:profile_page")


class UpdateDriver(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Driver
    form_class = DriverForm
    template_name = "basic/submit_form.html"
    # success_url = reverse_lazy("basic:profile_page")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Vehicle Info"
        return context

    def get_success_url(self):
        self.request.user.first_name = self.object.first_name
        self.request.user.last_name = self.object.last_name
        self.request.user.save()
        return reverse_lazy("basic:profile_page")


@login_required
def deleteDriverView(request):
    if request.method == "POST":
        request.user.driver.delete()
        return HttpResponseRedirect(reverse("basic:profile_page"))
    return HttpResponse("no POST request")


################################ RIDE OWNER #########################################
@login_required
def ownerRideView(request):
    ride_set = request.user.ride_set.all()
    return render(request, "basic/ride_index.html", {"ride_set": ride_set})


class AddRide(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Ride
    form_class = RideRequestForm
    template_name = "basic/submit_form.html"
    success_url = reverse_lazy("basic:ride_page")

    def get_initial(self):
        return {
            'owner': self.request.user,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Request ride"
        return context


class UpdateRide(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Ride
    form_class = RideRequestForm
    template_name = "basic/submit_form.html"
    # success_url = reverse_lazy("basic:ride_detail")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Ride update"
        return context

    def get_success_url(self):
        if (self.object.is_shared == 1):
            for sharer in self.object.sharer_set.iterator():
                sharer.delete()
        return reverse_lazy("basic:ride_detail", kwargs={'ride_id': self.object.id})


@login_required
def deleteRideView(request):
    if request.method == "POST":
        obj = request.user.ride_set.get(pk=request.POST["ride_id"])
        obj.delete()
        return HttpResponseRedirect(reverse("basic:ride_page"))
    return HttpResponse("no POST request")


################################ RIDE DRIVE #########################################
@login_required
def driverRideView(request):
    request_GET = request.GET.dict()
    if hasattr(request.user, 'driver'):
        driver = request.user.driver
    else:
        return HttpResponseRedirect(reverse("basic:driver_register"))

    uncomplete_ride_set = driver.ride_set.filter(status=2)
    open_ride_set = Ride.objects.exclude(owner=request.user, pk__in=getJoinedShareRideIDs(request))\
        .filter(status=1, passengers__lte=driver.capacity, veh_type__in=[driver.veh_type, 0])

    context = {"uncomplete_ride_set": uncomplete_ride_set,
               "open_ride_set": open_ride_set}
    return render(request, "basic/drive_index.html", context)


@login_required
def claimRideView(request):
    if request.method == "POST":
        ride = Ride.objects.get(pk=request.POST["ride_id"])
        if request.user.driver.capacity >= ride.passengers:
            ride.driver = request.user.driver
            ride.status = 2
            ride.save()
            subject = 'Naive_Uber Request Confirmed'
            message = 'Hi!\n\nThe ride from '+ride.start_point+' to '+ride.destination+' at ' + \
                str(ride.req_arrival_time) + \
                ' has been confirmed!\n\nEnjoy your journey!\n\nNaive_Uber'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [ride.owner.email]
            send_mail(subject, message, from_email,
                      recipient_list, fail_silently=False,)
            for sharer in ride.sharer_set.iterator():
                recipient_list = [sharer.user.email]
                send_mail(subject, message, from_email,
                          recipient_list, fail_silently=False,)
            return HttpResponseRedirect(reverse_lazy("basic:drive_page"))
        return HttpResponse("Your car is too small!")
    return HttpResponse("no POST request")


@login_required
def completeRideView(request):
    if request.method == "POST":
        ride = Ride.objects.get(pk=request.POST["ride_id"])
        ride.status = 3
        ride.save()
        return HttpResponseRedirect(reverse_lazy("basic:drive_page"))
    return HttpResponse("no POST request")


################################ RIDE SHARE #########################################
def custom_filter(request_dict, query_set):
    if (request_dict.get("destination") != None and request_dict.get("destination") != ""):
        query_set = query_set.filter(
            destination__contains=request_dict["destination"])

    if (request_dict.get("filter_time_gt") != None and request_dict.get("filter_time_gt") != ""):
        query_set = query_set.filter(
            req_arrival_time__gt=request_dict["filter_time_gt"])

    if (request_dict.get("filter_time_lt") != None and request_dict.get("filter_time_lt") != ""):
        query_set = query_set.filter(
            req_arrival_time__lt=request_dict["filter_time_lt"])

    if (request_dict.get("fiter_passengers") != None and request_dict.get("fiter_passengers") != ""):
        query_set = query_set.filter(
            passengers__exact=request_dict["fiter_passengers"])

    type_kv = {"Hatchback": 1, "MPV": 2, "Pickup": 3,
               "Sedan": 4, "Sports": 5, "SUV": 6, "other": 7}
    if (request_dict.get("filter_type") != None and request_dict.get("filter_type") != "" and request_dict.get("filter_type") != "Any"):
        query_set = query_set.filter(
            veh_type__exact=type_kv[request_dict["filter_type"]])

    binary_kv = {"No": 1, "Yes": 2}
    if (request_dict.get("fiter_is_shared") != None and request_dict.get("fiter_is_shared") != ""):
        query_set = query_set.filter(
            is_shared__exact=binary_kv[request_dict["fiter_is_shared"]])

    return query_set


def getJoinedShareRideIDs(request):
    all_sharers = request.user.sharer_set.iterator()
    joined_share_ride_ids = []
    for sharer in all_sharers:
        joined_share_ride_ids.append(sharer.ride.id)
    return joined_share_ride_ids


@login_required
def sharerRideView(request):
    joined_share_ride_set = Ride.objects.filter(
        pk__in=getJoinedShareRideIDs(request))
    joined_uncomplete_share_ride_set = joined_share_ride_set.exclude(status=3)

    open_share_ride_set = Ride.objects.exclude(owner=request.user).filter(
        is_shared=2).filter(status=1)
    if hasattr(request.user, 'driver'):
        open_share_ride_set = open_share_ride_set.exclude(
            driver=request.user.driver)

    request_GET = request.GET.dict()
    if (request_GET.get("search") != None):
        open_share_ride_set = custom_filter(request_GET, open_share_ride_set)
    if (request_GET.get("reset") != None):
        return HttpResponseRedirect(reverse_lazy("basic:share_page"))

    # Calling QuerySet.filter() after difference() is not supported.
    open_share_ride_set = open_share_ride_set.difference(joined_share_ride_set)

    context = {"joined_uncomplete_share_ride_set": joined_uncomplete_share_ride_set,
               "open_share_ride_set": open_share_ride_set}
    return render(request, "basic/share_index.html", context)


@login_required
def joinRideView(request):
    if request.method == "POST":
        form = SharerForm(data=request.POST)
        if form.is_valid() and form.cleaned_data["party_passengers"] > 0:
            ride = Ride.objects.get(pk=form.cleaned_data["ride_id"])
            sharer = Sharer(user=request.user, ride=ride,
                            party_passengers=form.cleaned_data["party_passengers"])
            ride.passengers = ride.passengers + sharer.party_passengers
            ride.save()
            sharer.save()
            return HttpResponseRedirect(reverse_lazy("basic:share_page"))
    else:
        form = SharerForm(initial={"ride_id": request.GET["ride_id"]})
    context = {"form": form, "title": "Input your party passengers"}
    return render(request, "basic/submit_form.html", context)


@login_required
def exitRideView(request):
    if request.method == "POST":
        ride = Ride.objects.get(pk=request.POST["ride_id"])
        sharer = ride.sharer_set.get(user=request.user)
        ride.passengers = ride.passengers - sharer.party_passengers
        # ride.sharer_set.remove(sharer)
        sharer.delete()
        ride.save()
        return HttpResponseRedirect(reverse_lazy("basic:share_page"))
    return HttpResponse("no POST request")


################################ DETAIL #########################################
@login_required
def showRideDetialView(request, ride_id):
    ride = Ride.objects.get(pk=ride_id)
    context = {"ride": ride}
    return render(request, "basic/ride_detail.html", context)
