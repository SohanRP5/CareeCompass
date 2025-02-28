import os
import json
from openai import OpenAI

# Initialize OpenAI client with environment variable
client = OpenAI()  # This will automatically use OPENAI_API_KEY from environment

def get_career_recommendations(skills, experience_years, education_level, interests):
    """
    Get career recommendations based on user input using OpenAI API
    """
    prompt = {
        "skills": skills,
        "experience_years": experience_years,
        "education_level": education_level,
        "interests": interests
    }

    system_message = """
    You are a career guidance expert. Analyze the user's skills, experience, and interests to recommend suitable career paths.
    Provide detailed recommendations in JSON format with the following structure:
    {
        "careers": [
            {
                "title": "Career Title",
                "match_score": 0-100,
                "description": "Detailed description",
                "requirements": "Key requirements bullet points",
                "growth_potential": "Growth potential description",
                "next_steps": "Recommended next steps"
            }
        ],
        "development_plan": "Detailed development plan"
    }
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": json.dumps(prompt)}
            ],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)
    except Exception as e:
        raise Exception(f"Failed to get career recommendations: {str(e)}")