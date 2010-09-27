import datetime

from django.conf import settings
from activities.models import Activity, Commitment

# Directory in which to save image files for ActivityMember verification.
ACTIVITY_FILE_DIR = getattr(settings, 'ACTIVITY_FILE_DIR', 'activities')

# Maximum number of commitments user can have at one time.
MAX_COMMITMENTS = 5

def get_incomplete_tasks(user):
  """Gets user's incomplete activities and commitments. Returns a dictionary."""
  
  user_commitments = get_current_commitments(user)
  user_activities = get_current_activities(user)
    
  return {
    "commitments": user_commitments,
    "activities": user_activities,
  }
  
def can_add_commitments(user):
  """Determines if the user can add additional commitments."""
  return get_current_commitments(user).count() < MAX_COMMITMENTS
  
def get_current_commitments(user):
  """Get the user's incomplete commitments."""
  return user.commitment_set.filter(
    commitmentmember__award_date=None,
  ).order_by("commitmentmember__completion_date")
  
def get_available_commitments(user):
  """Get any commitments that the user is not currently active in."""
  return Commitment.objects.exclude(
    commitmentmember__user=user,
    commitmentmember__completion_date__gt=datetime.datetime.today(),
  ).order_by("title")

def get_completed_commitments(user):
  """Gets the user's completed commitments"""
  return user.commitment_set.filter(
    commitmentmember__award_date__isnull=False,
  ).order_by("title")
  
def get_current_activities(user):
  """Get the user's incomplete activities."""
  
  return user.activity_set.filter(
    activitymember__award_date=None,
  ).order_by("activitymember__submission_date")
  
def get_available_activities(user):
  """Retrieves only the activities that a user can participate in (excluding events)."""
  
  activities = Activity.objects.exclude(
    activitymember__user=user,
  ).filter(
    is_event=False,
    pub_date__lte=datetime.date.today(),
    expire_date__gte=datetime.date.today(),
  ).order_by("priority", "title")
  
  return [item for item in activities if item.is_active] # Filters out inactive activities.
  
def get_available_events(user):
  """Retrieves only the events that a user can participate in."""

  events = Activity.objects.exclude(
    activitymember__user=user,
  ).filter(is_event=True).order_by("title")

  return (item for item in events if item.is_active) # Filters out inactive activities.
  
def get_completed_activities(user):
  """Gets the user's completed activities"""
  return user.activity_set.filter(
    activitymember__award_date__isnull=False,
  ).order_by("title")
  