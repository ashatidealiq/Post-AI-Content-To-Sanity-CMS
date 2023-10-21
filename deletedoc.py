import requests
import json
import os

# how do you delete docs in Sanity

def delete_post_from_sanity(document_id):

    url = os.environ.get('SANITY_URL')
    token = os.environ['SANITY_TOKEN']
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    # Payload for deleting the post
    payload = {
        "mutations": [
            {
                "delete": {
                    "id": document_id
                }
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code != 200:
            print(f"Error deleting post in Sanity. Status Code: {response.status_code}")
        else:
            print(f"Successfully deleted post with ID: {document_id}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    return response

# Example usage
if __name__ == "__main__":
    post_id = "3ER6NULiBAHBqYxtuLssFj"  
    delete_post_from_sanity(post_id)
