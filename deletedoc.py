import requests
import json
import os

def delete_post_from_sanity(document_id):
    url = "https://vc1wqrrf.api.sanity.io/v1/data/mutate/production"  # Replace 'YOUR_PROJECT_ID' and 'YOUR_DATASET'

    try:
        token = os.environ['SANITY_TOKEN']
    except KeyError:
        print("Error: SANITY_TOKEN environment variable not set.")
        return

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
    post_id = "8gC8hyyysbAly7FAw2woTB"  # replace with the ID of the post/document you want to delete
    delete_post_from_sanity(post_id)
