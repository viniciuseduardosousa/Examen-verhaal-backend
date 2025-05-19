from django.db import models
import os
import subprocess
from django.core.files import File

# class User(models.Model):
#     naam = models.CharField(max_length=200)
#     email = models.EmailField()
#     wachtwoord = models.CharField(max_length=200)

#     def __str__(self):
#         return self.naam

class Categorie(models.Model):
    naam = models.CharField(max_length=200)
    cover_image = models.ImageField(upload_to='categorie_covers/', null=True, blank=True)
    is_uitgelicht = models.BooleanField(default=False)

    def __str__(self):
        return self.naam

class Verhaal(models.Model):
    titel = models.CharField(max_length=200)
    tekst = models.TextField()
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    is_onzichtbaar = models.BooleanField(default=False)
    beschrijving = models.CharField(max_length=500)
    cover_image = models.ImageField(upload_to='verhalen_covers/', null=True, blank=True)
    datum = models.DateField()
    is_uitgelicht = models.BooleanField(default=False)
    is_spotlighted = models.BooleanField(default=False)
    is_downloadable = models.BooleanField(default=False)
    word_file = models.FileField(upload_to='verhalen_pdfs/docx/', null=True, blank=True)
    pdf_file = models.FileField(upload_to='verhalen_pdfs/pdf/', null=True, blank=True)


    def __str__(self):
        return self.titel

    def convert_to_pdf(self):
        if self.word_file:
            # Absolute path to the docx
            docx_path = self.word_file.path
            output_dir = os.path.dirname(docx_path)

            # Convert with LibreOffice
            subprocess.run([
                '/opt/homebrew/bin/soffice',
                '--headless',
                '--convert-to', 'pdf',
                '--outdir', output_dir,
                docx_path
            ], check=True)

            # Construct expected output PDF file path
            pdf_file = os.path.splitext(os.path.basename(docx_path))[0] + '.pdf'
            pdf_path = os.path.join(output_dir, pdf_file)

            # Save to FileField
            with open(pdf_path, 'rb') as f:
                self.pdf_file.save(pdf_file, File(f), save=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save initial file first
        self.convert_to_pdf()         # Convert after saving
        super().save(update_fields=['pdf_file'])  # Save only pdf field

