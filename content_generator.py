import openai
import os
import re

# Ensure to replace with your OpenAI API Key
openai.api_key = os.environ['OPENAI_API_KEY']

def generate_excerpt(title):
    prompt = f"Provide a brief teaser or preview for a blog post titled '{title}' about the Australian mortgage market."
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=50,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error in excerpt generation: {str(e)}")
        return None

def generate_slug(title):
    slug = "-".join(title.lower().split())
    slug = ''.join(e for e in slug if e.isalnum() or e == '-')
    return slug

def generate_content(title, max_tokens=150, temperature=0.7):
    
    def get_gpt_response(prompt):
        return openai.Completion.create(
            engine='gpt-3.5-turbo-0613',
            prompt=prompt,
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.7
        ).choices[0].text.strip()
    
    def get_intro_and_conclusion(title):
        intro_prompt = f"You are an Australian mortgage broker writing blog content for your website. Write an introduction for a blog post with the title: '{title}'"
        conclusion_prompt = f"You are an Australian mortgage broker writing a blog post titled '{title}'. Your firm is called Ello Lending. Write a conclusion for a blog post with the title: '{title}'. Emphasize how your firm would love to help and answer questions and encourage the reader to contact you"
        intro = get_gpt_response(intro_prompt)
        conclusion = get_gpt_response(conclusion_prompt)
        return intro, conclusion

    intro, conclusion = get_intro_and_conclusion(title)
    prompt = f"You are an Australian mortgage broker writing blog content for your website. List the 4 most important points for a blog post with the title: '{title}'? Each point should be in a format suitable for a subheadline in a blog post"
    important_points = get_gpt_response(prompt)

    detailed_sections = []
    for point in important_points.split('\n'):
        point = re.sub('^\d+\.\s+', '', point)
        prompt = f"You are an Australian mortgage broker writing a blog post titled '{title}'. Write a detailed section about '{point}' where relevant expand on the point and discuss how the reader should be thinking about the problem. You may not give any financial advice and you may not give advice concerning family law. You must only discuss topics relative to the Australian market."
        detailed_section = get_gpt_response(prompt)
        detailed_sections.append(detailed_section)

    content_blocks = []
    content_blocks.append({"type": "paragraph", "text": intro})

    points = important_points.split('\n')
    for i, point in enumerate(points):
        point = re.sub('^\d+\.\s+', '', point).strip()
        if point and point != '.':  # Check to ensure the point is not empty or just a period
            content_blocks.append({"type": "h2", "text": point})
            content_blocks.append({"type": "paragraph", "text": detailed_sections[i]})

    # Remove a leading period (if present) from the conclusion
    if conclusion.startswith('.'):
        conclusion = conclusion[1:].strip()

    content_blocks.append({"type": "h2", "text": "We understand you and we want to help"})
    content_blocks.append({"type": "paragraph", "text": conclusion})

    return content_blocks
