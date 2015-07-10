from django import forms

class CreateAccountForm(forms.Form):
    user_name = forms.CharField(label='Login Name', max_length=128)
    organization = forms.CharField(max_length=256)
    email = forms.EmailField(required=None)
    location = forms.CharField(max_length=512)
    usage = forms.CharField(widget=forms.Textarea, initial="Please tell us how you plan to use this data.")
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label="Re-Enter Password",widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(CreateAccountForm, self).clean()
        if cleaned_data.get('password') != cleaned_data.get('password2'):
            raise forms.ValidationError(
                "You're password does not match in both password boxes."
            )
