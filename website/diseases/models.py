from django.db import models

class Folder(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Disease(models.Model):
    name = models.CharField(max_length=200)
    clinical_story = models.TextField()
    pe = models.TextField()
    dd = models.TextField()
    complementary_investigations = models.TextField()
    best_diagnostic_test = models.TextField()
    treatment = models.TextField()
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True, blank=True, related_name='diseases')

    def __str__(self):
        return self.name
