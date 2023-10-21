import fetch from 'node-fetch';

// deletes one off docs in sanity

async function deletePostFromSanity(documentId) {
    const url = "https://vc1wqrrf.api.sanity.io/v1/data/mutate/production";
    const token = 'sk5ftOXXXN59dEkzWCnMt734HJa0yPKlkM1ZpISU0jM20exqoZlIXlfBe8a6kyQegEaGg51V8s8WoppjOX7G3k5cWTRo9jECoV2dr0D8rRFpdKIvNlKikikuNHbCBC0OL1XHHd1vHzLKcUnfWftGETSD1NhSnlm2CGFwUZkqWSucBWd513GJ';

    const headers = {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
    };

    const payload = {
        mutations: [
            {
                delete: {
                    id: documentId
                }
            }
        ]
    };

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: headers,
            body: JSON.stringify(payload)
        });

        const responseBody = await response.text();
        console.log(response.text);
        console.log(`Status Code: ${response.status}`);
        console.log(`Response: ${responseBody}`);

        if (response.status !== 200) {
            console.log(`Error deleting post in Sanity. Status Code: ${response.status}`);
        } else {
            console.log(`Successfully deleted post with ID: ${documentId}`);
        }

    } catch (error) {
        console.log(`An error occurred: ${error.toString()}`);
    }
}

const postId = "3ER6NULiBAHBqYxtuLttxn";  // wtf is going on now
deletePostFromSanity(postId);