from django.shortcuts import render, get_object_or_404, redirect
from .forms import BoardForm
from .models import Board
from django.utils import timezone

# Create your views here.
def post(request):
    if request.method == "POST":
        form = BoardForm(request.POST)  #BoardForm으로 부터 받은 데이터를 처리하기 위한 인스턴스 생성
        if form.is_valid(): #폼 검증 메소드
            board = form.save(commit = False)   #board 오브젝트를 form으로부터 가져오지만, 실제로 DB반영은 하지 않는다.
            board.update_date=timezone.now()
            board.save()
            return redirect('show') # url의 name을 경로대신 입력한다.
    else:
        form = BoardForm()  # forms.py의 BoardForm 클래스의 인스턴스
        return render(request, 'post.html',{'form' : form})

def show(request):
    # 모든 글들을 대상으로
    boards = Board.objects.order_by('-id')
    return render(request,'show.html',{'boards':boards})

def detail(request,board_id):   # board의 id만 화면에 출력
    board_detail = get_object_or_404(Board, pk=board_id) # 객체를 가져오거나 404페이지만 가져온다는 의미
    return render(request, 'detail.html', {'board':board_detail})

def edit(request, pk):  # url에서 pk를 받아서 처리
# 수정하고자 하는 글의 Post모델 인스턴스를 가져온다.
# 원하는 글은 pk를 이용해 찾는다.
    print("post")
    board = get_object_or_404(Board, pk=pk)
    if request.method == "POST":
        print("post")
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():     # 폼 검증 메소드
            print("if")
            board = form.save(commit = False)
            board.update_date=timezone.now()
            board.save()

            return redirect('show')
    else:
        form = BoardForm(instance=board)
        return render(request, 'edit.html', {'form':form})

def delete(request, pk):
    board = Board.objects.get(id=pk)
    board.delete()
    return redirect('show')