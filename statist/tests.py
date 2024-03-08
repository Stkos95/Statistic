from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Game, Type


class GameTests(TestCase):
    def test_create_game(self):
        typee = Type.objects.create(name='tt', halfs=3)


