from django.contrib.auth.forms import UserCreationForm
from django import forms

#

from django.db import transaction
from django.forms.utils import ValidationError


from .models import *
from .models import Comment,Post,Appointment


# ---------------------------------------------------------------------------- #
#                   creating a form to allow users to sign up                  #
# ---------------------------------------------------------------------------- #

# ----------------------------- USer signup form ----------------------------- #
class UserCreation(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'phone')

    def save(self, commit=True):
        user = super(UserCreation, self).save(commit=False)
        if commit:
            user.is_active = True
            user.is_patient = True
            user.save()

        return user

# form for the thrapist

class TeacherSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserProfile
        fields = ('username', 'email', 'phone')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user

class OrganizationSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserProfile
        fields = ('username', 'email', 'phone','organization_name','location','representative_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_organization = True
        if commit:
            user.save()
        return user





class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'tip_type', 'content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    content = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'tiktok-comment-input', 'placeholder': 'Add a comment...'}),
        label=''
    )

from datetime import datetime 
from django.forms.widgets import SelectDateWidget

 # Import the AppointmentSlot model

from django import forms
from .models import AppointmentSlot

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['assigned_to', 'date', 'time', 'description']

    date = forms.DateField(
        widget=forms.SelectDateWidget(
            empty_label=("Choose Year", "Choose Month", "Choose Day"),
            attrs={'class': 'date-dropdown-widget'}
        )
    )

    time = forms.ChoiceField(choices=[], required=False)  # Use ChoiceField for time

    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 40}))

    def clean_time(self):
        time = self.cleaned_data['time']
        try:
            # Attempt to parse the time using strptime
            parsed_time = datetime.strptime(time, '%I:%M %p').time()
            return parsed_time
        except ValueError:
            raise forms.ValidationError("Enter a valid time in 'hh:mm AM/PM' format.")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set the initial choices for the 'time' field (predefined choices)
        self.fields['time'].choices = [
            ('7:00 AM', '7:00 AM - 11:00 AM'),
            ('11:00 AM', '11:00 AM - 3:00 PM'),
            ('3:00 PM', '3:00 PM - 5:00 PM')
        ]

        # Query therapists who have created appointment slots
        therapists_with_slots = AppointmentSlot.objects.values_list('therapist__id', 'therapist__username').distinct()
        
        # Create choices for the 'assigned_to' field based on therapists with slots
        therapist_choices = [(therapist[0], therapist[1]) for therapist in therapists_with_slots]
        
        # Set the choices for the 'assigned_to' field
        self.fields['assigned_to'].choices = therapist_choices



# from .models import AppointmentSlot

# class AppointmentSlotForm(forms.ModelForm):
#     class Meta:
#         model = AppointmentSlot
#         fields = [ 'therapist','time_slot']

#         time_slots = forms.MultipleChoiceField(
#         choices=[('7:00 AM', '7:00 AM - 11:00 AM'), ('11:00 AM', '11:00 AM - 3:00 PM'), ('3:00 PM', '3:00 PM - 5:00 PM')],
#         widget=forms.CheckboxSelectMultiple,
#     )



class AppointmentSlotForm(forms.ModelForm):

    conditions = forms.ModelMultipleChoiceField(
        queryset=MentalHealthCondition.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    class Meta:
        model = AppointmentSlot
        fields = ['therapist', 'time_slot','location','my_service','therapist_category','therapist_type','conditions']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filter the queryset for the therapist field to include only therapists
        if user and user.is_teacher:
            self.fields['therapist'].queryset = UserProfile.objects.filter(is_teacher=True)

        # You can customize the choices for the 'time_slot' field here if needed
        self.fields['time_slot'].choices = [
            ('7:00 AM - 8:00 AM', '7:00 AM - 8:00 AM'),
            ('8:00 AM - 9:00 AM', '8:00 AM - 9:00 AM'),
            ('9:00 AM - 10:00 AM', '9:00 AM - 10:00 AM'),
            # Add more time slots as needed
        ]

def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        time_slot_choices = kwargs.pop('time_slot_choices', None)
        # super().__init__(*args, **kwargs)

        if user and user.is_teacher:
            self.fields['therapist'].queryset = UserProfile.objects.filter(is_teacher=True)

        if time_slot_choices:
            self.fields['time_slot'].choices = time_slot_choices

        # # Customize the labels for the MentalHealthCondition fields
        # for field_name in MentalHealthCondition._meta.get_fields():
        #     if isinstance(field_name, models.Field):
        #         label = field_name.verbose_name
        #         self.fields[field_name.name].label = label



from .models import Profile
class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username']
        