from django.contrib.auth import logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from .serializers import (
    RegisterUserSerializer,
    EmailConfirmSerializer,
    LoginSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer,
)


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.save()
            domain = get_current_site(request).domain
            confirmation_link = (
                f"http://{domain}/authentication/confirm_email/{user_data['token']}"
            )
            send_mail(
                "Welcome to Videoflix",
                f"Follow this link to confirm your email: {confirmation_link}",
                "mail@niels-scholz.com",
                [user_data["user"].email],
                fail_silently=False,
            )
            return Response(
                {
                    "message": "User created successfully. Please check your email to confirm your account."
                }
            )
        else:
            return Response({"error": serializer.errors}, status=400)


class ConfirmEmailView(APIView):
    def get(self, request, token):
        serializer = EmailConfirmSerializer(data={"token": token})
        if serializer.is_valid():
            return HttpResponseRedirect(
                "https://niels-scholz.com/videoflix-frontend/login"
            )
        else:
            return Response({"error": serializer.errors}, status=400)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data)
        else:
            return Response({"error": serializer.errors}, status=400)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful."})


class PasswordResetView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            reset_data = serializer.save()
            reset_link = f"http://localhost:4200/resetpassword/{reset_data['uid']}/{reset_data['token']}/"
            subject = "Password Reset"
            html_message = f'<p>Password reset link: <a href="{reset_link}">Click here to reset your password</a></p>'
            email = EmailMessage(
                subject,
                html_message,
                "mail@niels-scholz.com",
                [request.data.get("email")],
            )
            email.content_subtype = "html"
            email.send()
            return Response({"detail": "Password reset email has been sent."})
        else:
            return Response({"error": serializer.errors}, status=400)


class PasswordResetConfirmView(APIView):
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.save())
        else:
            return Response({"error": serializer.errors}, status=400)


...
