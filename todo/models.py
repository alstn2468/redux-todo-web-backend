from django.db import models


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
        text : CharField
        is_completed : BooleanField
    """

    text = models.CharField(max_length=100)
    is_completed = models.BooleanField(default=False)
