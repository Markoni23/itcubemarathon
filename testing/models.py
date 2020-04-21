from django.db import models
from django import forms

class AgeCategory(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "AgeCategory"
        verbose_name_plural = "AgeCategorys"

    def __str__(self):
        return self.name


class Test(models.Model):
    name = models.CharField(max_length=50)
    lesson = models.ForeignKey('marathon.Lesson', verbose_name="tests", on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(AgeCategory, verbose_name="category", on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"

    def __str__(self):
        return self.name


class Question(models.Model):
    text = models.TextField()
    test = models.ForeignKey(Test, verbose_name="test", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return self.text

class Answer(models.Model):
    text = models.TextField()
    right_ans = models.BooleanField()
    question = models.ForeignKey(Question, verbose_name="answers", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def __str__(self):
        return self.text


class TestResult(models.Model):
    test = models.ForeignKey(Test, verbose_name="test", on_delete=models.CASCADE)
    student = models.ForeignKey("marathon.Student", verbose_name="student", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "TestResults"
        verbose_name_plural = "Test Resultss"


class ResultAnswer(models.Model):
    testresult = models.ForeignKey(TestResult, verbose_name="test_result", on_delete=models.CASCADE)
    selected_ans = models.ForeignKey(Answer, verbose_name="answer", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "ResultAnswer"
        verbose_name_plural = "ResultAnswers"




