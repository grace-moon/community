from django.shortcuts import render, redirect
from .models import Board
from user.models import User
from .forms import BoardForm
# Create your views here.

def board_write(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            #user_id = request.session.get('user') # user_id를 가져옴
            user = User.objects.get() # 현재 로그인한 사용자 id를 user에 저장

            board = Board() # 모델 클래스 변수 생성
            board.title = form.cleaned_data['title'] # form의 제목을 가져옴
            board.contents = form.cleaned_data['contents']
            board.writer = user # 현재 로그인한 사용자의 id
            board.save()

            return redirect('/board/list/') # 작성 후 글목록으로 이동
    else:
        form = BoardForm()
    return render(request, 'board/board_write.html', {'form' : form})

def board_list(request):
    boards = Board.objects.all().order_by('-id') # Board모델의 모든 필드를 가져와 id의 역순으로 가져옴(최신글을 맨위로 올림)

    return render(request, 'board/board_list.html', {'boards' : boards})

def board_detail(request, pk): # 몇번째 글인지 확인하기 위해 주소로부터 pk를 받음
    board = Board.objects.get(pk=pk) # pk에 해당하는 글을 가져옴(입력받은 id값에(몇번째글인지) 맞는 글을 가져옴)
    return render(request, 'board/board_detail.html', {'board' : board}) #템플릿에 전달