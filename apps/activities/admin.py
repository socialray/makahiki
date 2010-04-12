from activities.models import Activity, ActivityMember, TextPromptQuestion, ConfirmationCode
from django.contrib import admin
from django import forms
from django.forms.models import BaseInlineFormSet
from django.forms.util import ErrorList
  
class ActivityAdminForm(forms.ModelForm):
  num_codes = forms.IntegerField(required=False, 
                                 label="Number of codes", 
                                 help_text="Number of confirmation codes to generate", 
                                 initial=0
                                )
  
  def __init__(self, *args, **kwargs):
    """Override to change number of codes help text if we are editing an activity."""
    
    super(ActivityAdminForm, self).__init__(*args, **kwargs)
    # Instance points to an instance of the model.
    if self.instance and self.instance.created_at:
      self.fields["num_codes"].help_text = "Number of additional codes to generate<br/>" 
      self.fields["num_codes"].help_text += "<a href=\"http://youtube.com\" target=\"_blank\">View codes</a>"
    
  class Meta:
    model = Activity
    
  def clean(self):
    """ Validates the admin form data based on our constraints.
      
      #1 Events must have an event date.
      #2 If the verification type is "image" or "code", then a confirm prompt is required.
      #3 If the verification type is "text", then additional questions are required 
         (Handled in the formset class below).
      #4 Publication date must be before expiration date.
      #5 If the verification type is "code", then the number of codes is required.  """
    
    # Data that has passed validation.
    cleaned_data = self.cleaned_data
    
    #1 Check that an event has an event date.
    is_event = cleaned_data.get("is_event")
    event_date = cleaned_data.get("event_date")
    has_date = cleaned_data.has_key("event_date") #Check if this is in the data dict.
    if is_event and has_date and not event_date:
      self._errors["event_date"] = ErrorList([u"Events require an event date."])
      del cleaned_data["is_event"]
      del cleaned_data["event_date"]
      
    #2 Check the verification type.
    confirm_type = cleaned_data.get("confirm_type")
    prompt = cleaned_data.get("confirm_prompt")
    if confirm_type != "text" and len(prompt) == 0:
      self._errors["confirm_prompt"] = ErrorList([u"This confirmation type requires a confirmation prompt."])
      del cleaned_data["confirm_type"]
      del cleaned_data["confirm_prompt"]
      
    #4 Publication date must be before the expiration date.
    if cleaned_data.has_key("pub_date") and cleaned_data.has_key("expire_date"):
      pub_date = cleaned_data.get("pub_date")
      expire_date = cleaned_data.get("expire_date")
      
      if pub_date >= expire_date:
        self._errors["expire_date"] = ErrorList([u"The expiration date must be after the pub date."])
        del cleaned_data["expire_date"]
        
    #5 Number of codes is required if the verification type is "code"
    has_codes = cleaned_data.has_key("num_codes")
    num_codes = cleaned_data.get("num_codes")
    if confirm_type == "code" and has_codes and not num_codes:
      self._errors["num_codes"] = ErrorList([u"The number of codes is required for this confirmation type."])
      del cleaned_data["num_codes"]
    elif confirm_type == "code" and len(self._errors) == 0 and num_codes > 0:
      # Generate codes here if all data is valid.
      ConfirmationCode.generate_codes_for_activity(self.instance, num_codes)
      
    return cleaned_data
    
class TextQuestionInlineFormSet(BaseInlineFormSet):
  """Custom formset model to override validation."""
  
  def clean(self):
    """Validates the form data and checks if the activity confirmation type is text."""
    
    # Form that represents the activity.
    activity = self.instance
    
    # Count the number of questions.
    count = 0
    for form in self.forms:
      try:
        if form.cleaned_data:
          count += 1
      except AttributeError:
        pass
        
    if activity.confirm_type == "text" and count == 0:
      raise forms.ValidationError("At least one question is required if the activity's confirmation type is text.")
        
    elif activity.confirm_type != "text" and count > 0:
      raise forms.ValidationError("Questions are not required for this confirmation type.")

class TextQuestionInline(admin.TabularInline):
  model = TextPromptQuestion
  fieldset = (
    (None, {
      'fields' : ('question', 'answer'),
      'classes' : ['wide',],
    })
  )
  extra = 3
  formset = TextQuestionInlineFormSet
  
class ActivityAdmin(admin.ModelAdmin):
  fieldsets = (
    ("Basic Information", {
      'fields' : ('title', 'description', 'point_value', 'duration', ('pub_date', 'expire_date')),
    }),
    ("Confirmation Type", {'fields': ('confirm_type', 'num_codes', 'confirm_prompt')}),
    ("Event", {'fields' : ('is_event', 'event_date')}),
  )
  form = ActivityAdminForm
  inlines = [TextQuestionInline]
  list_display = ["title", "created_at", "is_active", "pub_date", "expire_date",]
  
admin.site.register(Activity, ActivityAdmin)

class ActivityMemberAdmin(admin.ModelAdmin):
  radio_fields = {"approval_status" : admin.HORIZONTAL}
  # Requires Django 1.2
  # readonly_fields = ("user", "activity", "question", "response", "user_comment", "image")
  list_display = ("activity", "user", "approval_status")
  list_filter = ["approval_status"]
  
admin.site.register(ActivityMember, ActivityMemberAdmin)
