from django.db import models
from django.contrib.auth.models import User


class AbstractTimeStamp(models.Model):
    """Abstract TimeStamp Model
    Inherit:
        Model
    Fields:
        created_at : DateTimeField (UnEditable)
        updated_at : DateTimeField (Editable)
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Todo(AbstractTimeStamp):
    """Todo Model
    Inherit:
        AbstractTimeStamp
    Fields:
        user         : ForeignKey (User)
        text         : CharField
        is_completed : BooleanField
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.text
