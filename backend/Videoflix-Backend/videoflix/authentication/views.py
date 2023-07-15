from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import EmailValidator
from django.contrib.auth import logout


class RegisterView(APIView):
    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        password_again = request.data.get("password_again")

        # Überprüfen, ob alle Felder gesetzt sind
        if not username or not email or not password or not password_again:
            return Response({"error": "All fields are required."}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username is already taken."}, status=400)

        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "An account with this email already exists."}, status=400
            )

        if password != password_again:
            return Response({"error": "Passwords do not match."}, status=400)

        try:
            # Überprüfen Sie die Stärke des Passworts
            validate_password(password, user=User)
        except DjangoValidationError as e:
            return Response({"error": e.messages}, status=400)

        email_validator = EmailValidator()

        try:
            # Überprüfen Sie die Gültigkeit der E-Mail-Adresse
            email_validator(email)
        except DjangoValidationError:
            return Response({"error": "Invalid email address."}, status=400)

        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        user.is_active = (
            False  # Set the user to inactive until they have confirmed their email
        )
        user.save()

        confirmation_token = default_token_generator.make_token(user)

        # Generieren Sie einen Bestätigungslink
        domain = get_current_site(request).domain
        confirmation_link = "http://{}/authentication/confirm_email/{}".format(
            domain, confirmation_token
        )

        # Senden Sie eine E-Mail an den Benutzer mit dem Bestätigungslink
        send_mail(
            "Welcome to Videoflix",
            "Follow this link to confirm your email: {}".format(confirmation_link),
            "mail@niels-scholz.com",
            [email],
            fail_silently=False,
        )

        return Response(
            {
                "message": "User created successfully. Please check your email to confirm your account."
            }
        )


class ConfirmEmailView(APIView):
    def get(self, request, token):
        token_generator = PasswordResetTokenGenerator()

        for user in User.objects.filter(is_active=False):
            if token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                return Response(
                    {"message": "Email confirmed successfully. You can now login."}
                )

        return Response({"error": "Invalid token."}, status=400)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        # Find the user with the given email
        user = User.objects.filter(email=email).first()

        if user is not None:
            if user.is_active:
                # Authenticate the user using the email and password
                authenticated_user = authenticate(
                    request, username=user.username, password=password
                )

                if authenticated_user is not None:
                    # Login successful, retrieve or generate the token for this user
                    token, created = Token.objects.get_or_create(
                        user=authenticated_user
                    )
                    return Response({"token": token.key})
                else:
                    # Invalid password
                    return Response(
                        {"error": "Invalid email or password."},
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
            else:
                # User account is not activated
                return Response(
                    {"error": "Please confirm your E-Mail."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        else:
            # Invalid email
            return Response(
                {"error": "Invalid email or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful."})
