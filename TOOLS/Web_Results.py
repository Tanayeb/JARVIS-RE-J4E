# import requests
# from bs4 import BeautifulSoup


# while True:
#     find = input("Enter what you want to search: ")
#     url = f"https://www.google.com/search?q={find}"

#     req = requests.get(url)
#     soup = BeautifulSoup(req.text, "html.parser")

#     mysearch = soup.find("div", {"class": "BNeawe"}).text

#     print(mysearch)




import requests
from googlesearch import search
from bs4 import BeautifulSoup

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer


def get_query_result(prompt):
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

# Example usage
if __name__ == "__main__":
    query = input("Enter your query: ")
    print(get_query_result(query))
