from django.shortcuts import render, redirect # 리다이렉트 함수 import
from .models import User
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from .forms import LoginForm # 위에서 생성한 forms를 불러옴


def home(request):
    user_id = request.session.get('user') # 세션으로부터 사용자 ID를 가져옴

    if user_id:
        user = User.objects.get() # 모델에서 id를 기본키로해서 가져옴
        return HttpResponse(user.username) # 모델의 username을 출력 (로그인이 된경우)

    return HttpResponse("Home!") # 로그인이 되지 않은 경우 Home!출력


def login(request):
    if request.method == 'POST': # 메소드가 POST인 경우
        form = LoginForm(request.POST) # 폼 클래스 변수 생성시 POST데이터를 저장
        if form.is_valid(): # form에 기본적으로 있는 is_valid()함수로 데이터가 정상적인지 검증
            request.session['user'] = form.user_id # 세션에 user의 세션id를 저장
            return redirect('/')

    else:
        form = LoginForm() # 빈 클래스 변수 생성
    return render(request, 'user/login.html', {'form': form})  # 생성한 클래스 변수를 템플릿에 전달


def logout(request):
    if request.session.get('user'):
        del(request.session['user'])

    return redirect('/')

def register(request):
    if request.method == 'GET':
        return render(request, 'user/register.html')
    elif request.method == 'POST':
        username = request.POST.get('username', None) # 템플릿에서 입력한 name필드에 있는 값을 키값으로 받아옴
        password = request.POST.get('password', None) # 받아온 키값에 값이 없는경우 None값으로 기본값으로 지정
        re_password = request.POST.get('re-password', None)
        useremail = request.POST.get('useremail', None)

        res_data = {} # 응답 메세지를 담을 변수(딕셔너리)

        if not (username and useremail and password and re_password and useremail):
            res_data['error'] = '모든 값을 입력해야 합니다.'
        elif password != re_password:
            res_data['error'] = '비밀번호가 다릅니다.'
        else:
            user = User( # 모델에서 생성한 클래스를 가져와 객체를 생성
                username=username,
                useremail=useremail,
                password=make_password(password) # 비밀번호를 암호화하여 저장
            )

            user.save() # 데이터베이스에 저장

        return render(request, 'user/register.html', res_data) # res_data가 html코드로 전달이 됨
