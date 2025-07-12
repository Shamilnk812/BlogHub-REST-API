import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from .models import User


# Reserved usernames that should not be allowed for new users
RESERVED_USERNAMES = ['admin', 'root', 'superuser', 'null', 'none', 'user']

def validate_username(username):
    """
    Validates the given username.

    - Must be unique (case-insensitive)
    - Must not be in the reserved list
    - Must be 3 to 30 characters long
    - Can contain only letters, numbers, underscores, and dots
    - Cannot contain consecutive special characters like '__', '..', '._', or '_.'
    - Cannot be only numbers
    """
     
    # Check uniqueness (case-insensitive)
    if User.objects.filter(username__iexact=username).exists():
        raise ValidationError("This username is already taken.")
    
    # Check reserved names
    if username.lower() in RESERVED_USERNAMES:
        raise ValidationError("This username is reserved.")

    # Allow only specific characters
    if not re.match(r'^[a-zA-Z0-9_.]+$', username):
        raise ValidationError("Username can only contain letters, numbers, underscores, and dots.")

    # Disallow usernames with only numbers
    if username.isdigit():
        raise ValidationError("Username cannot be only numbers.")
    
    # Enforce length constraints
    if not (3 <= len(username) <= 30):
        raise ValidationError("Username must be between 3 and 30 characters.")

    # Disallow consecutive special characters
    if '__' in username or '..' in username or '._' in username or '_.' in username:
        raise ValidationError("Username cannot contain consecutive special characters.")



class CustomPasswordValidator:
    """
    Validates password strength.

    - Must include at least one uppercase letter
    - Must include at least one digit
    - Must include at least one special character
    """
    def validate(self, password, user=None):
        # Must contain at least one uppercase letter
        if not re.findall(r'[A-Z]', password):
            raise ValidationError(_('Password must contain at least one uppercase letter.'))
        
        # Must contain at least one digit
        if not re.findall(r'\d', password):
            raise ValidationError(_('Password must contain at least one digit.'))
        
        # Must contain at least one special character
        if not re.findall(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError(_('Password must contain at least one special character.'))

    def get_help_text(self):
        return _("Your password must contain at least one uppercase letter, one digit, and one special character.")