from django.db import models
from userauths.models import User
from shortuuid.django_fields import ShortUUIDField
import uuid
from django.db.models.signals import post_save


ACCOUNT_STATUS = (
    ("active", "Active"),
    ("pending", "Pending"),
    ("in-active", "In-active"),
)

MARITAL_STATUS = (("married", "Married"), ("single", "Single"), ("other", "Other"))

GENDER = (("male", "Male"), ("female", "Female"), ("other", "Other"))

NATIONALITY = (
    ("GH", "Ghanaian"),
    ("NG", "Nigerian"),
    ("US", "United States"),
    ("EU", "European"),
    ("IND", "Indian"),
    ("other", "Other"),
)

IDENTITY_TYPE = (
    ("national_id_card", "National ID Card"),
    ("drivers_licence", "Driver's Licence"),
    ("international_passport", "International Passport"),
)


def user_directory_path(instance, filename):
    file_extension = filename.split(".")[-1]
    file_name = "%s_%s" % (instance.id, file_extension)
    return "user_{0}/{1}".format(instance.user.id, filename)

# Bank Account Model : 
class Account(models.Model):
    id = models.UUIDField(
        primary_key=True, unique=True, default=uuid.uuid4, editable=False
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    account_number = ShortUUIDField(
        unique=True, length=10, max_length=25, prefix="217", alphabet="1234567890"
    )

    account_id = ShortUUIDField(
        unique=True, length=10, max_length=25, prefix="217", alphabet="1234567890"
    )

    pin_number = ShortUUIDField(
        unique=True, length=4, max_length=7, alphabet="1234567890"
    )

    ref_code = ShortUUIDField(
        unique=True,
        length=10,
        max_length=20,
        prefix="217",
        alphabet="abcdefgh1234567890",
    )
    
    # Account Status can either be inactive, pending or inactive : 
    account_status = models.CharField(
        max_length=100, choices=ACCOUNT_STATUS, default="in-active"
    )

    # Date account was created : 
    date = models.DateTimeField(auto_now_add=True)

    # KYC Forms associated with the Account is submitted or not ; It's false for newly created account
    kyc_submitted = models.BooleanField(default=False)
    
    # KYC submission confirmation 
    kyc_confirmed = models.BooleanField(default=False)

    # Who recommended the User to create an account with us? : This is an optional field 
    recommended_by = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="recommended_by",
    )

    review = models.CharField(max_length=100, null=True, blank=True, default="Review")

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.user}"



# The KYC is just a financial document that the user fills for account security and identification purposes
class KYC(models.Model):
    id = models.UUIDField(
        primary_key=True, unique=True, default=uuid.uuid4, editable=False
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account = models.OneToOneField(
        Account, on_delete=models.CASCADE, null=True, blank=True
    )
    full_name = models.CharField(max_length=1000)
    image = models.ImageField(upload_to="kyc", default="default.jpg")
    marital_status = models.CharField(choices=MARITAL_STATUS, max_length=40)
    gender = models.CharField(choices=GENDER, max_length=40)
    identity_type = models.CharField(choices=IDENTITY_TYPE, max_length=140)
    identity_image = models.ImageField(upload_to="kyc", null=True, blank=True)
    date_of_birth = models.DateTimeField(auto_now_add=False)
    signature = models.ImageField(upload_to="kyc")

    # User's Address
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    # User's Contact Details
    mobile = models.CharField(max_length=1000)
    fax = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name = "KYC"
        verbose_name_plural = "KYCs"
        ordering = ["-date"]


"""
Create signals to automatically create and save an account for a newly registered user
"""


def create_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)


def save_account(sender, instance, **kwargs):
    instance.account.save()


post_save.connect(create_account, sender=User)
post_save.connect(save_account, sender=User)
