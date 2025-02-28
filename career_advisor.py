import os
import json
from openai import OpenAI
from openai._exceptions import APIError

def validate_api_key():
    """Validate that OpenAI API key is properly configured"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OpenAI API key not found. Please ensure you have set the OPENAI_API_KEY environment variable."
        )
    return True

# Initialize OpenAI client with environment variable
client = OpenAI()  # This will automatically use OPENAI_API_KEY from environment

def get_career_recommendations(skills, experience_years, education_level, interests):
    """
    Get career recommendations based on user input using OpenAI API
    """
    try:
        # Validate API key before making the request
        validate_api_key()

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

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": json.dumps(prompt)}
            ],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)
    except APIError as e:
        if "insufficient_quota" in str(e):
            raise Exception(
                "The OpenAI API key has exceeded its quota or has billing issues. "
                "Please check your OpenAI account billing status and limits."
            )
        raise Exception(f"OpenAI API error: {str(e)}")
    except Exception as e:
        raise Exception(f"Failed to get career recommendations: {str(e)}")