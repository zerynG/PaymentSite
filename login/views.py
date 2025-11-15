from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Поиск пользователя по email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Пользователь не найден'})

        # Аутентификация
        user = authenticate(request, username=user.username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True, 'redirect_url': '/home/'})
        else:
            return JsonResponse({'success': False, 'message': 'Неверный пароль'})

    return render(request, 'login/login.html')  # Путь к шаблону



def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Проверка паролей
        if password != confirm_password:
            return JsonResponse({'success': False, 'message': 'Пароли не совпадают'})

        # Проверка существования пользователя
        if User.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'message': 'Пользователь с таким email уже существует'})

        # Создание пользователя
        try:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=name
            )
            user.save()

            # Автоматический вход после регистрации
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'success': True, 'redirect_url': '/home/'})

        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Ошибка при создании пользователя: {str(e)}'})

    return render(request, 'login/login.html')  # Используем тот же шаблон


def home_view(request):
    if not request.user.is_authenticated:
        return redirect('login:auth')
    return render(request, 'login/home.html')


def logout_view(request):
    logout(request)
    return redirect('login:auth')