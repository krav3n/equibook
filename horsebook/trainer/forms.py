
# django imports
from django import forms


class ChangePasswordForm(forms.BaseForm):
    """
    This form should be used when any user wants to change the password for his account
    """

    def __init__(self, *args, **kwargs):
        pass
