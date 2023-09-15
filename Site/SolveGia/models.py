from django.db import models
from Users.models import CustomUser


User = CustomUser


class Category(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=250)

    def __str__(self):
        return f'<Category-{self.name}>'

"""
Old task model:

class Task(models.Model):
    type_number = models.IntegerField(blank=False)
    text = models.TextField(blank=False)
    answer = models.TextField(blank=False)
    photos = models.TextField(blank=True)
    files = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    rating = models.IntegerField(blank=True, default=0)
    voices = models.ManyToManyField(User, blank=True)
"""

class Task(models.Model):
    type_number = models.IntegerField()
    text = models.TextField()
    answer = models.TextField(blank=True, null=True)
    photos = models.TextField(blank=True)
    files = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    rating = models.PositiveSmallIntegerField(blank=True, default=0)

    def __str__(self):
        return f'<task-{self.type_number}.{self.pk}>'


class Variant(models.Model):
    tasks = models.ManyToManyField(Task, related_name='totasks')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'<Variant-{self.category.name}>'


class Try(models.Model):
    solve_percent = models.FloatField()

    def __str__(self):
        return f'<Try-{self.solve_percent}>'


class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tries = models.ManyToManyField(Try, related_name='totries')

    def __str__(self):
        return f'<Result-{self.user.username}-tries:{len(self.tries.all())}>'


class Homework(models.Model):
    # variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    results = models.ManyToManyField(Result, related_name='toresults')

    def __str__(self):
        return f'<Homework-{self.variant}-rs:{len(self.results.all())}>'


class CustomGroup(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    users = models.ManyToManyField(User, related_name='tocustomusers')
    homeworks = models.ManyToManyField(Homework, related_name='tohomeworks')

    def __str__(self):
        return f'<CustomGroup-{self.name}-hws:{len(self.homeworks.all())}>'
