from django.shortcuts import render
from django.http import HttpResponse
from decouple import config
import openai
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# Load OpenAI API key from .env
openai.api_key = config("OPENAI_API_KEY")

def generate_ai_resume(data):
    prompt = f"""
Create a professional USA-standard resume for:

Name: {data['name']}
Email: {data['email']}
Phone: {data['phone']}
Address: {data['address']}
Objective: {data['objective']}
Skills: {data['skills']}
Experience: {data['experience']}
Education: {data['education']}
Languages: {data['languages']}

Format it in clean sections with bullet points, headings, and proper spacing. 
Do not include extra commentary.
"""
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    resume_text = response.choices[0].message.content
    return resume_text


def home(request):
    return render(request, "form.html")


def generate_resume(request):
    if request.method == "POST":
        data = {
            "name": request.POST.get("name", "Habibullah Rahimi"),
            "email": request.POST.get("email", "[email protected]"),
            "phone": request.POST.get("phone", "[your phone]"),
            "address": request.POST.get("address", "[your address]"),
            "objective": request.POST.get("objective", "Web Developer seeking new challenges."),
            "skills": request.POST.get("skills", "Python, Django, Laravel, HTML, CSS, JavaScript"),
            "experience": request.POST.get("experience", "Web Developer at Company A, Web Developer at Company B"),
            "education": request.POST.get("education", "Bachelor of Computer Science"),
            "languages": request.POST.get("languages", "English"),
        }

        resume_text = generate_ai_resume(data)

        request.session["resume_text"] = resume_text
        return render(request, "resume_preview.html", {"resume_text": resume_text})

    return render(request, "form.html")


def download_pdf(request):
    resume_text = request.session.get("resume_text")
    if not resume_text:
        return HttpResponse("No resume found", status=400)

    pdfmetrics.registerFont(
        TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    )

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="resume.pdf"'

    c = canvas.Canvas(response, pagesize=LETTER)
    c.setFont("DejaVu", 12)

    width, height = LETTER
    y = height - 50
    for line in resume_text.split("\n"):
        line = line.strip()
        if not line:
            continue
        # Bold headings
        if line.endswith(":") or line.isupper():
            c.setFont("DejaVu", 14)
        else:
            c.setFont("DejaVu", 12)
        # Bullet points
        if line.startswith("-") or line.startswith("•"):
            line = "• " + line.lstrip("-• ")
        c.drawString(50, y, line)
        y -= 18
        if y < 50:
            c.showPage()
            y = height - 50
    c.save()
    return response
