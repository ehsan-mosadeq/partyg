from django.db import models
from django.contrib.auth.models import User
import random


class Question(models.Model):
    template = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return str(self.template)


class Client(User):
    mob_num = models.CharField(max_length=13, unique=True, default='')

    def has_active_game(self):
        return not self.active_game() is None

    def active_game(self):
        return next((x for x in self.games.all() if x.active), None)

    def __str__(self):
        return self.first_name


class Game(models.Model):
    owner = models.ForeignKey(
        Client, related_name='games', on_delete=models.CASCADE)
    token = models.IntegerField(unique=False, default=0)
    num_of_rounds = models.IntegerField(unique=False, default=0)
    current_round = models.IntegerField(unique=False, default=0)

    @property
    def active(self):
        return self.num_of_rounds > self.current_round

    def questions(self):
        gamers_quests = [gamer.questions.all() for gamer in self.gamers.all()]
        return [item for sublist in gamers_quests for item in sublist]  # sample of double for

    def __get_rand_ix__(self, n):
        return random.randrange(0, n)

    def __get_new_question__(self):
        gamers_list = self.gamers.all()
        questions_list = Question.objects.all()
        gamer = gamers_list[self.__get_rand_ix__(len(gamers_list))]
        question = questions_list[self.__get_rand_ix__(len(questions_list))]
        new_gamer_question, created = \
            GamerQuestion.objects.get_or_create(subject=gamer, question=question)
        if created:
            return new_gamer_question

        return self.__get_new_question__()

    def get_current_question(self):
        cq = next((q for q in self.questions() if not q.finished), None)
        if cq is None:
            return self.__get_new_question__()
        return cq

    def __str__(self):
        return "owner: {}, is active: {} ".format(self.owner, self.active)


class Gamer(models.Model):
    game = models.ForeignKey(Game, related_name='gamers', on_delete=models.CASCADE)
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
        through_fields=['voter', 'selection'], blank=True)

    def __str__(self):
        return str(self.name)

    def get_invitor(self): return self.game.owner

    def token(self): return self.game.token

    @property
    def points(self):
        sumOfPts = sum([len(answer.selectors.all()) for answer in self.my_answers.all()])
        return sumOfPts

    class Meta:
        unique_together = ('game', 'name')


class GamerQuestion(models.Model):
    subject = models.ForeignKey(Gamer, related_name="questions", on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name="instances", on_delete=models.CASCADE)
    finished = models.BooleanField(default=False)

    @property
    def text(self):
        return self.question.template.format(str(self.subject))

    @property
    def answered_by_all(self):
        all_gamers = self.subject.game.gamers.all()
        all_publishers = [ans.publisher for ans in self.answers_to_me.all()]
        return set(all_gamers) == set(all_publishers)

    def __str__(self):
        return "Question: {}, Finished: {}".format(self.text, self.finished)

    class Meta:
        unique_together = ('subject', 'question')


class Answer(models.Model):
    publisher = models.ForeignKey(Gamer, related_name='my_answers', on_delete=models.CASCADE)
    gamer_question = models.ForeignKey(GamerQuestion,
                                       related_name="answers_to_me", on_delete=models.CASCADE, default=None)

    text = models.CharField(max_length=500, unique=False, default='')
    selectors = models.ManyToManyField(Gamer,
                                       through='Vote',
                                       through_fields=['selection', 'voter'], blank=True)

    @property
    def game_token(self):
        return self.publisher.game.token

    def __str__(self):
        return str(self.text)

    class Meta:
        unique_together = ('publisher', 'gamer_question')


class Vote(models.Model):
    voter = models.ForeignKey(Gamer, related_name="my_votes", on_delete=models.CASCADE)
    question = models.ForeignKey(GamerQuestion, related_name="votes", on_delete=models.CASCADE)
    selection = models.ForeignKey(Answer, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('voter', 'question')


class Alert(models.Model):
    publisher = models.ForeignKey(Gamer, related_name="published_alerts", on_delete=models.CASCADE)
    receiver = models.ForeignKey(Gamer, related_name="received_alerts", on_delete=models.CASCADE)
    gamer_question = models.ForeignKey(GamerQuestion,
                                       related_name="alerts", on_delete=models.CASCADE, default=None)

    def __str__(self):
        return "from {} to {} for {}".format(
            str(self.publisher.name), str(self.receiver.name), str(self.gamer_question))

    class Meta:
        unique_together = ('publisher', 'receiver', 'gamer_question')

# points for a Gamer = for answer in Gamer.Answers: points += len(answer.selectors))
# "gtenv/scripts/activate.bat"
