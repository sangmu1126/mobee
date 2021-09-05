from django.db import models


class Movie(models.Model):
    name = models.CharField(max_length=30)  # 이름
    genre = models.CharField(max_length=30)  # 장르

    image = models.CharField(max_length=500, default=None, null=True)
    password = models.CharField(max_length=20, default=None, null=True)

    created_at = models.DateTimeField(auto_now_add=True)  # 글 작성 시 (이 모델의 데이터(레코드) 저장 시) 생성 시각
    updated_at = models.DateTimeField(auto_now=True)  # 저장된 레코드 수정 시 수정 시각


class Review(models.Model):
    point = models.IntegerField()
    comment = models.CharField(max_length=500)

    # 식당 모델과의 릴레이션 정의,
    # on_delete CASCADE로 지정하면 식당이 삭제되면 같이 삭제된다.
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)  # 글 작성 시 (이 모델의 데이터(레코드) 저장 시) 생성 시각
    updated_at = models.DateTimeField(auto_now=True)
