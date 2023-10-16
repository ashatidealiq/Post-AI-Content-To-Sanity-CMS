import openai
import os
import re  # Needed for regular expression operations

# Ensure to replace with your OpenAI API Key
openai.api_key = os.environ['OPENAI_API_KEY']

def generate_excerpt(title):
    prompt = f"Provide a brief teaser or preview for a blog post titled '{title}' about the Australian mortgage market."
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=50,  # Limiting the length to get a concise description
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
            engine='text-davinci-003',
            prompt=prompt,
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.7
        ).choices[0].text.strip()
    
    def get_intro_and_conclusion(title):
        intro_prompt = f"You are an Australian mortgage broker writing blog content for your website. Write an introduction for a blog post with the title: '{title}'"
        conclusion_prompt = f"You are an Australian mortgage broker writing a blog post titled '{title}'. Your firm is called . Write a conclusion for a blog post with the title: '{title}'. Emphasize how your firm would love to help and answer questions and encourage the reader to contact you"
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

    content = f"{intro}\n"
    points = important_points.split('\n')
    for i, point in enumerate(points):
        point = re.sub('^\d+\.\s+', '', point)
        content += f"<h2>{point}</h2>\n{detailed_sections[i]}\n"
    content += f"<h2>Conclusion</h2>\n{conclusion}\n"
    return content
