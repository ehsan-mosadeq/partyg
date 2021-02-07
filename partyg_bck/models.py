from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    template = models.CharField(max_length=500, unique=True)
    def __str__(self):
        return str(self.template)

class Client(User):
    mob_num = models.CharField(max_length=13, unique=True, default='')

    def __str__(self):
        return self.first_name

class Game(models.Model):
    owner = models.ForeignKey(
        Client, related_name='games', on_delete=models.CASCADE)
    token = models.IntegerField(unique=False, default=0)
    num_of_rounds = models.IntegerField(unique=False, default=0)
    current_round = models.IntegerField(unique=False, default=0)

class Gamer(models.Model):
    game = models.ForeignKey(
        Game, related_name='gamers', on_delete=models.CASCADE)
    name = models.CharField(max_length=13, unique=False, default='')

    def __str__(self):
        return str(self.name)

    def get_invitor(): return game.owner

    @property
    def points(self):
        return sum([len(answer.selectors.all()) for answer in self.answers.all()])

class GameQuestion(models.Model):
    question = models.ForeignKey(Question, related_name = "instances", on_delete=models.CASCADE)
    subject = models.ForeignKey(Gamer, related_name = "questions", on_delete=models.CASCADE)

    @property
    def text(self):
        return self.question.template.format(str(self.subject))

    def __str__(self):
        return self.text

class Answer(models.Model):
    publisher = models.ForeignKey(Gamer, related_name = "answers", on_delete=models.CASCADE)
    game_question = models.ForeignKey(GameQuestion, related_name = "answers", on_delete=models.CASCADE, default = None)
    text = models.CharField(max_length=500, unique=False, default = '')
    selectors = models.ManyToManyField(Gamer)

    def __str__(self):
        return str(self.text)

class Alert(models.Model):
    publisher = models.ForeignKey(Gamer, related_name = "published_alerts", on_delete=models.CASCADE)
    receiver = models.ForeignKey(Gamer, related_name = "received_alerts", on_delete=models.CASCADE)
    game_question = models.ForeignKey(GameQuestion, related_name = "alerts", on_delete=models.CASCADE, default = None)

    def __str__(self):
        return "from {} to {} for {}".format(str(publisher.name), str(receiver.name), str(game_question))



# points for a Gamer = for answer in Gamer.Answers: points += len(answer.selectors))
#"gtenv/scripts/activate.bat"