# main_script.py

import requests
import json
import csv
import time
from content_generator import generate_content  # Ensure content_generator.py is in the same directory or set in sys.path

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

def upload_to_sanity(title, content):

    url = "https://vc1wqrrf.api.sanity.io/v1/data/mutate/production"
    token = "sk5ftOXXXN59dEkzWCnMt734HJa0yPKlkM1ZpISU0jM20exqoZlIXlfBe8a6kyQegEaGg51V8s8WoppjOX7G3k5cWTRo9jECoV2dr0D8rRFpdKIvNlKikikuNHbCBC0OL1XHHd1vHzLKcUnfWftGETSD1NhSnlm2CGFwUZkqWSucBWd513GJ"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    payload = {
        "mutations": [
            {
                "create": {
                    "_type": "blogPost",
                    "title": title,
                    "content": content
                }
            }
        ]
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 200:
        print("Post uploaded successfully!")
    else:
        print(f"Failed to upload post. Status Code: {response.status_code}, Response: {response.text}")

def main():
    # Open and read the CSV file
    with open('blog_titles.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        
        # Skip the header row (if it exists)
        next(csv_reader, None)
        
        total_start_time = time.time()  # Start time for all posts
        for row in csv_reader:
            start_time = time.time()  # Start time for one post
            title = row[0]
            print(f"Generating content for: {title}")
            
            generated_content = generate_content(title)
            
            if generated_content:
                portable_text_content = convert_to_portable_text(generated_content)
                upload_to_sanity(title, portable_text_content)
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
