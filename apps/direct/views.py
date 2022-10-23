
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone


from apps.user.models import CustomUser
from apps.direct.models import Message

@login_required
def inbox(request):
    user = request.user
    messages = Message.get_message(user=request.user)
    active_direct = None
    directs = None
    profile = get_object_or_404(CustomUser, username=user)

    if 'search-button' in request.GET:
            finding_word = request.GET.get('search_word')
            title = 'Search - "'+finding_word+'"'
            if finding_word != '':
                    accounts = CustomUser.objects.filter(Q(username__icontains=finding_word) | Q(first_name__startswith=finding_word) | Q(last_name__startswith=finding_word)   )
            return render(request, 'users_list.html', locals())

    if messages:
        message = messages[0]
        active_direct = message['user'].username
        directs = Message.objects.filter(user=request.user, reciepient=message['user'])
        len_direct = len(directs)
        directs.update(is_read=True)
            


        for message in messages:
            if message['user'].username == active_direct:
                message['unread'] = 0
        if len(CustomUser.objects.filter(username=active_direct)) > 0:
            recep = CustomUser.objects.get(username=active_direct)

        
        context = {
        'directs':directs,
        'messages': messages,
        'active_direct': active_direct,
        'profile': profile,
        'recep':recep

     
    }
    else:
        context={}
    
    return render(request, 'directs/direct.html', context)


@login_required
def Directs(request, username):
    user  = request.user
    messages = Message.get_message(user=user)
    active_direct = username
    directs = Message.objects.filter(user=user, reciepient__username=username)  
    directs.update(is_read=True)

    active_user = CustomUser.objects.get(username=username)

    
    




    for message in messages:
            if message['user'].username == username:
                message['unread'] = 0
    context = {
        'directs': directs,
        'messages': messages,
        'active_direct': active_direct,
        'recep': active_user
    }


    
    if 'search-button' in request.GET:
            finding_word = request.GET.get('search_word')
            title = 'Search - "'+finding_word+'"'
            if finding_word != '':
                    accounts = CustomUser.objects.filter(Q(username__icontains=finding_word) | Q(first_name__startswith=finding_word) | Q(last_name__startswith=finding_word)   )
            return render(request, 'users_list.html', locals())
    return render(request, 'directs/direct.html', context)




def SendDirect(request):
    from_user = request.user
    to_user_username = request.POST.get('to_user')
    body = request.POST.get('body')
    if body.strip() != '':
        if request.method == "POST":
            to_user = CustomUser.objects.get(username=to_user_username)
            Message.sender_message(from_user, to_user, body)
            return redirect('message')
    else:
        return redirect('message')



def NewConversation(request, username):
    from_user = request.user
    body = '⠀'

    to_user = CustomUser.objects.get(username=username)

    if from_user != to_user:
        Message.sender_message(from_user, to_user, body)
    return redirect('message')


def delete_message(request, id, username):
    message = Message.objects.get(id=id)
    message.delete()
    return redirect('directs', username )
