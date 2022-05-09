from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import*
# Create your views here.

def comment(request):
    comments = Comment.objects.all()
    content = {'comments' : comments}
    return render(request, 'comment/comment.html', content)

def createComment(request):
    user_comment = request.POST['Comment']
    new_comment = Comment(content = user_comment)
    new_comment.save()
    return HttpResponseRedirect(reverse('comment'))
    # return HttpResponse("createCommet를 할거야 =>" + user_comment)

def deleteComment(request):
    delete_comment_id = request.GET['todoNum']
    # print("완료한 todo의 id", delete_comment_id)
    comment = Comment.objects.get(id = delete_comment_id)
    comment.delete()
    return HttpResponseRedirect(reverse('comment'))