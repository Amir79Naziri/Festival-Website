from django.shortcuts import render, redirect
from .models import *
from .nlp import *
from datetime import datetime
from threading import Thread
import os


def start_page(request):
    return render(request, 'start_page.html')


def images_festival_page(request):
    photos = Photo.objects.all()
    return render(request, 'images_gallery_page.html', {'photos': photos, 'TYPE': 'image'})


def stories_festival_page(request):
    stories = Story.objects.all()
    return render(request, 'stories_gallery_page.html', {'stories': stories, 'TYPE': 'story'})


def new_comment_page(request, ID, TYPE):
    if request.method == 'POST':
        comment = request.POST['comment']
        username = request.POST['username']

        def comment_checker():
            nonlocal TYPE, ID, comment

            result = emotion_analyzer(str(comment))
            if result['fear'] >= 0.3 or result['disgust'] >= 0.3 or result['anger'] >= 0.5:
                return
            if TYPE == 'image':
                obj = Photo.objects.filter(id=int(ID)).first()
                c = PhotoComment(comment=comment, username=username, photo=obj,
                                 date=datetime.now())
                c.save()
                filename = os.path.join('media',
                                        os.path.join('tts_audio',
                                                     os.path.join('image_comment', 'comment-' +
                                                                  str(ID) + '-' + str(c.id) + '.mp3')))
                text_to_speech(comment, filename)
            else:
                obj = Story.objects.filter(id=int(ID)).first()
                c = StoryComment(comment=comment, username=username, story=obj,
                                 date=datetime.now())
                c.save()
                filename = os.path.join('media',
                                        os.path.join('tts_audio',
                                                     os.path.join('story_comment', 'comment-' +
                                                                  str(ID) + '-' + str(c.id) + '.mp3')))
                text_to_speech(comment, filename)

        Thread(target=comment_checker, args=()).start()

        if TYPE == 'image':
            return redirect('/gallery/images')
        else:
            return redirect('/gallery/stories')
    else:
        if TYPE == 'image':
            o = Photo.objects.filter(id=ID).first()
        else:
            o = Story.objects.filter(id=ID).first()
        return render(request, 'new_comment_page.html',
                      {'ID': ID, 'object': o, 'TYPE': TYPE,
                       'cancel_url': ('images' if TYPE == 'image' else 'stories')})


def view_comments_page(request, ID, TYPE):
    if TYPE == 'image':
        comments = PhotoComment.objects.filter(photo_id=int(ID))
    else:
        comments = StoryComment.objects.filter(story_id=int(ID))

    return render(request,
                  'comments_list_page.html',
                  {'comments': comments,
                   'TYPE': TYPE,
                   'ID': ID,
                   'cancel_url': ('images' if TYPE == 'image' else 'stories')})
