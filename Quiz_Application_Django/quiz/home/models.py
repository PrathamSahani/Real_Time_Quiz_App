from django.db import models
import uuid
import random




class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        abstract = True

class Types(BaseModel):
    gfg_name = models.CharField(max_length=100)

    def __str__(self):
        return self.gfg_name

    @staticmethod
    def create_default_categories():
        categories = ['Programming', 'Logical', 'Reasoning']
        for category_name in categories:
            if not Types.objects.filter(gfg_name=category_name).exists():
                Types.objects.create(gfg_name=category_name)

class Question(BaseModel):
    gfg = models.ForeignKey(Types, related_name='gfg', on_delete=models.CASCADE)
    question = models.CharField(max_length=100)
    marks = models.IntegerField(default=5)

    def __str__(self):
        return self.question

    def get_answers(self):
        answer_objs = list(Answer.objects.filter(question=self))
        data = []
        random.shuffle(answer_objs)
        for answer_obj in answer_objs:
            data.append({
                'answer': answer_obj.answer,
                'is_correct': answer_obj.is_correct
            })
        return data

class Answer(BaseModel):
    question = models.ForeignKey(Question, related_name='question_answer', on_delete=models.CASCADE)
    answer = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer

# --
from django.contrib.auth.models import User

class QuizAttempt(BaseModel):
    user = models.ForeignKey(User, related_name="quiz_attempts", on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name="attempts", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    incorrect_answers = models.IntegerField(default=0)
    unattempted = models.IntegerField(default=0)
    status = models.CharField(max_length=10, default="Incomplete")  # e.g., Passed/Failed

    def __str__(self):
        return f"{self.user.username} - {self.question.gfg.gfg_name}"
