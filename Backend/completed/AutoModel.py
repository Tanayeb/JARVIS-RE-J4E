o
            �                   @   �   d dl Z d dlmZ d dlmZ d dlmZmZ d dlm	Z	 d dl
mZ e	�  e jed d�Zg d	�Zeddefdd��ZedkrK	 eeed��� qBdS )�    N��TimeIt��print��load�dump��load_dotenv��environ�	CohereAPI��api_key��general�realtime�open�close�playzgenerate image�system�contentzgoogle searchzyoutube search�clickzdouble click�test�promptc           	      C   �  t dd��}t|�}W d   � n1 sw   Y  |�d| � d�� t dd��}t||dd� W d   � n1 s9w   Y  tjd| d	d
dd�ddd�d
dd�ddd�d
dd�ddd�d
dd�ddd�d
dd�ddd�g
dg dd�}d}|D ]}|jdkr�||j7 }t|jdd� qvt�  |�	dd�}|�
d�}dd� |D �}g }|D ]}tD ]}|�|�r�|�|� q�q�t|�dkr�|�d� |}|S )N�ChatLog.json�r�user��roler   �w�   ��indent�command-r-plus�ffffff�?�User�how are you�r!   �message�Chatbotr   �do you like pizza�open chrome�open chrome and firefox�open chrome, open firefox�chat with me�OFF�%  You are a very accurate Decision-Making-Model, which decides what kind of a query is given to you.
    You will decide weather a query is a 'general' query or 'realtime' query or is it asking to perform any task or automation like 'open facebook, instagram', 'can you write a application and open it in notepad'
    *** Do not answer any query, just decide what kind of query is given to you. ***
    -> Respond with 'general' if a query can be answered by a llm model ( conversational ai chatbot ) and doesn't require any up to date information like 'who was akbar?', 'how can i study more effectively?', 'can you help me with this math problem?', 'Thanks, i really liked it.', 'what is python programming language?', etc. Respond with 'general' if a query doesn't have a proper noun or is incomplete like 'who is he?', 'what's his networth?', 'tell me more about him.', and so on even if it require up-to-date information to answer. Respond with 'general' if the query is asking about time, day, date, month, year, etc.
    -> Respond with 'realtime' if a query can not be answered by a llm model ( cause they don't have realtime data ) and requires up to date information like 'who is indian prime minister', 'tell me about facebook's recent update.', 'tell me news about coronavirus', etc and if the query is asking about any individual or thing like 'who is akshay kumar', 'what is today's headline', etc.
    -> Respond with 'open ( application name or website name )' if a query is asking to open any application like 'open facebook', 'open telegram', etc. but if the query is asking to open multiple applications, respond with 'open 1st application name, open 2nd application name' and so on.
    -> Respond with 'close ( application name )' if a query is asking to close any application like 'close notepad', 'close facebook', etc. but if the query is asking to close multiple applications or websites, respond with 'close 1st application name, close 2nd application name' and so on.
    -> Respond with 'play ( song name )' if a query is asking to play any song like 'play afsanay by ys', 'play let her go', etc. but if the query is asking to play multiple songs, respond with 'play 1st song name, play 2nd song name' and so on.
    -> Respond with 'generate image ( image prompt )' if a query is requesting to generate a image with given prompt like 'generate image of a lion', 'generate image of a cat', etc. but if the query is asking to generate multiple images, respond with 'generate image 1st image prompt, generate image 2nd image prompt' and so on.
    -> Respond with 'system ( task name )' if a query is asking to mute, unmute, minimize, maximize, volmume up, volume down, minimize all windows, maximize all windows, shutdown, restart, etc. but if the query is asking to do multiple tasks, respond with 'system 1st task, system 2nd task', etc.
    -> Respond with 'content ( topic )' if a query is asking to write any type of content like application, codes, emails or anything else about a sepecific topic but if the query is asking to write multiple types of content, respond with 'content 1st topic , content 2nd topic' and so on.
    -> Respond with 'google search ( topic )' if a query is asking to search a specific topic on google but if the query is asking to search multiple topics on google, respond with 'google search 1st topic, google search 2nd topic' and so on.
    -> Respond with 'youtube search ( topic )' if a query is asking to search a specific topic on youtube but if the query is asking to search multiple topics on youtube, respond with 'youtube search 1st topic, youtube search 2nd topic' and so on.
    -> Respond with 'click ( text )' if a query is asking to click any text on the screen like 'click on facebook', 'click on instagram', etc. but if the query is asking to click multiple texts, respond with 'click 1st_text, click 2nd_text' and so on.
    -> Respond with 'double click ( text )' if a query is asking to click any text on the screen like 'double click on facebook', 'double click on instagram', etc. but if the query is asking to click multiple texts, respond with 'double click 1st_text, double click 2nd_text' and so on.
    -> Respond with 'open webcam' if a query is asking to open webcam.
    -> Respond with 'close webcam' if a query is asking to close webcam.
    *** if the query is asking to perform multiple tasks like 'open facebook, telegram and close whatsapp', respond with 'open facebook, open telegram, close whatsapp' ***
    *** Respond with 'general' if you can't decide the kind of query or if a query is asking to perform a task which is not mentioned above. ***��modelr+   �temperature�chat_history�prompt_truncation�
connectors�preamble� �text-generation��end�
�,c                 S   �   g | ]}|� � �qS ) ��strip��.0�i� rG   �Backend\AutoModel.py�
<listcomp>J   �    �Model.<locals>.<listcomp>r   �r   r   �appendr	   �co�chat_stream�
event_type�textr   �replace�split�funcs�
startswith�len�	r   �f�messages�stream�response�event�temp�task�funcrG   rG   rH   �Model   �J   
��R�

�


��
r`   �__main__T�>>> �r   ��cohereZ
Nara.Extrar   �richr   �jsonr   r	   �dotenvr   �osr   �ClientrN   rT   �strr`   �__name__�inputrG   rG   rG   rH   �<module>   �$    �8��