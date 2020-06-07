from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Encrypted_data

from django.core.mail import send_mail
from django.conf import settings

# cryptographic modules
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


def home(request):
    return render(request, 'encryption/home.html')


def encrypt(request):
    if (request.method == 'POST'):
        secret_key = request.POST['secretKey']
        file_data = request.POST['fileForEncrypt']
        with open(file_data, 'rb') as f:
            message = f.read()

        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

        public_key = private_key.public_key()

        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        with open('private_key.pem', 'wb') as f:
            f.write(pem)

        pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        with open('public_key.pem', 'wb') as f:
            f.write(pem)

        with open("public_key.pem", "rb") as key_file:
            public_key = serialization.load_pem_public_key(
                key_file.read(),
                backend=default_backend()
            )

        encrypted = public_key.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        f = open('test.encrypted', 'wb')
        f.write(encrypted)
        f.close()
        send_mail('Encryption of file', 'Hey you just encrypted your file with the awesome application',
                  'mathachew@hushmail.com', ['subashwork10@gmail.com'])
        return redirect('/')
    else:
        return render(request, 'encryption/encrypt.html')


def decrypt(request):
    if (request.method == 'POST'):

        file_data = request.POST['fileForDecrypt']

        with open("private_key.pem", "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )

        with open(file_data, 'rb') as f:
            encrypted = f.read()

        original_message = private_key.decrypt(
            encrypted,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            ))

        with open('original_message.txt', 'wb') as f:
            f.write(original_message)
        send_mail('Decryption of file', 'Hey you just decrypt your file with the awesome application',
                  'mathachew@hushmail.com', ['subashwork10@gmail.com'])
        print(original_message)

        return redirect('/')
    else:
        return render(request, 'encryption/decrypt.html')


def profile(request):
    email = request.session['email']
    one = User.objects.get(email=email)
    context = {"data": one}
    return render(request, 'encryption/profile.html', context)


def login(request):
    if (request.method == 'POST'):
        email = request.POST['email']
        password = request.POST['password']
        one = User.objects.get(email=email)
        if(one.password == password):
            #     if(one.password == request.password):
            messages.success(
                request, 'Login Successful')
            context = {'one': one}
            # request.session['email'] = one.email
            request.session['email'] = email
            return redirect('/', context)
        # else:
        #     messages.warning(
        #         request, 'Invalid Credentials')
        #     return redirect('encryption/login.html')
        else:
            messages.error(
                request, 'Invalid Credentials')
            return redirect('login.html')
    else:
        return render(request, 'encryption/login.html')


def register(request):
    if (request.method == 'POST'):
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        photo = request.POST['photo']
        action = User(name=name, email=email, password=password, photo=photo)
        a = action.save()
        print(a)
        messages.success(
            request, 'Success')
        return redirect('/login.html')
    else:
        return render(request, 'encryption/register.html')


def logout(request):
    email = request.session['email']
    del request.session['email']
    return redirect('/login.html')
