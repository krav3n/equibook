# coding=utf-8
from haystack import indexes

from horsebook.trainer.models import Trainer


class TrainerIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True)
    name = indexes.EdgeNgramField(model_attr='name')
    email = indexes.EdgeNgramField(model_attr='email')
    diciplines = indexes.MultiValueField()
    skill_level = indexes.IntegerField(model_attr='skill_level')
    homepage = indexes.EdgeNgramField(model_attr='homepage')
    county = indexes.CharField(model_attr='county')

    def prepare_diciplines(self, obj):
        """
        Fetch all diciplines for each trainer
        """
        return [d.code for d in Trainer.objects.filter(id=obj.id).first().diciplines.all()]

    def get_model(self):
        return Trainer
