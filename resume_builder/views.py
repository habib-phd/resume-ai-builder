from django.shortcuts import render
from transformers import pipeline

# Load AI model once
generator = pipeline("text-generation", model="EleutherAI/gpt-neo-1.3B")

def home(request):
    return render(request, 'form.html')

def generate_resume(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        experience = request.POST.get('experience')
        skills = request.POST.get('skills')
        education = request.POST.get('education')

        prompt = f"Create a professional resume for {name}. Experience: {experience}. Skills: {skills}. Education: {education}."
        result = generator(prompt, max_length=250)[0]['generated_text']

        return render(request, 'resume_preview.html', {'resume_text': result})
    return render(request, 'form.html')
