from django import forms
from django.forms.util import ErrorList

from resources.models import Topic, Resource
  
class TopicChoiceField(forms.ModelMultipleChoiceField):
  def label_from_instance(self, obj):
    return "%s (%d)" % (obj.topic, obj.resource_set.count())

class TopicSelectForm(forms.Form):
  topics = TopicChoiceField(
      label="",
      queryset=Topic.objects,
      widget=forms.CheckboxSelectMultiple,
      initial=[topic.pk for topic in Topic.objects.all()],
  )