from django.db import models

# Create your models here.
from apps.api_data.models import UserToken


class Category(models.Model):
    """
    A model representing a category.

    Fields:
        ACTIVE (str): Constant for active status.
        INACTIVE (str): Constant for inactive status.
        STATUS_CHOICES (tuple): Tuple of tuples containing the status choices for the model.
        id (int): The primary key of the model.
        category_name (str): The name of the category.
        created_at (datetime): The date and time the category was created.
        updated_at (datetime): The date and time the category was last updated.
        deleted_at (datetime): The date and time the category was deleted.
        created_by (str): The username of the user who created the category.
        is_global (bool)
        status (int): The status, either active or inactive, default is inactive.

    """
    ACTIVE = 0
    INACTIVE = 1

    STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    )

    id = models.AutoField(primary_key=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=ACTIVE)
    category_name = models.CharField(max_length=30)
    user_token = models.ForeignKey(UserToken, on_delete=models.DO_NOTHING, related_name='user_token_category',
                                   null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    # created_by = models.TextField(null=True, blank=True)
    # updated_by = models.TextField(null=True, blank=True)
    is_global = models.BooleanField(null=True, blank=True, default=False)

    class Meta:
        db_table = "category"
        managed = True
