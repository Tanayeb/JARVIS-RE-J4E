import pathlib
import PIL.Image
import google.generativeai as genai
import google.ai.generativelanguage as glm
from json import load, dump, JSONDecodeError
from os import environ

DefaultMessage = [{'role': 'user', 'content': "Hello JARVIS, How are you?"}, {'role': 'assistant', 'content': "Welcome Back Tanayeb, I am doing well. How may I assist you?"}]

def AnswerModifier(Answer):
    if Answer is None:
        return None
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

def ChatGptAI(user_message: str, image_path: str = r"capture.png", system_prompt: str = "Be a helpful assistant"):
    try:
        with open('ChatLog.json', 'r') as f:
            try:
                messages = load(f)
            except JSONDecodeError:
                print("ChatLog.json is corrupted or empty. Resetting to default.")
                messages = DefaultMessage
    except FileNotFoundError:
        print("ChatLog.json not found. Creating a new one.")
        with open('ChatLog.json', 'w') as f:
            dump(DefaultMessage, f)
        messages = DefaultMessage

    try:
        GOOGLE_API_KEY = "AIzaSyBmjXfLShhfrp-3L_2Nn2OoV9-PykaGu0M"
        genai.configure(api_key=GOOGLE_API_KEY)

        # Load the image
        img = PIL.Image.open(image_path)

        # Convert image to bytes
        image_bytes = pathlib.Path(image_path).read_bytes()

        # Initialize Generative Model
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Generate content using the image and system prompt
        response = model.generate_content(
            glm.Content(
                parts=[
                    glm.Part(text=user_message),
                    glm.Part(
                        inline_data=glm.Blob(
                            mime_type="image/png",
                            data=image_bytes,
                        )
                    ),
                ],
            ),
            stream=True
        )

        # Resolve the response
        response.resolve()

        # Extract text from the resolved response
        Answer = response.text

        # Update chat log with the response
        messages.append({'role': 'assistant', 'content': Answer})
        with open('ChatLog.json', 'w') as f:
            dump(messages, f, indent=4)

        return AnswerModifier(Answer)

    except Exception as e:
        print(f"An error occurred: {e}")
        # Reset the ChatLog file and try again
        with open('ChatLog.json', 'w') as f:
            dump(DefaultMessage, f)
        return ChatGptAI(user_message)

if __name__ == "__main__":
    prompt = input("Enter your query: ")
    print(ChatGptAI(prompt))
