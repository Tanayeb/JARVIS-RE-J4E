# from huggingface_hub import InferenceClient
# import random
# from dotenv import load_dotenv
# from os import environ
# from json import load, dump
# load_dotenv()

# import re
# from typing import List
# from duckduckgo_search import DDGS
# import concurrent.futures

# DefaultMessage = [{'role': 'user', 'content': f"Hello {environ['AssistantName']}, How are you?"}, {'role': 'assistant', 'content': f"Welcome Back {environ['NickName']}, I am doing well. How may I assist you?"}]

# try:
#     with open('ChatLog.json', 'r') as f:
#         messages = load(f)
# except:
#     with open('ChatLog.json', 'w') as f:
#         dump(DefaultMessage, f)

# import os
# from typing import List, Tuple, Union
# from dotenv import load_dotenv; load_dotenv()

# from googlesearch import search as google_search
# from duckduckgo_search import DDGS

# import requests
# import json
# import concurrent.futures

# def fetch_search_results(query: str, max_results: int = 5, verbose: bool = False, search_engine: str = 'duckduckgo', format_output: bool = False) -> Union[Tuple[List[str], List[str], List[str]], str]:
#     sentences = re.split(r'(?<=[.!?]) +', query)

#     urls: List[str] = []
#     titles: List[str] = []
#     descriptions: List[str] = []

#     if verbose:
#         print("Query Breakdown:")
#         for i, sentence in enumerate(sentences):
#             print(f"  Sentence {i + 1}: {sentence}")

#     def fetch_results_for_sentence(sentence: str):
#         sentence_urls = []
#         sentence_titles = []
#         sentence_descriptions = []

#         if verbose:
#             print(f"Fetching results for sentence: {sentence} using {search_engine}")

#         if search_engine.lower() == 'google':
#             results = google_search(sentence, num_results=max_results, advanced=True)
#             for j, link in enumerate(results):
#                 if verbose:
#                     print(f"    Result {j + 1}:")
#                     print(f"      URL: {link.url}")
#                     print(f"      Title: {link.title}")
#                     print(f"      Description: {link.description}")
#                 sentence_urls.append(link.url)
#                 sentence_titles.append(link.title)
#                 sentence_descriptions.append(link.description)

#         elif search_engine.lower() == 'duckduckgo':
#             results = DDGS().text(sentence, max_results=max_results)
#             for j, result in enumerate(results):
#                 if verbose:
#                     print(f"    Result {j + 1}:")
#                     print(f"      URL: {result['href']}")
#                     print(f"      Title: {result['title']}")
#                     print(f"      Description: {result['body']}")
#                 sentence_urls.append(result['href'])
#                 sentence_titles.append(result['title'])
#                 sentence_descriptions.append(result['body'])

#         elif search_engine.lower() == 'serper':
#             url = "https://google.serper.dev/search"
#             payload = json.dumps({"q": sentence})
#             headers = {
#                 'X-API-KEY': os.getenv('SERPER_API_KEY'),
#                 'Content-Type': 'application/json'
#             }
#             response = requests.post(url, headers=headers, data=payload)
#             if response.status_code == 200:
#                 data = response.json()
#                 for j, result in enumerate(data.get('organic', [])):
#                     if j >= max_results:
#                         break
#                     if verbose:
#                         print(f"    Result {j + 1}:")
#                         print(f"      URL: {result['link']}")
#                         print(f"      Title: {result['title']}")
#                         print(f"      Description: {result['snippet']}")
#                     sentence_urls.append(result['link'])
#                     sentence_titles.append(result['title'])
#                     sentence_descriptions.append(result['snippet'])
#             else:
#                 print("Error fetching results from Serper API")
#         else:
#             raise ValueError("Invalid search engine specified. Please choose either 'google', 'duckduckgo', or 'serper'.")

#         return sentence_urls, sentence_titles, sentence_descriptions

#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         futures = [executor.submit(fetch_results_for_sentence, sentence) for sentence in sentences]

#         for future in concurrent.futures.as_completed(futures):
#             sentence_urls, sentence_titles, sentence_descriptions = future.result()
#             urls.extend(sentence_urls)
#             titles.extend(sentence_titles)
#             descriptions.extend(sentence_descriptions)

#     if format_output:
#         return format_response(query, descriptions, verbose=verbose)
#     else:
#         return urls, titles, descriptions

# def format_response(query: str, descriptions: List[str], verbose: bool = False) -> str:
#     formatted_response: str = """
# **Instructions**: 

# 1. Gather Information from Provided Sources
#     - Carefully read through all the provided sources.
#     - Extract relevant information that directly answers or contributes to answering the query.
#     - Ensure the information is accurate and comes from a reliable source.

# 2. Synthesize and Integrate Information
#     - Combine information from multiple sources if applicable.
#     - Ensure that the synthesized response is coherent and logically consistent.
#     - Avoid redundancy and ensure the response flows naturally.

# 3. Use Knowledge Cutoff
#     - If the provided sources do not contain valuable or relevant information, then rely on your pre-existing knowledge up to the cutoff date.
#     - Ensure that any information provided from your knowledge is accurate as of the last update in October 2023.

# 4. Acknowledge Knowledge Limits
#     - If the query pertains to information or events beyond your knowledge cutoff date, clearly state this to the user.
#     - Avoid providing speculative or unverified information.

# 5. Maintain Clarity and Precision
#     - Ensure that the response is clear, precise, and directly answers the query.
#     - Avoid unnecessary jargon and ensure the language is accessible to the user.

