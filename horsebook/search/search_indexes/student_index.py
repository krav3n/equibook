# coding=utf-8
from haystack import indexes

from horsebook.student.models import Student


class StudentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True)
    name = indexes.CharField(model_attr='name')
    email = indexes.CharField(model_attr='email')

    def get_model(self):
        return Student
