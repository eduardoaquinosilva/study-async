from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Flashcard(models.Model):
    LEVEL_CHOICES = (('D', 'Difícil'), ('M', 'Médio'), ('F', 'Fácil'))
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    question = models.CharField(max_length=100)
    answer = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    level = models.CharField(max_length=1, choices=LEVEL_CHOICES)
    
    def __str__(self):
        return self.question
    
    @property
    def level_style(self):
        if self.level == "F":
            return "flashcard-facil"
        elif self.level == "M":
            return "flashcard-medio"
        else:
            return "flashcard-dificil"

class FlashcardChallenge(models.Model):
    flashcard = models.ForeignKey(Flashcard, on_delete=models.DO_NOTHING)
    done = models.BooleanField(default=False)
    got_right = models.BooleanField(default=False)

    def __str__(self):
        return self.flashcard.question

class Challenge(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=100)
    category = models.ManyToManyField(Category)
    quant_questions = models.IntegerField()
    level = models.CharField(max_length=1, choices=Flashcard.LEVEL_CHOICES)
    flashcards = models.ManyToManyField(FlashcardChallenge)
 
    def __str__(self):
        return self.title

    @property    
    def status(self):
        if self.flashcards.filter(done=True).count() == self.flashcards.all().count():
            return ["Finalizado", "finished-challenge-background"]
        elif self.flashcards.filter(done=False).count() == 0:
            return ["A começar", "not-started-challenge-background"]
        else:
            return ["Em aberto", "opened-challenge-background"]

    @property
    def challenge_level_style(self):
        if self.level == "F":
            return "easy-challenge-background"
        elif self.level == "M":
            return "medium-challenge-background"
        else:
            return "hard-challenge-background"
