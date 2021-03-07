from dashboard.models import Project,User

def access_pid(request):

    project = Project.objects.filter(user_id=request.user.id, pk=1).values_list()
    p = list(project)

