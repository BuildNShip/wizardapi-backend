from django.db import models
from apps.category.models import Category
from apps.app_settings.models import ResponseCodes


class UserToken(models.Model):

    """
    A model for storing app_token from common auth server.

    Fields:
        ACTIVE (str): Constant for active status.
        INACTIVE (str): Constant for inactive status.
        STATUS_CHOICES (tuple): Tuple of tuples containing the status choices for the model.
        id (int): The primary key of the model.
        user_token (str): The user token.
        api_token (str): The API token.
        status (int): The status, either active or inactive.
        created_at (datetime): The date and time of creation.
        updated_at (datetime): The date and time of last update.
        deleted_at (datetime): The date and time of deletion.

    """

    ACTIVE = 1
    INACTIVE = 0

    STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    )

    id = models.AutoField(primary_key=True)
    user_token = models.TextField()
    api_token = models.TextField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "user_token"
        managed = True


class APIData(models.Model):

    """
    A model representing API data.

    Fields:
        ACTIVE (str): Constant for active status.
        INACTIVE (str): Constant for inactive status.
        STATUS_CHOICES (tuple): Tuple of tuples containing the status choices for the model.
        METHOD_CHOICES (tuple): Tuple of tuples containing the method choices for the model.
        id (int): The primary key of the model.
        user_token (str): The user token.
        category (Category): The category of the API.
        Responses (ManyToManyField): The responses associated with the API data.
        url (str): The URL of the API.
        method (int): The method used.
        status (int): The status, either active or inactive.
        created_at (datetime): The date and time of creation.
        updated_at (datetime): The date and time of last update.
        deleted_at (datetime): The date and time of deletion.

    """

    ACTIVE = 1
    INACTIVE = 0

    STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    )

    GET = 1
    POST = 2
    PUT = 3
    DELETE = 4

    METHOD_CHOICES = (
        (GET, 'Get'),
        (POST, 'Post'),
        (PUT, 'Put'),
        (DELETE, 'Delete'),
    )

    id = models.AutoField(primary_key=True)
    user_token = models.ForeignKey(UserToken, on_delete=models.DO_NOTHING, related_name='user_token_api_data', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, null=True)
    responses = models.ManyToManyField('ApiResponses', through='ApiDataResponses')
    url = models.CharField(max_length=1024)
    method = models.IntegerField(choices=METHOD_CHOICES, default=POST)
    status = models.IntegerField(choices=STATUS_CHOICES, default=ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "api_data"
        managed = True


class ApiResponses(models.Model):

    """
    A model representing the apiresponses.

    Fields:
    - id (AutoField): the primary key of the response.
    - response_code (ForeignKey): the response code associated with each response.
    - body (JSONField): the JSON body of the response.
    - status (int): the status of the response (active or inactive).
    - created_at (DateTimeField): the date and time the response was created.
    - updated_at (DateTimeField): the date and time the response was last updated.
    - deleted_at (DateTimeField): the date and time the response was soft-deleted.

    """

    ACTIVE = 1
    INACTIVE = 0

    STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    )

    id = models.AutoField(primary_key=True)
    response_code = models.ForeignKey(ResponseCodes, on_delete=models.DO_NOTHING, null=True)
    body = models.JSONField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)


class ApiDataResponses(models.Model):
    """
    Model representing the many-to-many relationship between `APIData` and `ApiResponses` models.

    Fields:
    - api_data: A foreign key to the `APIData` model.
    - api_response: A foreign key to the `ApiResponses` model.
    - default_response: A boolean indicating whether this is the default response for the associated `ResponseCodes` object.
    """
    api_data = models.ForeignKey(APIData, on_delete=models.CASCADE, null=True)
    api_response = models.ForeignKey(ApiResponses, on_delete=models.CASCADE, null=True)
    default_response = models.BooleanField(null=True, blank=True, default=False)
