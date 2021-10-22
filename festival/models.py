from django.db import models
from threading import Thread
from .nlp import *
import os


class Photo(models.Model):
    url = models.TextField()

    def __str__(self):
        return "id:{} URL:{}".format(self.id, self.url)


class PhotoComment(models.Model):
    comment = models.TextField(null=False)
    username = models.CharField(max_length=100, null=False)
    date = models.DateTimeField()
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)

    def __str__(self):
        return "comment:{} Photo_id:{}".format(self.comment, self.photo)


class Story(models.Model):
    story = models.TextField(null=False)

    def __str__(self):
        return "id:{} URL:{}".format(self.id, self.story)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Story, self).save(force_insert, force_update, using, update_fields)

        def trigger():
            filename = os.path.join('media',
                                    os.path.join('tts_audio',
                                                 os.path.join('story', 'story-' +
                                                              str(self.id) + '.mp3')))
            text_to_speech(self.story, filename)

        Thread(target=trigger, args=()).start()


class StoryComment(models.Model):
    comment = models.TextField(null=False)
    username = models.CharField(max_length=100, null=False)
    date = models.DateTimeField()
    story = models.ForeignKey(Story, on_delete=models.CASCADE)

    def __str__(self):
        return "comment:{} Photo_id:{}".format(self.comment, self.story)
