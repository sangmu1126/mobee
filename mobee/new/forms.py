from django.forms import ModelForm
from new.models import Movie, Review
from django import forms
from django.utils.translation import gettext_lazy as _

REVIEW_POINT_CHOICES = (
    ('1', 1),
    ('2', 2),
    ('3', 3),
    ('4', 4),
    ('5', 5),
)  # 평점의 선택지를 정의합니다.


class MovieForm(ModelForm):
    class Meta:
        model = Movie
        fields = ['name', 'genre', 'image', 'password']
        labels = {
            'name': _('이름'),
            'genre': _('장르'),
            'image': _('이미지 url'),
            'password': _('게시물 비밀번호'),
        }
        help_texts = {
            'name': _('이름을 입력해주세요.'),
            'genre': _('장르를 입력해주세요.'),
            'image': _('이미지의 url을 입력해주세요.'),
            'password': _('비밀번호를 입력해주세요.'),
        }
        widgets = {
            'password': forms.PasswordInput()
        }
        error_messages = {
            'name': {
                'max_length': _("이름이 너무 깁니다. 30자 이하로 해주세요."),
            },
            'image': {
                'max_length': _("이미지 주소의 길이 너무 깁니다. 400자 이하로 해주세요."),
            },
            'password': {
                'max_length': _("비밀번호가 너무 깁니다. 20자 이하로 해주세요."),
            },
        }


class UpdateMovieForm(MovieForm):
    class Meta:
        model = Movie
        exclude = ['password']


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['point', 'comment', 'movie']
        labels = {
            'point': _('평점'),
            'comment': _('코멘트'),
        }
        widgets = {
            'movie': forms.HiddenInput(),  # 리뷰를 달 식당 정보는 사용자에게 보여지지 않도록 합니다.
            'point': forms.Select(choices=REVIEW_POINT_CHOICES)  # 선택지를 인자로 전달합니다.
        }
        help_texts = {
            'point': _('평점을 입력해주세요.'),
            'comment': _('코멘트를 입력해주세요.'),
        }
