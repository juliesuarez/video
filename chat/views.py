from .forms import UserCreation
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from .models import Message, UserProfile
from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404, render
from django.views import generic

from django.template.loader import get_template
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from .models import Appointment
from django.contrib.auth.decorators import login_required
from .models import Post, Comment,AppointmentSlot
from .forms import CommentForm, PostForm,AppointmentForm
# Create your views here.

# ---------------------------------------------------------------------------- #
#                             Function Based Views                             #
# ---------------------------------------------------------------------------- #

# --------------------------- Creating User Profile -------------------------- #
def signup(request):
    if request.method == 'POST':
        form = UserCreation(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            ######################### mail system ####################################
            """htmly = get_template('user/Email.html')
            d = { 'username': username }
            subject, from_email, to = 'welcome', 'your_email@gmail.com', email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            ##################################################################
            messages.success(request, f'Your account has been created ! You are now able to log in')
            """
            return redirect('login')
    else:
        form = UserCreation()
    return render(request, 'auth/signup.html', {'form': form})


# ---------------------------------------------------------------------------- #
#                               Class based Views                              #
# ---------------------------------------------------------------------------- #

# ----------------------- Inbox/messages/users list ----------------------- #
class MessagesListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'chat/messages_list.html'
    login_url = '/login/'

    # context data for latest message to display
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = UserProfile.objects.get(pk=self.request.user.pk)  # get your primary key
        messages = Message.get_message_list(user) # get all messages between you and the other user

        other_users = [] # list of other users

        # getting the other person's name fromthe message list and adding them to a list
        for i in range(len(messages)):
            if messages[i].sender != user:
                other_users.append(messages[i].sender)
            else:
                other_users.append(messages[i].recipient)


        context['messages_list'] = messages
        context['other_users'] = other_users
        context['you'] = user
        return context


from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404, render, redirect
from .models import Message, UserProfile

class InboxView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'chat/inbox.html'
    login_url = '/login/'
    queryset = UserProfile.objects.all()

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_object(self):
        UserName = self.kwargs.get("username")
        return get_object_or_404(UserProfile, username=UserName)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = UserProfile.objects.get(pk=self.request.user.pk)
        other_user = UserProfile.objects.get(username=self.kwargs.get("username"))
        messages = Message.get_message_list(user)

        other_users = []

        for i in range(len(messages)):
            if messages[i].sender != user:
                other_users.append(messages[i].sender)
            else:
                other_users.append(messages[i].recipient)

        sender = other_user
        recipient = user

        context['messages'] = Message.get_all_messages(sender, recipient)
        context['messages_list'] = messages
        context['other_person'] = other_user
        context['you'] = user
        context['other_users'] = other_users

        return context


    def post(self, request, *args, **kwargs):
        sender = UserProfile.objects.get(pk=request.POST.get('you'))
        recipient = UserProfile.objects.get(pk=request.POST.get('recipient'))
        message = request.POST.get('message')
        file_upload = request.FILES.get('file_upload')  # Get the uploaded file from the request

        if request.user.is_authenticated:
            if request.method == 'POST':
                if message.strip() or file_upload:  # Check if there's a message or file
                    # Create a new message instance
                    new_message = Message(sender=sender, recipient=recipient, message=message)
                    if file_upload:
                        new_message.file_attachment = file_upload
                    new_message.save()

                return redirect('chat:inbox', username=recipient.username)

        else:
            return render(request, 'auth/login.html')




# -------------------------------- Users list -------------------------------- #
class UserListsView(LoginRequiredMixin, ListView):
    model = UserProfile
    template_name = 'chat/users_list.html'
    context_object_name = 'users'
    login_url = '/login/'

    # context data for the users list
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get your primary key and checking if your are a patient
        user = UserProfile.objects.get(pk=self.request.user.pk, is_patient=self.request.user.is_patient)  # get your primary key and check
        # get all the users except you and a patient (only thrapists to display for chating)
        context['users'] = UserProfile.objects.exclude(pk=user.pk)# get all the users except you
        context['users'] = UserProfile.objects.exclude(is_patient=user.is_patient)
        return context



def Login(request):
    if request.method == 'POST':
  
        # AuthenticationForm_can_also_be_used__
  
        username = request.POST['username']
        password = request.POST['password']
#this is checking for only individual users(patients)
        user = authenticate(request, username = username, password = password)
        if user is not None and user.is_patient==True:

            form = login(request, user)
            messages.success(request, f' welcome {username} !!')
#we change this for tips page.
            return redirect('/patients')
        if user is not None and user.is_teacher==True:

            form = login(request, user)
            messages.success(request, f' welcome {username} !!')
            return redirect('/thrpy')
        
        if user is not None and user.is_organization==True:

            form = login(request, user)
            messages.success(request, f' welcome {username} !!')
            return redirect('/organization')


        else:
            messages.info(request, f'account done not exit plz sign in')
    form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form':form, 'title':'log in'})


#------------------------------Post View-----------------------------------------#
@login_required
def post_list(request):
    tip_type = request.GET.get('tip_type')  # Get the selected tip type from the query parameters

    # Filter posts based on the selected tip type if it's not empty
    if tip_type:
        posts = Post.objects.filter(tip_type=tip_type).order_by("-created_on")
    else:
        posts = Post.objects.order_by("-created_on")

    return render(request, "tip/post_list.html", {"posts": posts})




@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post)
    comment_form = CommentForm()

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('chat:post_detail', pk=post.pk)


    return render(request, 'tip/post_detail.html', {"post": post, "comments": comments, "comment_form": comment_form})

