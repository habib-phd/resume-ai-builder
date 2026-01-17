import logging
logging.getLogger("transformers").setLevel(logging.ERROR)

from django.shortcuts import render, redirect
from transformers import pipeline

# Load AI model once
generator = pipeline(
    "text-generation",
    model="distilgpt2"
)
generator.tokenizer.pad_token_id = generator.model.config.eos_token_id


def home(request):
    return render(request, 'form.html')

def generate_resume(request):
    if request.method == "POST":
        name = request.POST.get("name")
        experience = request.POST.get("experience")
        skills = request.POST.get("skills")
        education = request.POST.get("education")

        prompt = f"""
        Write a professional resume for this person. Include:
- Full sentences
- Bullet points for each experience and skill
- Summary paragraph at the top.

        Name: {name}
        Experience: {experience}
        Skills: {skills}
        Education: {education}
        """
        print("AI generation started...")
        result = generator(
            prompt,
            max_new_tokens=200,
            do_sample=True,
            temperature=0.7
        )[0]["generated_text"]
        print("AI generation completed!")


        return render(request, "resume_preview.html", {"resume_text": result})

    # GET request should show form again, not redirect
    return render(request, "form.html")


