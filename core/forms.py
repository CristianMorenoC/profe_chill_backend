from django import forms
from allauth.account.forms import SignupForm

class CustomSignupForm(SignupForm):
    ROLES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    
    role = forms.ChoiceField(
        choices=ROLES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='I am a',
    )

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.role = self.cleaned_data['role']
        user.save()
        return user 