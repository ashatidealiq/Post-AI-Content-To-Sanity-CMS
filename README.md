# Utils for Sanity CMS content

Scripts to generate openai site content and upload to Sanity.

- Requires environment variables for Sanity project id and token, Openai API token to be sourced from Linux env
- Titles for posts should be in csv file in same directory
- Calls openai to create content around title topic and 4 relevant points. Experiment with prompts in content_generator.py to improve/extend content
- load into Sanity includes required fields for slug, excerpt, userid etc
- load into Sanity does NOT include required feature image
