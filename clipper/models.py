from django.db import models

# 추가 
class Site(models.Model):
    name = CharField(max_length=100)

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(max_length=200)
    thumbnail_link = models.URLField(null=True)
    description = models.TextField(null=True)
    instructor = models.CharField(max_length=100, null=True)
    course_link = models.URLField()
    site = models.ForeignKey(Site, on_delete=models.CASCADE) # add 

    def __str__(self):
        return self.title


class Chapter(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)    
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class Section(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

