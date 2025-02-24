import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

def generate_story():
    user_prompt = """
    Write a very short story (around 250 words, bit longer than the example) about a wide array of cybersecurity topics, use phishing stories sparringly. The story should be imaginative, engaging, and include interesting characters.

    The output must be a valid JSON string with the following keys: "title", "story", and "moral". Ensure the JSON structure is exact and does not include any additional text or explanations outside the JSON.

    Example of the expected JSON format:
    {
        "title": "The Password Puzzle",
        "moral": "Don't use easy-to-guess passwords, even if they seem tricky.",
        "story": "Ethan made his password ‘password123’ but thought adding ‘123’ made it strong. A hacker guessed it in seconds! His dad taught him to use a mix of letters, numbers, and symbols. Ethan learned that weak passwords are easy to crack."
    }

    Now, write your story in the exact same JSON format. Make it impactful and relevant to real-life cybersecurity issues, ensuring the story and its moral are completely different from the example and cover a unique cybersecurity topic. The topic can be less, moderately or highly discussed. Be creative and don't spit out the same things always!!
    """

    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": user_prompt}
                ]
            }
        ]
    }

    try:
        response = requests.post(GEMINI_URL, headers=headers, json=payload)
        response.raise_for_status()
        response_json = response.json()
        
        if "candidates" not in response_json:
            raise ValueError("Invalid API response: Missing 'candidates' key.")

        generated_text = response_json["candidates"][0]["content"]["parts"][0]["text"]

        try:
            story_data = json.loads(generated_text)
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
