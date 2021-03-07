import os
import requests
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import FormView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.core.files.base import ContentFile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from . import forms, models, mixins


class LoginView(mixins.LoggedOutOnlyView, FormView):

    """ Login View Definition """

    template_name = "users/login.html"
    form_class = forms.LoginForm

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
            messages.success(self.request, f"Welcome back {user.first_name}")
        return super().form_valid(form)

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse("core:home")


def log_out(request):
    messages.info(request, "See you later")
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(mixins.LoggedOutOnlyView, FormView):

    """ SignUp View Definition """

    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save(commit=False)
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
            messages.success(self.request, f"Welcome back {user.first_name}")
        user.verify_email()
        return super().form_valid(form)


def complete_verification(request, code):
    try:
        user = models.User.objects.get(code=code)
        user.verified = True
        user.code = ""
        user.save()
    except models.User.DoesNotExist:
        pass
    return redirect(reverse("core:home"))


class GithubException(Exception):
    pass


def github_login(request):
    client_id = os.environ.get("GITHUB_ID")
    return redirect(f"https://github.com/login/oauth/authorize?client_id={client_id}")


def github_callback(request):
    try:
        client_id = os.environ.get("GITHUB_ID")
        client_secret = os.environ.get("GITHUB_SECRET")
        code = request.GET.get("code", None)
        if code is not None:
            access_res = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )
            access_json = access_res.json()
            error = access_json.get("error", None)
            if error is not None:
                raise GithubException("Can't get access token")
            else:
                access_token = access_json.get("access_token")
                profile_res = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                    },
                )
                profile_json = profile_res.json()
                username = profile_json.get("login", None)
                if username is not None:
                    name = profile_json.get("name")
                    email = profile_json.get("email")
                    avatar_url = profile_json.get("avatar_url")
                    try:
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_GITHUB:
                            raise GithubException(
                                f"Please log in with {user.login_method}"
                            )
                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            username=email,
                            first_name=name,
                            email=email,
                            login_method=models.User.LOGIN_GITHUB,
                            verified=True,
                        )
                        user.set_unusable_password()
                        user.save()
                        if avatar_url is not None:
                            image_res = requests.get(avatar_url)
                            user.avatar.save(
                                f"{name}-avatar", ContentFile(image_res.content)
                            )
                    login(request, user)
                    messages.success(request, f"Welcome back {user.first_name}")
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException("Can't get your profile")
        else:
            raise GithubException("Can't get code")
    except GithubException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


class KakaoException(Exception):
    pass


def kakao_login(request):
    client_id = os.environ.get("KAKAO_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )


def kakao_callback(request):
    try:
        client_id = os.environ.get("KAKAO_ID")
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
        code = request.GET.get("code", None)
        if code is None:
            raise KakaoException()
        access_res = requests.post(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
        )
        access_json = access_res.json()
        error = access_json.get("error", None)
        if error is not None:
            raise KakaoException("Can't get authorization code")
        access_token = access_json.get("access_token")
        profile_res = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_res.json()
        email = profile_json.get("kakao_account").get("email", None)
        if email is None:
            raise KakaoException("Please give me your email")
        profile = profile_json.get("kakao_account").get("profile")
        name = profile.get("nickname")
        profile_image_url = profile.get("profile_image_url")
        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGIN_KAKAO:
                raise KakaoException(f"Please log in with {user.login_method}")
        except models.User.DoesNotExist:
            user = models.User.objects.create(
                username=email,
                first_name=name,
                email=email,
                login_method=models.User.LOGIN_KAKAO,
                verified=True,
            )
            user.set_unusable_password()
            user.save()
            if profile_image_url is not None:
                image_res = requests.get(profile_image_url)
                user.avatar.save(f"{name}-avatar", ContentFile(image_res.content))
        login(request, user)
        messages.success(request, f"Welcome back {user.first_name}")
        return redirect(reverse("core:home"))
    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


class ProfileView(DetailView):

    """ Profile View Definition """

    model = models.User
    context_object_name = "user_obj"


class EditProfileView(mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    """ EditProfile View Definition """

    model = models.User
    template_name = "users/edit-profile.html"
    fields = [
        "first_name",
        "last_name",
        "gender",
        "bio",
        "birthday",
        "language",
        "currency",
    ]
    success_message = "Profile Updated"

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["first_name"].widget.attrs = {"placeholder": "First name"}
        form.fields["last_name"].widget.attrs = {"placeholder": "Last name"}
        form.fields["bio"].widget.attrs = {"placeholder": "Bio"}
        form.fields["birthday"].widget.attrs = {"placeholder": "Birthday"}
        return form


class ChangePasswordView(
    mixins.LoggedInOnlyView,
    mixins.EmailLoginOnlyView,
    SuccessMessageMixin,
    PasswordChangeView,
):

    """ ChangePassword View Definition """

    template_name = "users/change-password.html"
    success_message = "Password Updated"

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["old_password"].widget.attrs = {"placeholder": "Current password"}
        form.fields["new_password1"].widget.attrs = {"placeholder": "New password"}
        form.fields["new_password2"].widget.attrs = {
            "placeholder": "Confirm new password"
        }
        return form

    def get_success_url(self):
        return self.request.user.get_absolute_url()


@login_required
def toggle_hosting(request):
    try:
        del request.session["is_hosting"]
    except KeyError:
        request.session["is_hosting"] = True
    return redirect(reverse("core:home"))
