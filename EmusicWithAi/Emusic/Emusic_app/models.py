from django.db import models
class Artist(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image_url = models.URLField()

    def __str__(self):
        return self.name

class Song(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='songs')
    image_url = models.URLField()
    spotify_url = models.URLField()

    def __str__(self):
        return self.name
