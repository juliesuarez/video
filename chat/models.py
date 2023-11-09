from django.db import models
from django.contrib.auth.models import AbstractUser,User
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse




# Create your models here.

# ---------------------------------------------------------------------------- #
#                                  User Model                                  #
# ---------------------------------------------------------------------------- #

class UserProfile(AbstractUser):
    is_patient = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_organization = models.BooleanField(default=False)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    title = models.CharField(max_length=50, unique=False)
    organization_name=models.CharField(max_length=50,default='Organization')
    location=models.CharField(max_length=50,default='Location')
    representative_name=models.CharField(max_length=50,default='Name')
    
    def __str__(self):
        return self.username

    class Meta:
        db_table = 'chat_users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'


def get_mental_health_conditions(self):
        conditions = MentalHealthCondition.objects.all()
        condition_names = [condition.name for condition in conditions]
        return ", ".join(condition_names)

# thrapist


# ---------------------------------------------------------------------------- #
#                                 Message Model                                #
# ---------------------------------------------------------------------------- #
class Message(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='recipient')
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    file_attachment = models.FileField(upload_to='message_attachments/', blank=True, null=True)

    def __str__(self):
        return self.message

    class Meta:
        db_table = 'chat_messages'
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ('-date',)

    # function gets all messages between 'the' two users (requires your pk and the other user pk)
    def get_all_messages(id_1, id_2):
        messages = []
        # get messages between the two users, sort them by date(reverse) and add them to the list
        message1 = Message.objects.filter(sender_id=id_1, recipient_id=id_2).order_by('-date') # get messages from sender to recipient
        for x in range(len(message1)):
            messages.append(message1[x])
        message2 = Message.objects.filter(sender_id=id_2, recipient_id=id_1).order_by('-date') # get messages from recipient to sender
        for x in range(len(message2)):
            messages.append(message2[x])

        # because the function is called when viewing the chat, we'll return all messages as read
        for x in range(len(messages)):
            messages[x].is_read = True
        # sort the messages by date
        messages.sort(key=lambda x: x.date, reverse=False)
        return messages

    # function gets all messages between 'any' two users (requires your pk)
    def get_message_list(u):
        # get all the messages
        m = []  # stores all messages sorted by latest first
        j = []  # stores all usernames from the messages above after removing duplicates
        k = []  # stores the latest message from the sorted usernames above
        for message in Message.objects.all():
            for_you = message.recipient == u  # messages received by the user
            from_you = message.sender == u  # messages sent by the user
            if for_you or from_you:
                m.append(message)
                m.sort(key=lambda x: x.sender.username)  # sort the messages by senders
                m.sort(key=lambda x: x.date, reverse=True)  # sort the messages by date

        # remove duplicates usernames and get single message(latest message) per username(other user) (between you and other user)
        for i in m:
            if i.sender.username not in j or i.recipient.username not in j:
                j.append(i.sender.username)
                j.append(i.recipient.username)
                k.append(i)

        return k

STATUS = ((0, "Draft"), (1, "Publish"))


class Post(models.Model):
    DAY = 'day'
    MONTH = 'month'
    WEEK = 'week'
    TIP_TYPE_CHOICES = [
        (DAY, 'Day'),
        (MONTH, 'Month'),
        (WEEK, 'Week'),
    ]

    title = models.CharField(max_length=200, unique=True)
    tip_type = models.CharField(max_length=10, choices=TIP_TYPE_CHOICES)
    content = models.TextField()
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        limit_choices_to={'is_teacher': True},  # Only allow teachers to create tips
        related_name="created_tips"
    )
    created_on = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField(get_user_model(), related_name="liked_posts", blank=True)
    commented_by = models.ManyToManyField(get_user_model(), related_name="commented_posts", blank=True)
    status = models.IntegerField(choices=STATUS,default=0)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"



STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('finished', 'Finished'),
    # Add more choices as needed
)


from django.urls import reverse

class Appointment(models.Model):
    assigned_to = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='assigned_appointments', null=True, blank=True)
    patient = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='created_appointments', null=True, blank=True)
    organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='organization_appointments', null=True, blank=True)
    title = models.CharField(max_length=200, null=False, blank=False)
    client_Name = models.CharField(max_length=50, null=False, blank=False)
    date = models.DateField()
    time = models.TimeField(null=False, blank=False)
    description = models.TextField(max_length=1000, null=False, blank=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_done = models.BooleanField(default=False)

    def can_be_edited_by(self, user):
        # Define who can edit the appointment
        return user == self.patient or user == self.assigned_to or user == self.organization

    def get_absolute_url(self):
        return reverse('user_appointments')

    def __str__(self):
        return self.title

    

class MentalHealthCondition(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class AppointmentSlot(models.Model):
    LOCATION_CHOICES = [
        ('Makerere University School of Psychology', 'Makerere University School of Psychology'),
        ('Makerere University School of Guidance & Counselling', 'Makerere University School of Guidance & Counselling'),
        ('Safe Places – Kyambogo', 'Safe Places – Kyambogo'),
        ('Makerere University Business School', 'Makerere University Business School'),
    ]

    therapist = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    conditions = models.ManyToManyField(MentalHealthCondition)
    therapist_title_choices = [
        ('Counselor', 'Counselor'),
        ('Clinical counsellor','Clinical counsellor'),
        ('Clinical Psychologist', 'Clinical Psychologist'),
        ('Psychiatrist', 'Psychiatrist'),
    ]
    my_service = models.CharField(
        max_length=200,
        choices=therapist_title_choices,
        default='Therapist', 
    )

    therapist_category_choices = [
        ('Cognitive Behavioral Therapy (CBT)', 'Cognitive Behavioral Therapy (CBT)'),
        ('Psychoanalysis or Psychodynamic','Psychoanalysis or Psychodynamic'),
        ('Therapy', 'Therapy'),
    ]
    therapist_category = models.CharField(
        max_length=200,
        choices=therapist_category_choices,
        default='None', 
    )
    therapist_type_choices = [
        ('Cognitive Therapy (CT)', 'Cognitive Therapy (CT)'),
        ('Dialectical Behavioral','Dialectical Behavioral'),
        ('Emotive Behavior Therapy', 'Emotive Behavior Therapy'),
        ('Cognitive Processing Therapy', 'Cognitive Processing Therapy'),
        ('Dream interpretation', 'Dream interpretation'),
        ('Free Association', 'Free Association'),
        ('Transference', 'Transference'),
    ]
    therapist_type = models.CharField(
        max_length=200,
        choices=therapist_type_choices,
        default='None', 
    )
    time_slot = models.CharField(max_length=50, choices=[
        ('7:00 AM - 8:00 AM', '7:00 AM - 8:00 AM'),
        ('8:00 AM - 9:00 AM', '8:00 AM - 9:00 AM'),
        ('9:00 AM - 10:00 AM', '9:00 AM - 10:00 AM'),
        # Add more time slots as needed
    ])
    location = models.CharField(max_length=100, choices=LOCATION_CHOICES,null=False,blank=False,default=False)

    def __str__(self):
        return f"{self.therapist.username} - {self.time_slot}"

    


    
class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    

    def _str_(self):
        return self.user.username

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Signal to automatically create a UserProfile when a User is created
from django.db.models.signals import post_save
post_save.connect(create_user_profile, sender=get_user_model())