# View for creating a new post (restricted to teachers)
@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = request.user
            post.save()
            return redirect('chat:post_detail', pk=post.pk)

            #return redirect("post_detail", pk=post.pk)  # Use 'post_detail' here
    else:
        form = PostForm()
    return render(request, "tip/post_form.html", {"form": form})

# View for updating an existing post (restricted to teachers)
@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('chat:post_detail', pk=post.pk)

    else:
        form = PostForm(instance=post)
    return render(request, "tip/post_form.html", {"form": form})

# View for liking a post



@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user

    if user in post.liked_by.all():
        post.liked_by.remove(user)  # Remove the user's like
    else:
        post.liked_by.add(user)     # Add the user's like

    return redirect('chat:post_detail', pk=pk)  # Redirect back to the post detail page


@login_required
def patients(request):
    
    tip_type = request.GET.get('tip_type')  # Get the selected tip type from the query parameters

    # Filter posts based on the selected tip type if it's not empty
    if tip_type:
        posts = Post.objects.filter(tip_type=tip_type).order_by("-created_on")
    else:
        posts = Post.objects.order_by("-created_on")


    return render(request, "auth/patient.html", {"posts":posts})


from django.urls import reverse

class CreateAppointmentView(LoginRequiredMixin, CreateView):
    model = Appointment
    template_name = 'create_appointment.html'
    form_class = AppointmentForm

    def form_valid(self, form):
        # Assign the logged-in user as the patient for the appointment
        form.instance.patient = self.request.user

        # Set the assigned therapist based on the form data (selected therapist)
        therapist_id = self.request.POST.get('assigned_to')
        if therapist_id:
            therapist = UserProfile.objects.get(pk=therapist_id)
            form.instance.assigned_to = therapist

        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        # Filter the queryset for the 'assigned_to' field to only include therapists
        form.fields['assigned_to'].queryset = UserProfile.objects.filter(is_teacher=True)

        return form

    def get_success_url(self):
        user = self.request.user

        # Determine the user type (organization or patient)
        if user.is_organization:
            return reverse('chat:QuizListView')  # Use the URL name or pattern name
        else:
            return reverse('chat:patients')  # Use the URL name or pattern name





from django.db.models import Q

class UserAppointmentsView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'user_appointments.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        user = self.request.user

        # If the user is an organization or therapist, show appointments assigned to them
        if user.is_organization or user.is_teacher:
            return Appointment.objects.filter(Q(assigned_to=user) | Q(patient=user))

        # If the user is a patient, show appointments created by them
        elif user.is_patient:
            return Appointment.objects.filter(Q(patient=user) | Q(assigned_to=user))





@login_required
 # Import your UserProfile model or relevant model

def available_therapists(request):
    current_user = request.user
    appointmentslots = AppointmentSlot.objects.filter(therapist=current_user).prefetch_related('conditions')

    if appointmentslots.exists():
        # Therapist has created slots, display them
        return render(request, 'available_therapists.html', {'appointmentslots': appointmentslots})
    else:
        # Therapist has not created slots, show a message
        messages.info(request, "You haven't created any appointment slots yet.")
        return render(request, 'no_appointments.html')









# @login_required
# def user_appointments(request):
#     if request.user.is_teacher:
#         # User is a therapist, retrieve all appointments
#         appointments = Appointment.objects.all()
#     else:
#         # User is not a therapist, retrieve appointments created by the current user (patient)
#         appointments = Appointment.objects.filter(patient=request.user)

#     return render(request, 'user_appointments.html', {'appointments': appointments})

@login_required
def user_appointments(request):
    if request.user.is_teacher:
        # User is a therapist, retrieve appointments assigned to them
        appointments = Appointment.objects.filter(assigned_to=request.user)
    elif request.user.is_organization:
        # User is an organization member, retrieve appointments created by the organization
        appointments = Appointment.objects.filter(patient=request.user)
    else:
        # User is not a therapist or organization member, retrieve appointments created by the patient
        appointments = Appointment.objects.filter(patient=request.user)

    return render(request, 'user_appointments.html', {'appointments': appointments})








