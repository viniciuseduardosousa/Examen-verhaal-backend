from django.db import models

# class User(models.Model):
#     naam = models.CharField(max_length=200)
#     email = models.EmailField()
#     wachtwoord = models.CharField(max_length=200)

#     def __str__(self):
#         return self.naam

class Categorie(models.Model):
    naam = models.CharField(max_length=200)

    def __str__(self):
        return self.naam

class Verhaal(models.Model):
    titel = models.CharField(max_length=200)
    tekst = models.TextField()
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    is_onzichtbaar = models.BooleanField(default=False)
    beschrijving = models.CharField(max_length=200)
    cover_image = models.ImageField(upload_to='verhalen_covers/')
    datum = models.DateField()


    def __str__(self):
        return self.titel


