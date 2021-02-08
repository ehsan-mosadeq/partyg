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
    game = models.ForeignKey( Game, related_name='gamers', on_delete=models.CASCADE)
    name = models.CharField(max_length=13, unique=False, default='')

    quests_from_me = models.ManyToManyField(
                Question,
                through='GamerQuestion', 
                through_fields=['subject', 'question'], blank=True)

    connections = models.ManyToManyField(
                'Gamer',
                through='Alert', 
                through_fields=['publisher', 'receiver'], blank=True)

    answered_quests = models.ManyToManyField(
                'GamerQuestion',
                through='Answer', 
                through_fields=['publisher', 'gamer_question'], blank=True)

    answers_selected_by_me = models.ManyToManyField(
                'Answer',
                through='Vote', 
                through_fields=['voter', 'selection'],blank=True)

    def __str__(self):
        return str(self.name)

    def get_invitor(self): return game.owner

    @property
    def points(self):
        sumOfPts = sum([len(answer.selectors.all()) for answer in self.my_answers.all()])
        return sumOfPts

class GamerQuestion(models.Model):
    subject = models.ForeignKey(Gamer, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name = "instances", on_delete=models.CASCADE)
    asked = models.BooleanField(default = False)

    @property
    def text(self):
        return self.question.template.format(str(self.subject))

    def __str__(self):
        return self.text

    class Meta:
        unique_together = ('subject', 'question')

class Answer(models.Model):
    publisher = models.ForeignKey(Gamer, related_name = 'my_answers', on_delete=models.CASCADE)
    gamer_question = models.ForeignKey(GamerQuestion, related_name = "answers_to_me", on_delete=models.CASCADE, default = None)
    text = models.CharField(max_length=500, unique=False, default = '')
    selectors = models.ManyToManyField(Gamer,
                through='Vote', 
                through_fields=['selection', 'voter'], blank=True)

    def __str__(self):
        return str(self.text)
    
    class Meta:
        unique_together = ('publisher', 'gamer_question')

class Vote(models.Model):
    voter = models.ForeignKey(Gamer, related_name = "my_votes", on_delete=models.CASCADE)
    question = models.ForeignKey(GamerQuestion, related_name = "votes", on_delete=models.CASCADE)
    selection = models.ForeignKey(Answer, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('voter', 'question')

class Alert(models.Model):
    publisher = models.ForeignKey(Gamer, related_name = "published_alerts", on_delete=models.CASCADE)
    receiver = models.ForeignKey(Gamer, related_name = "received_alerts", on_delete=models.CASCADE)
    gamer_question = models.ForeignKey(GamerQuestion,
         related_name = "alerts", on_delete=models.CASCADE, default = None)

    def __str__(self):
        return "from {} to {} for {}".format(
            str(self.publisher.name), str(self.receiver.name), str(self.gamer_question))
    
    class Meta:
        unique_together = ('publisher', 'receiver', 'gamer_question')


# points for a Gamer = for answer in Gamer.Answers: points += len(answer.selectors))
#"gtenv/scripts/activate.bat"