from django.conf.urls import url
from . import views
from . import getagrip_crud

urlpatterns = [
    url(r'^allTasks', getagrip_crud.display_all_tasks.as_view(), name='allTasks'),
    url(r'^newTask$', getagrip_crud.new_post.as_view(), name='newTask'),
    url(r'^(?P<pk>[0-9]+)/$', getagrip_crud.display_detailed_task.as_view(), name='display_detailed_task'),
    url(r'^(?P<pk>[0-9]+)/update/$', getagrip_crud.task_update.as_view(), name='task_update'),
    url(r'^(?P<pk>[0-9]+)/delete/$', getagrip_crud.task_delete.as_view(), name='task_delete'),
    url(r'^userTasks/$', getagrip_crud.display_user_tasks.as_view(), name='display_user_tasks'),

    url(r'^logs/$', getagrip_crud.log_entry.as_view(), name='logs'),

    url(r'^(?P<task_id>[0-9]+)/comment/post/(?P<comment_text>.*)/$', views.task_comment, name='task_comment'),
    url(r'^(?P<task_id>[0-9]+)/comment/(?P<comment_id>[0-9]+)/delete/$', views.comment_delete,
        name='task_comment_delete'),

    url(r'^(?P<task_id>[0-9]+)/assignee/(?P<assignee_id>[0-9]+)/$', views.task_assignee, name='task_assignee'),
    url(r'^(?P<task_id>[0-9]+)/assignee/(?P<assignee_id>[0-9]+)/delete/$', views.assignee_delete,
        name='task_assignee_delete'),

    url(r'^help/$', views.contact,
        name='contact'),

]
