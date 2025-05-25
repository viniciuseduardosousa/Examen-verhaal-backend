from django.db import models
import os
import subprocess
from django.core.files import File
from django.conf import settings

from PyPDF4 import PdfFileReader, PdfFileWriter
import os
import subprocess

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
    beschrijving = models.CharField(max_length=500, null=True, blank=True)
    cover_image = models.ImageField(upload_to='verhalen_covers/', null=True, blank=True)
    datum = models.DateField()
    is_uitgelicht = models.BooleanField(default=False)
    is_spotlighted = models.BooleanField(default=False)
    is_downloadable = models.BooleanField(default=False)
    word_file = models.FileField(upload_to='verhalen_pdfs/docx/', null=True, blank=True)
    pdf_file = models.FileField(upload_to='verhalen_pdfs/pdf/', null=True, blank=True)
    url = models.CharField(max_length=200, null=True, blank=True)


    def __str__(self):
        return self.titel

    def convert_to_pdf(self):
        if self.word_file and self.is_downloadable == True:
            docx_path = self.word_file.path
            output_dir = os.path.dirname(docx_path)
            # Convert DOCX to PDF
            subprocess.run([
                '/opt/homebrew/bin/soffice',
                '--headless',
                '--convert-to', 'pdf',
                '--outdir', output_dir,
                docx_path
            ], check=True)

            # Get generated PDF path
            pdf_file_name = os.path.splitext(os.path.basename(docx_path))[0] + '.pdf'
            pdf_path = os.path.join(output_dir, pdf_file_name)

            # Load the watermark PDF
            watermark_path = os.path.join(settings.MEDIA_ROOT, 'watermark.pdf')
            if not os.path.exists(watermark_path):
                raise FileNotFoundError("Watermark file not found.")

            with open(pdf_path, 'rb') as original_pdf_file, open(watermark_path, 'rb') as watermark_file:
                original_pdf = PdfFileReader(original_pdf_file)
                watermark_pdf = PdfFileReader(watermark_file)
                watermark_page = watermark_pdf.getPage(0)

                output_pdf = PdfFileWriter()

                # Apply watermark to each page
                for i in range(original_pdf.getNumPages()):
                    page = original_pdf.getPage(i)
                    page.mergePage(watermark_page)
                    output_pdf.addPage(page)

                # Save watermarked PDF to a temporary file
                watermarked_path = os.path.join(output_dir, f'watermarked_{pdf_file_name}')
                with open(watermarked_path, 'wb') as f_out:
                    output_pdf.write(f_out)

            # Save watermarked PDF to FileField
            with open(watermarked_path, 'rb') as final_pdf:
                self.pdf_file.save(f'watermarked_{pdf_file_name}', File(final_pdf), save=False)

            # Optionally delete temp files
            os.remove(pdf_path)
            os.remove(watermarked_path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save original first
        self.convert_to_pdf()         # Convert and watermark
        super().save(update_fields=['pdf_file'])  # Save updated file
