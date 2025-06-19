from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from bidi.algorithm import get_display
import arabic_reshaper
from .models import Disease, Folder
from .forms import DiseaseForm, FolderForm
from django.contrib import messages

def generate_pdf(request, pk):
    disease = get_object_or_404(Disease, pk=pk)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="disease_{pk}.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response, pagesize=A4)

    # Register the Arabic font
    pdfmetrics.registerFont(TTFont('Amiri', 'static/fonts/Amiri-Regular.ttf'))

    # Use the font
    p.setFont('Amiri', 14)

    # Reshape and prepare Arabic text for correct display
    def prepare_text(text):
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped_text)
        return bidi_text

    # Margin from right
    margin_right = 40

    # Write content to the PDF with right alignment
    p.drawRightString(550, 800, prepare_text("اسم المرض: " + disease.name))
    p.drawRightString(550, 770, prepare_text("القصة المرضية:"))
    p.drawRightString(550, 740, prepare_text(disease.clinical_story))
    p.drawRightString(550, 710, prepare_text("الفحص السريري:"))
    p.drawRightString(550, 680, prepare_text(disease.pe))
    p.drawRightString(550, 650, prepare_text("التشخيص التفريقي:"))
    p.drawRightString(550, 620, prepare_text(disease.dd))
    p.drawRightString(550, 590, prepare_text("الفحوصات المتممة:"))
    p.drawRightString(550, 560, prepare_text(disease.complementary_investigations))
    p.drawRightString(550, 530, prepare_text("أفضل اختبار تشخيصي:"))
    p.drawRightString(550, 500, prepare_text(disease.best_diagnostic_test))
    p.drawRightString(550, 470, prepare_text("العلاج:"))
    p.drawRightString(550, 440, prepare_text(disease.treatment))

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    return response

def prepare_text(text):
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    return bidi_text

def disease_list(request):
    folders = Folder.objects.all()
    return render(request, 'disease_list.html', {'folders': folders})

def disease_detail(request, pk):
    disease = get_object_or_404(Disease, pk=pk)
    return render(request, 'disease_detail.html', {'disease': disease})

def disease_new(request):
    if request.method == "POST":
        form = DiseaseForm(request.POST)
        if form.is_valid():
            disease = form.save()
            return redirect('disease_detail', pk=disease.pk)
    else:
        form = DiseaseForm()
    return render(request, 'disease_new.html', {'form': form})


def disease_edit(request, pk):
    disease = get_object_or_404(Disease, pk=pk)
    if request.method == "POST":
        form = DiseaseForm(request.POST, instance=disease)
        if form.is_valid():
            disease = form.save()
            return redirect('disease_detail', pk=disease.pk)
    else:
        form = DiseaseForm(instance=disease)
    folders = Folder.objects.all()
    return render(request, 'disease_edit.html', {'form': form, 'folders': folders, 'disease': disease})

def delete_disease(request, pk):
    disease = get_object_or_404(Disease, pk=pk)
    if request.method == "POST":
        disease.delete()
        return redirect('disease_list')
    return render(request, 'disease_confirm_delete.html', {'disease': disease})

def download_all_diseases(request):
    diseases = Disease.objects.all().order_by('name')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="all_diseases.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    pdfmetrics.registerFont(TTFont('Amiri', 'static/fonts/Amiri-Regular.ttf'))
    p.setFont('Amiri', 12)

    y = 800
    for disease in diseases:
        if y < 100:
            p.showPage()
            p.setFont('Amiri', 12)
            y = 800

        p.drawRightString(550, y, prepare_text("اسم المرض: " + disease.name))
        y -= 20
        p.drawRightString(550, y, prepare_text("التاريخ السريري:"))
        y -= 20
        p.drawRightString(550, y, prepare_text(disease.clinical_story))
        y -= 20
        p.drawRightString(550, y, prepare_text("الفحص السريري:"))
        y -= 20
        p.drawRightString(550, y, prepare_text(disease.pe))
        y -= 20
        p.drawRightString(550, y, prepare_text("التشخيص التفريقي:"))
        y -= 20
        p.drawRightString(550, y, prepare_text(disease.dd))
        y -= 20
        p.drawRightString(550, y, prepare_text("الفحوصات التكميلية:"))
        y -= 20
        p.drawRightString(550, y, prepare_text(disease.complementary_investigations))
        y -= 20
        p.drawRightString(550, y, prepare_text("أفضل اختبار تشخيصي:"))
        y -= 20
        p.drawRightString(550, y, prepare_text(disease.best_diagnostic_test))
        y -= 20
        p.drawRightString(550, y, prepare_text("العلاج:"))
        y -= 20
        p.drawRightString(550, y, prepare_text(disease.treatment))
        y -= 40

    p.showPage()
    p.save()
    return response

def add_folder(request):
    if request.method == "POST":
        form = FolderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('disease_list')
    else:
        form = FolderForm()
    return render(request, 'add_folder.html', {'form': form})


def delete_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)

    # Prevent deletion if diseases exist in this folder
    if folder.diseases.exists():
        messages.warning(request, "لا يمكنك حذف هذا المجلد لأنه يحتوي على أمراض مرتبطة به.")
    else:
        folder.delete()
        messages.success(request, "تم حذف المجلد بنجاح.")

    return redirect('disease_list')


