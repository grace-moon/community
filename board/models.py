from django.db import models

class Board(models.Model):
    title = models.CharField(max_length=200, verbose_name='제목')
    contents = models.TextField(verbose_name='내용')
    writer = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='작성자')
    # 참조키로 user앱의 User모델의 기본키를 참조한다
    # models.CASCADE : user가 탈퇴한 경우 삭제된 사용자의 글들을 모두 삭제한다
    registered_dttm = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')

    def __str__(self): # 클래스가 문자열로 변환될 때 사용되는 내장함수
        return self.title

    class Meta:
        db_table = 'Community_board'
        verbose_name = '커뮤니티 게시글'
        verbose_name_plural = '커뮤니티 게시글' # 복수형 표현도 설정