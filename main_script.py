import requests
import json
import uuid
import os
import csv
import time
from datetime import datetime
from content_generator import generate_content, generate_excerpt, generate_slug  

def convert_to_portable_text(content_blocks):
    portable_text = []
    for block in content_blocks:
        if block['type'] == 'h2':
            # Create a block with h2 style
            portable_text.append({
                "_type": "block",
                "_key": str(uuid.uuid4()),
                "children": [{
                    "_type": "span",
                    "_key": str(uuid.uuid4()),
                    "text": block['text']
                }],
                "style": "h2",
                "markDefs": []
            })
        elif block['type'] == 'paragraph':
            # Create a regular block
            portable_text.append({
                "_type": "block",
                "_key": str(uuid.uuid4()),
                "children": [{
                    "_type": "span",
                    "_key": str(uuid.uuid4()),
                    "text": block['text']
                }],
                "markDefs": []
            })
    return portable_text

def upload_to_sanity(title, slug, content, excerpt):
    url = "https://vc1wqrrf.api.sanity.io/v1/data/mutate/production"
    author = "b98df841-6f6d-49d9-82f9-654ed8339e5f" # set author to "Ello"
    current_date = datetime.now().date().isoformat()

    token = os.environ.get('SANITY_TOKEN')
    if not token:
        print("Error: SANITY_TOKEN environment variable not set.")
        return

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    # Ensure content is an array
    if not isinstance(content, list):
        content = [content]

    print(content)

    payload = {
        "mutations": [
            {
                "create": {
                    "_type": "post",
                    "title": title,
                    "slug": {
                        "_type": "slug",
                        "current": slug  
                    },
                    "content": content,  
                    "excerpt": excerpt,
                    "date": current_date,
                    "author": {
                        "_type": "reference",
                        "_ref": author  
                    }
                }
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        if response.status_code != 200:
            print(f"Error posting to Sanity. Status Code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    return response

def main():
    with open('blog_titles.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        total_start_time = time.time()  # Start time for all posts
        for row in csv_reader:
            start_time = time.time()  # Start time for one post
            title = row[0]
            print(f"Generating content for: {title}")

            generated_content = generate_content(title)
            excerpt = generate_excerpt(title)
            slug = generate_slug(title)

            if generated_content:
                portable_text_content = convert_to_portable_text(generated_content)
                upload_to_sanity(title, slug, portable_text_content, excerpt)
                end_time = time.time()
                elapsed_time = (end_time - start_time) / 60
                print(f"Successfully published '{title}' to Sanity site in '{elapsed_time}' minutes")
            else:
                print(f"Failed to generate content for title: {title}")

        # Calculate and print the total elapsed time
        total_end_time = time.time()
        total_elapsed_time = total_end_time - total_start_time
        print(f"Total elapsed time for all posts: '{total_elapsed_time}' seconds")

if __name__ == "__main__":
    main()
