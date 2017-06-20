from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout

from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic import View

from getagrip_app.models import *
from .forms import *
from django.contrib.admin.models import LogEntry

from django.views.generic import View


@method_decorator(login_required, name='dispatch')
class display_all_tasks(ListView):
    model = tasks_log

    def get_queryset(self):
        return tasks_log.objects.all().order_by('-deadline')


@method_decorator(login_required, name='dispatch')
class new_post(CreateView):
    template_name = 'getagrip_app/tasks_log_form.html'
    form_class = PostForm

    def get_context_data(self, *args, **kwargs):
        context = super(new_post, self).get_context_data(*args, **kwargs)
        context['assigneed_tasks'] = assignees_log.objects.filter(assigneed_to=self.request.user)
        context['tasks_log_list'] = tasks_log.objects.filter(createdBy=self.request.user)
        context['task_objects'] = tasks_log.objects.all()
        return context

    def get_form_kwargs(self):
        kwargs = super(new_post, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.createdBy = self.request.user
        return super(new_post, self).form_valid(form)

    def get_success_url(self):
        return reverse('display_user_tasks')


# class new_post(CreateView):
#     model=tasks_log
#     fields = ['title','description','deadline','state','type','maintask']
#
#     def form_valid(self, form):
#         form.instance.createdBy = self.request.user
#         return super(new_post,self).form_valid(form)
#
#     def get_success_url(self):
#         return reverse('display_user_tasks')

@method_decorator(login_required, name='dispatch')
class display_detailed_task(DetailView):
    model = tasks_log

    def get_context_data(self, *args, **kwargs):
        context = super(display_detailed_task, self).get_context_data(*args, **kwargs)
        context['users_objects'] = User.objects.all()
        context['task_objects'] = tasks_log.objects.all()
        context['assigneed_tasks'] = assignees_log.objects.filter(assigneed_to=self.request.user)
        context['task_log_list'] = tasks_log.objects.filter(createdBy=self.request.user)
        return context

    def get_queryset(self):
        return tasks_log.objects.all()


@method_decorator(login_required, name='dispatch')
class log_entry(ListView):
    model = LogEntry

    def get_queryset(self):
        return LogEntry.objects.all()


@method_decorator(login_required, name='dispatch')
class task_update(UpdateView):
    model = tasks_log
    fields = ['title', 'description', 'deadline', 'state', 'type']

    def get_context_data(self, *args, **kwargs):
        context = super(task_update, self).get_context_data(*args, **kwargs)
        context['assigneed_tasks'] = assignees_log.objects.filter(assigneed_to=self.request.user)
        context['tasks_log_list'] = tasks_log.objects.filter(createdBy=self.request.user)
        return context

    def get_queryset(self):
        return tasks_log.objects.filter(createdBy=self.request.user)

    def get_success_url(self):
        return reverse('display_detailed_task', kwargs={'pk': self.kwargs['pk']})


@method_decorator(login_required, name='dispatch')
class task_delete(DeleteView):
    model = tasks_log

    def get_context_data(self, *args, **kwargs):
        context = super(task_delete, self).get_context_data(*args, **kwargs)
        context['assigneed_tasks'] = assignees_log.objects.filter(assigneed_to=self.request.user)
        context['tasks_log_list'] = tasks_log.objects.filter(createdBy=self.request.user)
        return context

    def get_queryset(self):
        return tasks_log.objects.filter(createdBy=self.request.user)

    def get_success_url(self):
        return reverse('display_user_tasks')


@method_decorator(login_required, name='dispatch')
class display_user_tasks(ListView):
    model = tasks_log

    def get_context_data(self, *args, **kwargs):
        context = super(display_user_tasks, self).get_context_data(*args, **kwargs)
        context['assigneed_tasks'] = assignees_log.objects.filter(assigneed_to=self.request.user)
        return context

    def get_queryset(self):
        return tasks_log.objects.filter(createdBy=self.request.user)

class UserFormView(View):
    form_class = UserForm
    temeplate_name = 'registration/registration_form.html'

    def get(self, request):  # display blang form
        form = self.form_class(None)
        return render(request, self.temeplate_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # cleansed (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # returns user object if he is a normal user
            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('/successful-register/')

        return render(request, self.temeplate_name, {'form': form})


@method_decorator(login_required, name='dispatch')
class UserListView(ListView):
    model = User

    def get_queryset(self):
        return User.objects.all()


@method_decorator(login_required, name='dispatch')
class UserDetailView(DetailView):
    model = User

    def get_context_data(self, *args, **kwargs):
        context = super(UserDetailView, self).get_context_data(*args, **kwargs)
        context['assigneed_tasks'] = assignees_log.objects.filter(assigneed_to=self.request.user)
        context['tasks_log_list'] = tasks_log.objects.filter(createdBy=self.request.user)
        context['task_objects'] = tasks_log.objects.all()
        return context

    def get_queryset(self):
        return User.objects.all()

    def get_success_url(self):
        return reverse('user_detail_view', kwargs={'pk': self.kwargs['pk']})


@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', ]

    def get_context_data(self, *args, **kwargs):
        context = super(UserUpdateView, self).get_context_data(*args, **kwargs)
        context['assigneed_tasks'] = assignees_log.objects.filter(assigneed_to=self.request.user)
        context['tasks_log_list'] = tasks_log.objects.filter(createdBy=self.request.user)
        return context

    def get_queryset(self):
        return User.objects.filter(username=self.request.user.username)

    def get_success_url(self):
        return reverse('user_detail_view', kwargs={'pk': self.kwargs['pk']})


@method_decorator(login_required, name='dispatch')
class UserDeleteView(DeleteView):
    model = User

    def get_context_data(self, *args, **kwargs):
        context = super(UserDeleteView, self).get_context_data(*args, **kwargs)
        context['assigneed_tasks'] = assignees_log.objects.filter(assigneed_to=self.request.user)
        context['tasks_log_list'] = tasks_log.objects.filter(createdBy=self.request.user)
        return context

    def get_queryset(self):
        return User.objects.filter(username=self.request.user.username)

    def get_success_url(self):
        return reverse('index')

