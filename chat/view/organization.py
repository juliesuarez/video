from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from ..decorators import organization_required
from ..forms import OrganizationSignUpForm
from ..models import UserProfile
from ..models import Post



class OrganizationSignUpView(CreateView):
    model = UserProfile
    form_class = OrganizationSignUpForm
    template_name = 'registration/org.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'organization'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/thrpy')


def QuizListView(request):
    if request.user.is_authenticated:
        tip_type = request.GET.get('tip_type')  # Get the selected tip type from the query parameters

    # Filter posts based on the selected tip type if it's not empty
        if tip_type:
            posts = Post.objects.filter(tip_type=tip_type).order_by("-created_on")
        else:
            posts = Post.objects.order_by("-created_on")
            return render(request, 'auth/organization.html', {"posts": posts})

    return render(request, 'classroom/home.html')
