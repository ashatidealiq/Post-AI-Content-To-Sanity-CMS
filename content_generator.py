# content_generator.py

import openai

# Ensure to replace with your OpenAI API Key
openai.api_key = 'YOUR_OPENAI_API_KEY'

def generate_content(title, max_tokens=150, temperature=0.7):
    
    def get_gpt_response(prompt):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.7
    )

    def get_intro_and_conclusion(title):
    intro_prompt = f"You are an Australian mortgage broker writing blog content for your website. Write an introduction for a blog post with the title: '{title}'"
    conclusion_prompt = (
        f"You are an Australian mortgage broker writing a blog post titled '{title}'. Your firm is called . "
        f"Write a conclusion for a blog post with the title: '{title}'. Emphasize how your firm would love to help and answer questions and encourage the reader to contact you"
    )

    intro, conclusion = get_intro_and_conclusion(title)

    # Prompt for important points
    prompt = (
                f"You are an Australian mortgage broker writing blog content for your website. List the 4 most important points for a blog post with the title: '{title}'?"
                f"Each point should be in a format suitable for a subheadline in a blog post"
            )
    
    important_points = get_gpt_response(prompt)

    detailed_sections = []
        for point in important_points.split('\n'):
            # Remove potential numbering from the point
            point = re.sub('^\d+\.\s+', '', point)

            # Prompt for detailed section on each point
            prompt = (
                    f"You are an Australian mortgage broker writing a blog post titled '{title}'. Write a detailed section about '{point}'." 
                    f"Where relevant expand on the point and discuss how the reader should be thinking about the problem."
                    f"You may not give any financial advice and you may not give advice concerning family law. You must only discuss topics relative to the Australian market."
                    )
            detailed_section = get_gpt_response(prompt)
            detailed_sections.append(detailed_section)

            # Create the blog post with headers for each important point
            content = f"{intro}\n"
            points = important_points.split('\n')
            for i, point in enumerate(points):
                # Remove potential numbering from the point
                point = re.sub('^\d+\.\s+', '', point)

                content += f"<h2>{point}</h2>\n{detailed_sections[i]}\n"
            
            content += f"<h2>Conclusion</h2>\n{conclusion}\n"



    intro = get_gpt_response(intro_prompt)
    conclusion = get_gpt_response(conclusion_prompt)
    return intro, conclusion


        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error in content generation: {str(e)}")
        return None
