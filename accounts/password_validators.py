import re
from difflib import SequenceMatcher

from django.core.exceptions import FieldDoesNotExist, ValidationError


class ContainsDigitValidator:
    """
    Validate that the password has at least one digit
    """
    def __init__(self):
        self.help_text = "Password must contain at least one digit"

    def validate(self, password, user=None):
        if not any([c.isdigit() for c in password]):
            raise ValidationError(
                self.help_text,
                code='password_no_digits',
            )

    def get_help_text(self):
        return self.help_text


class ContainsBothCasesValidator:
    """
    Validate that the password has letters of both upper- and lower-case
    """
    def __init__(self):
        self.help_text = "Password must contain upper- and lower-case letters"

    def validate(self, password, user=None):
        if not any([c.isupper() for c in password]) or not any([c.islower() for c in password]):
            raise ValidationError(
                self.help_text,
                code='password_mono_case',
            )

    def get_help_text(self):
        return self.help_text


class ContainsSpecialCharactersValidator:
    """
    Validate that the password has a special character
    """
    def __init__(self):
        self.special_characters = '!@#$%+^&*()-_/?,.[]}{<>`~\\\'\"'
        self.help_text = "Password must contain at least one of: {}".format(
            self.special_characters)

    def validate(self, password, user=None):
        if not any([(c in self.special_characters) for c in password]):
            raise ValidationError(
                self.help_text,
                code='password_no_special_characters',
            )

    def get_help_text(self):
        return self.help_text


# All validators below this line are rewritten from Django's source

class MinimumLengthValidator:
    """
    Validate that the password is of a minimum length
    """
    def __init__(self, min_length=8):
        self.min_length = min_length
        self.help_text = "Password must be at least {} characters".format(self.min_length)

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                self.help_text,
                code='password_too_short',
            )

    def get_help_text(self):
        return self.help_text


class UserAttributeSimilarityValidator:
    """
    Validate that the password is sufficiently different from the user's
    attributes

    If no specific attributes are provided, look at a sensible list of
    defaults. Attributes that don't exist are ignored. Comparison is made to
    not only the full attribute value, but also its components, so that, for
    example, a password is validated against either part of an email address,
    as well as the full address
    """
    DEFAULT_USER_ATTRIBUTES = ('first_name', 'last_name', 'email')

    def __init__(self, user_attributes=DEFAULT_USER_ATTRIBUTES, max_similarity=0.7):
        self.user_attributes = user_attributes
        self.max_similarity = max_similarity

    def validate(self, password, user=None):
        if not user:
            return

        for attribute_name in self.user_attributes:
            value = getattr(user, attribute_name, None)
            if not value or not isinstance(value, str):
                continue
            value_parts = re.split(r'\W+', value) + [value]
            for value_part in value_parts:
                if SequenceMatcher(a=password.lower(), b=value_part.lower()).quick_ratio() >= \
                        self.max_similarity:
                    try:
                        verbose_name = str(user._meta.get_field(attribute_name).verbose_name)
                    except FieldDoesNotExist:
                        verbose_name = attribute_name
                    raise ValidationError(
                        "Password is too similar to the %(verbose_name)s",
                        code='password_too_similar',
                        params={'verbose_name': verbose_name},
                    )

    def get_help_text(self):
        return "Password can't be too similar to your personal information"


class NumericPasswordValidator:
    """
    Validate that the password is not entirely alphanumeric
    """
    def __init__(self):
        self.help_text = "Password can't be entirely alphanumeric"

    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                self.help_text,
                code='password_entirely_numeric',
            )

    def get_help_text(self):
        return self.help_text
