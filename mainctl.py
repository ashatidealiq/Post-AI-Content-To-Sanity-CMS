import requests
import json

def upload_to_sanity(post):
    # our API endpoint url
    url = "https://vc1wqrrf.api.sanity.io/v1/data/mutate/production"
    
    # API Token for Sanity
    projectid = "vc1wqrrf"
    dataset = "production"
    token = "sk5ftOXXXN59dEkzWCnMt734HJa0yPKlkM1ZpISU0jM20exqoZlIXlfBe8a6kyQegEaGg51V8s8WoppjOX7G3k5cWTRo9jECoV2dr0D8rRFpdKIvNlKikikuNHbCBC0OL1XHHd1vHzLKcUnfWftGETSD1NhSnlm2CGFwUZkqWSucBWd513GJ"
    
    # Headers for the API request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    # Mutation to create a new document in Sanity
    payload = {
        "mutations": [
            {
                "create": {
                    "_type": "blogPost",
                    "title": post["title"],
                    "content": post["content"]
                }
            }
        ]
    }
    
    # Making the API request
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    # Checking the response
    if response.status_code == 200:
        print("Post uploaded successfully!")
    else:
        print(f"Failed to upload post. Status Code: {response.status_code}, Response: {response.text}")

# Example usage:
# Assume generate_post is a function from your existing script that returns the post as JSON.
# post = generate_post()
# upload_to_sanity(post)
