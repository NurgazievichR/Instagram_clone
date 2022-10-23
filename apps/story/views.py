from django.shortcuts import redirect, render
from django.views import generic

from apps.story.models import Story
from apps.user.models import CustomUser
from apps.user.utils import get_id_by_username
from apps.user.tasks import delete_story



class StoriesView(generic.ListView):
    model = Story
    template_name = 'stories/story.html'
    context_object_name = 'stories'
    paginate_by = 1

    def get_queryset(self):
        id = get_id_by_username(self.kwargs['username'])
        return super().get_queryset().filter(user=id)
    
    def post(self, request, *args, **kwargs):
        if 'delete_story' in request.POST:
            story_id = request.POST['delete_story']
            Story.objects.get(id=story_id).delete()
            if len(Story.objects.filter(user=self.request.user)) > 0:
                return redirect('story', self.request.user)
            else:
                return redirect('index')




def ImageOrVideo(request):
    return render(request, 'stories/video_or_image.html')


def addVideoStory(request):
    if request.method == 'POST' and str(request.FILES['video']).split('.')[1] in ['mp4', 'mov','jpg', 'jpeg','png']:
        story = Story.objects.create(user=request.user, file=request.FILES['video'])   
        delete_story.delay(id_story=story.id)
        return redirect('index')
    return render(request, 'stories/add_video_story.html')