# **Sources**:
# """
#     for i, description in enumerate(descriptions):
#         formatted_response += f"- {description}\n"

#     formatted_response += f"\n\n**Query**: {query}"

#     if verbose:
#         print(formatted_response)

#     return formatted_response

# API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
# headers = {"Authorization": "Bearer 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"}

# def generate_response(prompt, temperature=0.9, max_new_tokens=512, top_p=0.95, repetition_penalty=1.0):
#     temperature = float(temperature)
#     if temperature < 1e-2:
#         temperature = 1e-2

#     top_p = float(top_p)

#     generate_kwargs = dict(
#         temperature=temperature,
#         max_new_tokens=max_new_tokens,
#         top_p=top_p,
#         repetition_penalty=repetition_penalty,
#         do_sample=True,
#         seed=random.randint(0, 10**7),
#     )

#     System = f"Hello, I am {environ['NickName']}, You are a very accurate and advanced AI chatbot named {environ['AssistantName']} with real-time up-to-date internet information.\n*** Answer the questions professionally based on the provided data. ***"

#     SystemChat = [{'role': 'system', 'content': System}]

#     # Ensure the prompt is clean and properly formatted
#     formatted_prompt = f"{SystemChat}\nUser: {prompt}\nAssistant:"

#     client = InferenceClient(API_URL, headers=headers)
#     response = client.text_generation(formatted_prompt, **generate_kwargs)

#     # Return just the assistant's response, removing the role identifiers
#     return response.split('Assistant: ')[-1].strip()

# def AnswerModifier(Answer):
#     lines = Answer.split('\n')
#     non_empty_lines = [line for line in lines if line.strip()]
#     modified_answer = '\n'.join(non_empty_lines)
#     return modified_answer

# try:
#     with open('ChatLog.json', 'r') as f:
#         messages = load(f)
# except:
#     with open('ChatLog.json', 'w') as f:
#         dump(DefaultMessage, f)

# def RealTimeChatBotAI(query):
#     # Fetch search results and generate a response
#     formatted_output = fetch_search_results(query, search_engine='serper')
#     response = generate_response(formatted_output)

#     # Load existing chat log
#     try:
#         with open('ChatLog.json', 'r') as f:
#             messages = load(f)
#     except FileNotFoundError:
#         messages = DefaultMessage

#     # Append the new user query and assistant response to the chat log
#     messages.append({'role': 'user', 'content': query})
#     messages.append({'role': 'assistant', 'content': response})

#     # Save updated chat log
#     with open('ChatLog.json', 'w') as f:
#         json.dump(messages, f, indent=4)

#     return AnswerModifier(response)

# if __name__ == "__main__":
#     while True:
#         query = input("Enter: ")
#         print(f"\nJarvis: {RealTimeChatBotAI(query)}")

from bs4 import BeautifulSoup
import requests
from groq import Groq
from googlesearch import search
from json import load, dump
from os import environ
from dotenv import load_dotenv
global SystemChat
global messages
load_dotenv()
client = Groq(api_key=environ['GroqAPI'])
DefaultMessage = [{'role': 'user', 'content': f"Hello {environ['AssistantName']}, How are you?"}, {'role': 'assistant', 'content': f"Welcome Back {environ['NickName']}, I am doing well. How may i assist you?"}]
try:
    with open('ChatLog.json', 'r') as f:
        messages = load(f)
except:
    with open('ChatLog.json', 'w') as f:
        dump(DefaultMessage, f)

def GoogleSearch(prompt):
        # Search for the query on Google and fetch the first result
    search_results = list(search(prompt, num_results=1))
    
    if not search_results:
        return "No search results found."
    
    url = search_results[0]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    
    try:
        # Set a timeout and headers for the request
        response = requests.get(url, timeout=10, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses
    except requests.exceptions.Timeout:
        return "The request timed out. Please try again later."
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract text from the webpage
    result = soup.find('p')
    
    if result:
        return result.get_text()
    else:
        return "Couldn't fetch the relevant information. Please try again."
System = f"Hello, I am {environ['NickName']}, You are a very accurate and advance AI chatbot named {environ['AssistantName']} which have realtime up-to-date information of internet.\n*** Just answer the question from the provided data in a professional way. ***"

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer
SystemChat = [{'role': 'system', 'content': System}, {'role': 'user', 'content': 'Do you have realtime data ?'}, {'role': 'assistant', 'content': 'Yes, I have all real time data.'}]

def RealTimeChatBotAI(prompt):
    global messages
    with open('ChatLog.json', 'r') as f:
        messages = load(f)
    SystemChat.append({'role': 'system', 'content': GoogleSearch(prompt)})
    messages.append({'role': 'user', 'content': prompt})
    # completion = client.chat.completions.create(model='mixtral-8x7b-32768', messages=SystemChat + messages, temperature=0.7, max_tokens=2048, top_p=1, stream=True, stop=None)
    Answer = GoogleSearch(prompt)
    # for chunk in completion:
    #     if chunk.choices[0].delta.content:
    #         Answer += chunk.choices[0].delta.content
    # Answer = Answer.strip().replace('</s>', '')
    # Answer = Answer[0:Answer.find('[')]
    messages.append({'role': 'assistant', 'content': Answer})
    with open('ChatLog.json', 'w') as f:
        dump(messages, f, indent=4)
    SystemChat.pop()
    return AnswerModifier(Answer)
if __name__ == '__main__':
    while True:
        prompt = input('Enter your query: ')
        print(RealTimeChatBotAI(prompt))