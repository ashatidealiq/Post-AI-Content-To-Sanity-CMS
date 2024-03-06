# Generate Blog Content For Sanity CMS

Contains py scripts to generate content with OpenAI API and publish to Sanity headless CMS

To run: Set up python env (and/or Node for js utils). main_script.py is control script, calls content_generator.py to generate posts

- Requires environment variables for Sanity project id and token, Openai API token to be sourced from Linux env
- Titles for posts should be in csv file in same directory
- Calls openai to create content around title topic and 4 relevant points. Experiment with prompts in content_generator.py to improve/extend content
- load into Sanity includes required fields for slug, excerpt, userid etc
- load into Sanity does NOT include required feature image
- js scripts are handy to delete old posts you want to replace (batch) or one offs for testing