from .forms import AppointmentSlotForm
from django.urls import reverse


@login_required
def create_appointment_slot(request):
    if request.method == 'POST':
        form = AppointmentSlotForm(request.POST, user=request.user)
        if form.is_valid():
            appointment_slot = form.save()
            return redirect('/available-therapists')
    else:
        form = AppointmentSlotForm(user=request.user)

    context = {'form': form}
    return render(request, 'create_appointment_slot.html', context)




from django.shortcuts import redirect

@login_required
def edit_appointment_slot(request, slot_id):
    appointment_slot = get_object_or_404(AppointmentSlot, id=slot_id)

    if request.method == 'POST':
        form = AppointmentSlotForm(request.POST, user=request.user, instance=appointment_slot)
        if form.is_valid():
            form.save()
            return redirect('/available-therapists/')  # Redirect to the available therapists page after editing
    else:
        # Initialize the form with the existing appointment slot data
        form = AppointmentSlotForm(instance=appointment_slot, user=request.user)

    context = {'form': form}
    return render(request, 'edit_appointment_slot.html', context)




from django.http import JsonResponse





from django.http import JsonResponse
from django.shortcuts import get_object_or_404

@login_required
def update_appointment_status(request):
    if request.method == 'POST':
        appointment_ids = request.POST.getlist('appointment_ids')

        if appointment_ids:
            # Check if the user is a therapist
            if request.user.is_teacher:
                # Update the status of selected appointments to 'done'
                Appointment.objects.filter(id__in=appointment_ids).update(status='finished')

                # Add a success message to indicate that appointments were marked as done
                messages.success(request, 'Appointments marked as done successfully.')
            else:
                # User is not a therapist, return a forbidden response or handle it as you prefer
                return JsonResponse({'error': 'Permission denied'}, status=403)

    return redirect('chat:finished_appointments')











from django.utils import timezone
from django.http import HttpResponseForbidden

# def finished_appointments(request):
#     # Query the database to get appointments with the 'status' field set to 'done'
#     finished_appointments = Appointment.objects.filter(status='done')

#     # Pass the finished appointments to the template
#     return render(request, 'finished_appointments.html', {'finished_appointments': finished_appointments})


@login_required
def finished_appointments(request):
    if request.user.is_teacher:  # Check if the user is a therapist
        # Query the database to get finished appointments based on status
        finished_appointments = Appointment.objects.filter(status='finished')

        # Pass the finished appointments to the template
        return render(request, 'finished_appointments.html', {'finished_appointments': finished_appointments})
    else:
        # If the user is not a therapist, you can handle it accordingly
        # For example, you can show a message or redirect them to a different page
        return HttpResponseForbidden("Permission denied")



@login_required
def edit_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)

    # Check if the user has permission to edit this appointment
    if not appointment.can_be_edited_by(request.user):
        return HttpResponseForbidden("You don't have permission to edit this appointment.")

    if request.method == 'POST':
        # Instantiate the form with POST data and the appointment instance
        form = AppointmentForm(request.POST, instance=appointment)

        if form.is_valid():
            # Save the updated appointment data
            form.save()
            return redirect(reverse('chat:user_appointments'))  # Redirect to the appointments list
    else:
        # Instantiate the form with the appointment instance for pre-filling
        form = AppointmentForm(instance=appointment)

    return render(request, 'edit_appointment.html', {'form': form, 'appointment': appointment})


from.models import Profile
from.forms import UserProfileForm
from.forms import ProfilePictureForm


@login_required
def user_profile(request):
    user_profile, created = Profile.objects.get_or_create(user=request.user)
    username_form = UserProfileForm(instance=request.user)

    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile.profile_picture = form.cleaned_data['profile_picture']
            user_profile.save()

            # Update the username in the user instance
            username_form = UserProfileForm(request.POST, instance=request.user)
            if username_form.is_valid():
                username_form.save()
                messages.success(request, 'Username and profile picture updated successfully.')  # Success message
                return redirect('chat:user_profile')

    else:
        form = ProfilePictureForm()

    context = {
        'user': request.user,  # Use request.user to get the current user
        'user_profile': user_profile,
        'form': form,
        'username_form': username_form,
    }
    return render(request, 'user_profile.html', context)



@login_required
def view_appointment_slots(request):
    appointment_slots = AppointmentSlot.objects.all()  # Get all appointment slots
    
    context = {
        'appointment_slots': appointment_slots,
    }
    return render(request, 'view_appointment_slots.html', context)
