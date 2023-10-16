# main_script.py

import requests
import json
import os
import csv
import time
from content_generator import generate_content, generate_excerpt, generate_slug  # Ensure content_generator.py is in the same directory or set in sys.path

def convert_to_portable_text(plain_text):
   
    # Returns dict as converted portable text
    
    return {
        "_type": "block",
        "children": [
            {
                "_type": "span",
                "text": plain_text
            }
        ]
    }

def upload_to_sanity(title, slug, content, excerpt):

    url = "https://vc1wqrrf.api.sanity.io/v1/data/mutate/production"
    token = os.environ['SANITY_TOKEN']
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    payload = {
        "mutations": [
            {
                "create": {
                    "_type": "Post",
                    "title": title,
                    "slug": slug,
                    "content": content,
                    "excerpt": excerpt,
                    "author": "Ello"
                }
            }
        ]
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
def main():
    # Open and read the CSV file
    with open('blog_titles.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        
        # Skip the header row (if it exists)
        # next(csv_reader, None)
        
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
