from django import forms
from .models import User
from django.contrib.auth.hashers import check_password

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label="사용자 이름")
    password = forms.CharField(widget=forms.PasswordInput, label="비밀번호") # 비밀번호를 표시할 위젯을 지정

    def clean(self):
        cleaned_data = super().clean() # super을 통해 기존의 form안에 들어있는 clean함수를 호출 값이 들어있지 않다면 이부분에서 실패처리되어 나가짐
        username = cleaned_data.get('username') # 값이 존재한다면 값들을 가져옴
        password = cleaned_data.get('password')

        if username and password: # 각 값이 들어있는 경우
            user = User.objects.get(username=username)
            if not check_password(password, user.password): # 입력된 비밀번호와 데이터베이스에서 가져온 비밀번호 비교
                self.add_error('password', '비밀번호를 틀렸습니다.') # 특정 필드에 에러를 넣는 함수
            else: # 비밀번호가 일치하는 경우
                self.user_id = user.id # self를 통해 클래스 변수 안에 저장되므로 밖에서 접근가능
