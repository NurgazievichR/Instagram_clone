from django.db.models import F
from django.utils import timezone

from apps.user.models import Activity, CustomUser

class ActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def activity(self):
        if not Activity.objects.all():    
            Activity.objects.create(all_time=0, today=0)
        ids = Activity.objects.all().last().pk
        last = Activity.objects.filter(id=ids)
        last.update(today=F('today')+1)
        Activity.objects.all().update(all_time=F('all_time')+1)
        if last[0].date != timezone.now().date():
            Activity.objects.create(today=0, all_time=last[0].all_time, date=timezone.now().date())

        
    
    def last_activity(self, request):
        user = CustomUser.objects.filter(username=request.user)
        user.update(last_activity=timezone.now())

    def __call__(self, request):
        response = self.get_response(request)
        self.last_activity(request)
        if '/admin' not in request.path_info:
            self.activity()
        return response

        