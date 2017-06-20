from django.shortcuts import render
from django.http import Http404
from django.shortcuts import redirect
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template import Context
from django.template.loader import get_template
from getagrip_app.models import *
from django.contrib.auth import logout
from getagrip_app.forms import ContactForm


def index(request):
    return render(request, "registration/index.html")

def successfulRegister(request):
    return render(request, "registration/successfulRegister.html")

def task_comment(request, task_id, comment_text):
    current_user = request.user
    try:
        task = tasks_log.objects.get(id=task_id)
        comment = comments_log(task=task, commented_by=current_user, comment=comment_text)
        if current_user == comment.commented_by:
            comment.save()
        else:
            pass

    except:
        raise Http404("<h1>Cannot Find the Requested Comment or something went wrong<h1>")
    return redirect('/getagrip/' + str(task_id) + '/')


def comment_delete(request, task_id, comment_id):
    current_user = request.user
    try:
        comment = comments_log.objects.get(id=comment_id)
        if current_user == comment.commented_by:
            comment.delete()
        else:
            pass
    except:
        raise Http404("<h1>Cannot Find the Requested comment or something went wrong<h1>")
    return redirect('/getagrip/' + str(task_id) + '/')


def task_assignee(request, task_id, assignee_id):
    current_user = request.user
    try:
        task = tasks_log.objects.get(id=task_id)
        user = User.objects.get(id=assignee_id)
        assignee = assignees_log(task=task, assigneed_to=user)
        if not assignees_log.objects.filter(task=task_id,
                                            assigneed_to=assignee_id).exists() and current_user == task.createdBy:
            assignee.save()
        else:
            pass

    except:
        raise Http404("<h1>Cannot Find the Requested Assignee or something went wrong<h1>")
    return redirect('/getagrip/' + str(task_id) + '/')


def assignee_delete(request, task_id, assignee_id):
    current_user = request.user
    try:
        task = tasks_log.objects.get(id=task_id)
        assignee = assignees_log.objects.get(id=assignee_id)

        if current_user == task.createdBy:
            assignee.delete()
        else:
            pass

    except:
        raise Http404("<h1>Cannot Find the Requested Assignee or something went wrong<h1>")

    return redirect('/getagrip/' + str(task_id) + '/')


def logout_view(request):
    logout(request)
    return redirect('/login/')

def contact(request):
    form_class = ContactForm

    # new logic!
    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get('contact_name', '')
            contact_email = request.POST.get('contact_email', '')
            form_content = request.POST.get('content', '')

            # Email the profile with the
            # contact information
            template =get_template('registration/contact_template.txt')
            context = Context({
                'contact_name': contact_name,
                'contact_email': contact_email,
                'form_content': form_content,
            })
            content = template.render(context)

            email = EmailMessage(
                "New contact form submission",
                content,
                "Get-A-Grip" +'',
                ['dasamantarao.aditya@gmail.com'],
                headers = {'Reply-To': contact_email }
            )
            email.send()
            return redirect('display_user_tasks')

    return render(request, 'registration/contact.html', {
        'form': form_class,
    })
