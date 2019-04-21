# -*- coding: utf-8 -*-
#Import der benoetigten Bibliotheken
from StringIO import StringIO
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from time import gmtime, strftime
from reportlab.graphics.barcode import code39
from reportlab.lib.colors import gray
from reportlab.lib.utils import ImageReader

def createpdf(filehandle, data):
    """
    Schreibt eine PDF-Datei
    """

    #Pfad und Dateiname
    timestamp=datetime.now().strftime("%d%m%Y%H%M%S")
    dateiname = "/tmp/certificate.pdf" 

    #c ist ein Objekt der Klasse Canvas
    c = canvas.Canvas(filehandle,pagesize=A4)

    #Metainformationen fuer das PDF-Dokument
    c.setAuthor(u"educorvi GmbH & Co. KG")
    c.setTitle(u"Teilnahmezertifikat Online-Kurs")

    #Variablen 
    schriftart = "Helvetica"
    schriftartfett = "Helvetica-Bold"
    datum = datetime.now().strftime("%d.%m.%Y")

    image = ImageReader(data.get('imageurl'))

    c.drawImage(image, 0*cm, 0*cm, width=20.993*cm, height=29.693*cm)

    c.setFont(schriftart, 36)
    c.drawString(data.get('name_x')*cm, data.get('name_y')*cm, data.get('name'))

    c.setFont(schriftart, 12)
    c.drawString(data.get('datum_x')*cm, data.get('datum_y')*cm, data.get('datum'))

    c.showPage()
    c.save()
    return filehandle
