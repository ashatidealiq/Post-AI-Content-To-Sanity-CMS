import fetch from 'node-fetch';
import fs from 'fs';
import readline from 'readline';

// deletes batch sanity posts

async function deletePostFromSanity(documentId) {
    
    const url = os.environ.get('SANITY_URL') 
    const token = os.environ.get('SANITY_TOKEN')

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

async function processFile() {
    const readInterface = readline.createInterface({
        input: fs.createReadStream('todelete.csv'),
        output: process.stdout,
        terminal: false
    });

    for await (const line of readInterface) {
        const postId = `drafts.${line.trim()}`;
        await deletePostFromSanity(postId);
    }
}

processFile();
