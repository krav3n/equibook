# Create the form class.

from django.forms import ModelForm

from horsebook.student.models import Student


class StudentSignupForm(ModelForm):

    class Meta:
        model = Student
        fields = [
            'username', 'password1', 'password2', 'email', 'phone',
        ]
