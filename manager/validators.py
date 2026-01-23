from django.core.validators import RegexValidator

alphanumeric_validator = RegexValidator(
    regex=r"^[a-zA-Z0-9 _-]+$",
    message="Only letters, numbers, spaces, hyphens, and underscores are allowed.",
)
