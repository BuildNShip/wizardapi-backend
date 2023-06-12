from django.db import models


class ResponseCodes(models.Model):
    """
    A model representing response codes.

    Fields:
        ACTIVE (str): Constant for active status.
        INACTIVE (str): Constant for inactive status.
        STATUS_CHOICES (tuple): Tuple of tuples containing the status choices for the model.
        id (int): The primary key of the model.
        code (int): The response code.
        title (str): The title of the response code.
        created_at (datetime): The date and time the response code was created.
        updated_at (datetime): The date and time the response code was last updated.
        deleted_at (datetime): The date and time the response code was deleted.
        status (int): The status of the response code, either active or inactive, default is inactive.

    """

    ACTIVE = 0
    INACTIVE = 1

    STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    )

    id = models.AutoField(primary_key=True)
    code = models.IntegerField()
    title = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=ACTIVE, null=False)
