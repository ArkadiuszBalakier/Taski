from django.core.validators import RegexValidator

alphanumeric_validator = RegexValidator(
    regex=r"^[a-zA-Z0-9_-]+$",
    message="Only alphanumeric characters and spaces are allowed.",
)
