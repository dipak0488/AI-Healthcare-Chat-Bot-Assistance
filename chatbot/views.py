from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from langdetect import detect
from .models import History
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from .bot import get_bot_response
from django.conf import settings
import os
from reportlab.lib.utils import ImageReader
import random
from django.core.mail import send_mail
#otp verification
def forgot_password(request):

    if request.method == 'POST':
        username = request.POST.get('username')

        try:
            user = User.objects.get(username=username)

            otp = str(random.randint(100000, 999999))

            request.session['otp'] = otp
            request.session['username'] = username

            send_mail(
                'Password Reset OTP',
                f'Your OTP is {otp}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

            return redirect('verify_otp')

        except User.DoesNotExist:
            messages.error(request, "User not found")

    return render(request, 'forgot_password.html')
#otp with reset password
def verify_register_otp(request):

    if request.method == 'POST':

        entered_otp = request.POST.get('otp')

        if entered_otp == request.session.get('reg_otp'):

            username = request.session.get('reg_username')
            email = request.session.get('reg_email')
            password = request.session.get('reg_password')

            from django.contrib.auth.models import User
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            from django.contrib import messages
            messages.success(request, "Registration successful! Please login.")
            return redirect('login')

        else:
            from django.contrib import messages
            messages.error(request, "Invalid OTP")

    return render(request, 'verify_register_otp.html')
#forget button
def forgot_password(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()

            messages.success(request, "Password reset successful! Please login.")
            return redirect('login')

        except User.DoesNotExist:
            messages.error(request, "Username not found")

    return render(request, 'forgot_password.html')    
# ---------------- HOME ----------------

def home(request):
    return render(request, 'chat.html')


# ---------------- REGISTER ----------------

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.save()
        messages.success(request, "Registration successful! Please login.")
        return redirect('login')

    return render(request, 'register.html')


# ---------------- LOGIN ----------------

def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:

            auth_login(request, user)

            if user.is_superuser:
                return redirect('/admin/')
            else:
                return redirect('/chat/')

        else:
            messages.error(request, "Invalid Username or Password")

    return render(request, 'login.html')


# ---------------- LOGOUT ----------------

def user_logout(request):
    logout(request)
    return redirect('login')


# ---------------- CHAT PAGE ----------------

def chatbot(request):
    return render(request, 'chat.html')


# ---------------- CHAT RESPONSE ----------------

def get_response(request):

    msg = request.GET.get("msg")

    try:
        user_lang = detect(msg)
    except:
        user_lang = "en"

    reply = get_bot_response(msg, user_lang)

    return JsonResponse({
        "reply": reply,
        "lang": user_lang
    })

# ---------------- PDF MEDICAL REPORT ----------------

def download_report(request):

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="AI_Medical_Report.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # -------- HEADER --------
        # -------- LOGO --------
    logo_path = os.path.join(settings.BASE_DIR, "static", "logo.png")
    if os.path.exists(logo_path):
        p.drawImage(logo_path, 30, 735, width=100, height=100)
    p.setFont("Helvetica-Bold", 18)
    p.drawString(120, 790, "AI Healthcare Hospital")

    p.setFont("Helvetica", 11)
    p.drawString(120, 770, "Smart AI Medical Report System")

    p.line(50, 750, 550, 750)

    # -------- TITLE --------
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width/2, 720, "MEDICAL REPORT")

    # -------- PATIENT DETAILS --------
    p.setFont("Helvetica", 12)

    p.drawString(70, 680, f"Patient Name : {request.user.username}")
    p.drawString(70, 660, "Doctor       : AI Health Assistant")
    p.drawString(70, 640, "Hospital     : AI Healthcare System")

    # separator
    p.line(50, 620, 550, 620)

    # -------- DIAGNOSIS RESULT --------
    p.setFont("Helvetica-Bold", 13)
    p.drawString(70, 590, "Diagnosis Result")

    p.setFont("Helvetica", 12)
    p.drawString(70, 560, "AI Prediction : General Checkup")

    # -------- DOCTOR ADVICE --------
    p.setFont("Helvetica-Bold", 13)
    p.drawString(70, 520, "Doctor Advice")

    p.setFont("Helvetica", 12)

    advice_list = [
        "Take proper rest",
        "Drink plenty of water",
        "Take prescribed medicines",
        "Consult doctor if symptoms continue"
    ]

    y = 495
    for advice in advice_list:
        p.drawString(90, y, f"- {advice}")
        y -= 20

    # -------- DISCLAIMER --------
    p.setFont("Helvetica-Oblique", 10)

    p.drawString(70, 420, "Note: This report is generated by AI Healthcare System.")
    p.drawString(70, 405, "Please consult a certified doctor for medical advice.")

    # signature
        #stamp
    stamp_path = os.path.join(settings.BASE_DIR, "static", "stamp.png")
    if os.path.exists(stamp_path):
        p.drawImage(stamp_path, 380, 250, width=120, height=90)
    p.setFont("Helvetica", 11)
    p.drawString(420, 240, "AI Doctor")

    p.showPage()
    p.save()

    return response