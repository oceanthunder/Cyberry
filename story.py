import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"  #ollama runs on this port

def generate_story(prompt):
    payload = {
        "model": "deepseek-r1:1.5b",
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        response_json = response.json()
        
        if "response" not in response_json:
            raise ValueError("The key 'response' is missing in the JSON response.")
        
        story_response = response_json["response"]
        
        try:
            story_data = json.loads(story_response)
        except json.JSONDecodeError:
            raise ValueError("The response is not a valid JSON string.")
        
        required_keys = {"title", "story", "moral"}
        if not required_keys.issubset(story_data.keys()):
            raise ValueError(f"The JSON response is missing one or more required keys: {required_keys}")
        
        return story_data["title"], story_data["story"], story_data["moral"]
    
    except requests.exceptions.RequestException as e:
        print(f"Network error occurred: {e}")
        return None, None, None
    except ValueError as e:
        print(f"Error parsing response: {e}")
        return None, None, None

user_prompt = """
Write a very short story (around 50 words) about a wide array of cybersecurity topics. The story should be imaginative, engaging, and include interesting characters.

The output must be a valid JSON string with the following keys: "title", "story", and "moral". Ensure the JSON structure is exact and does not include any additional text or explanations outside the JSON.

Example of the expected JSON format:
{
    "title": "The Password Puzzle",
    "moral": "Don't use easy-to-guess passwords, even if they seem tricky.",
    "story": "Ethan made his password ‘password123’ but thought adding ‘123’ made it strong. A hacker guessed it in seconds! His dad taught him to use a mix of letters, numbers, and symbols. Ethan learned that weak passwords are easy to crack."
}

Now, write your story in the exact same JSON format. Make it impactful and relevant to real-life cybersecurity issues, ensuring the story and its moral are completely different from the example and cover a unique cybersecurity topic. The topic can be less, moderately or highly discussed.
"""

#example 
title, story, moral = generate_story(user_prompt)

if title and story and moral:
    print("Title:", title)
    print("Story:", story)
    print("Moral:", moral)
else:
    print("Failed to generate a valid story.")

