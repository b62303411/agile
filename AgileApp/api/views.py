from django.http import JsonResponse
from ..models import UserStory

def userstory_data(request):
    userstories = UserStory.objects.all().values()
    return JsonResponse(list(userstories), safe=False)
