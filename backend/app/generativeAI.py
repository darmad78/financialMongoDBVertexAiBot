from vertexai.generative_models import GenerativeModel, SafetySetting
import vertexai
import os

# Configuration for Vertex AI
REGION = os.getenv("REGION")
PROJECT_ID  = os.getenv("PROJECT_ID")

# Generation configuration
generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

# Safety settings
safety_settings = [
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.OFF,
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF,
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.OFF,
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF,
    ),
]

# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=REGION)

# Generative Model
def generate_content(prompt: str) -> str:
    """
    Generates content using the Vertex AI generative model.

    Args:
        prompt (str): The input prompt for the generative model.

    Returns:
        str: The generated response from the model.
    """
    try:
        model = GenerativeModel("gemini-1.5-pro-002")
        responses = model.generate_content(
            [prompt],
            generation_config=generation_config,
            safety_settings=safety_settings,
            stream=True,
        )
        
        final_response = ""
        for response in responses:
            final_response += response.text
            print(response.text, end="")
        
        return final_response
    except Exception as e:
        print(f"Error during content generation: {e}")
        return "An error occurred while generating the response."

# Example usage
if __name__ == "__main__":
    sample_prompt = "Write a short poem about the future of technology."
    result = generate_content(sample_prompt)
    print("\nGenerated Response:\n", result)