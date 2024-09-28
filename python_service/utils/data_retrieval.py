import json
from bs4 import BeautifulSoup
import requests
import os
import re
from openai import OpenAI

link_checked =set()

def concise_text(allText):
    if not len(allText.strip()) == 0:
        global api_key
        client = OpenAI(api_key = api_key)
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            # response_format = {"type":"json_object"},
            messages=[
            {"role": "system", "content": "This is the document {document : " + allText + "}"},
            {"role": "user", "content": "Return a summary of this text including all the information regarding only dishwater or refrigerator parts with specfic details and numbers. If no information regarding regarding only dishwater and refrigerator parts, return \"none\""}
        ]
        )
        return completion.choices[0].message.content
    else:
        return ""

def itemize_text(allText):
    if not len(allText.strip()) == 0:
        global api_key
        client = OpenAI(api_key = api_key)
        completion = client.chat.completions.create(
            model="gpt-4o",
            # response_format = {"type":"json_object"},
            messages=[
            {"role": "system", "content": "This is the document {document : " + allText + "}"},
            {"role": "user", "content": "Return a list of the all items of derived from the document and make them have all the details regarding parts and informations about them. Make a unique set of items but include all the items"}
        ]
        )
        return completion.choices[0].message.content
    else:
        return ""

def fetch_page_content(url):
    """Fetch contents of a page."""
    global link_checked
    if url in link_checked:
        return ""
    else:
        link_checked.add(url)
    try:
        response = requests.get(url,  timeout=5)
        print(response.status_code)
        return response.text
    except requests.exceptions.Timeout:
        print("The request timed out")
        return ""
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e) # Raise an exception for HTTP errors 
        return ""

def extract_text(content):
    """Extract text content from HTML."""
    soup = BeautifulSoup(content, 'html.parser')
    ss = concise_text(soup.get_text(separator='\n', strip=True))
    cleaned_string = re.sub(r'[^a-zA-Z]', '', ss)  # Remove non-alphabet characters
    cleaned_string = cleaned_string.lower()
    if 'none' in cleaned_string:
        return ""
    else:
        return ss

def save_content_to_file(content, filename):
    """Save content to a text file."""
    with open(filename, 'a', encoding="utf-8") as file:
        file.write(content)

def delete_previous_file(filename):
    if os.path.exists(filename):
        os.remove(filename)

def scrape_and_save(base_url, page_url):
    """Scrape the main page and subpages and save their text contents."""
    print(f"Scraping main page: {base_url}")
    main_page_content = fetch_page_content(base_url)
    main_page_text = extract_text(main_page_content)
    extracted_text = main_page_text 
    # save_content_to_file(main_page_text, filename)

    soup = BeautifulSoup(main_page_content, 'html.parser')

    # Example of finding subpages - this depends on the structure of the website
    subpage_urls = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith("/")]

    for i, sub in enumerate(subpage_urls, start=1):
        subpage_url = page_url + sub
        print(f"Scraping subpage {i}: {subpage_url}")
        subpage_content = fetch_page_content(subpage_url)
        subpage_text = extract_text(subpage_content)
        extracted_text = extracted_text + subpage_text
        # save_content_to_file(subpage_text, filename)

    return extracted_text
    
    


def read_text(filename):
    """Extract text content from HTML."""
    with open(filename, 'r', encoding="utf-8") as file:
        return file.read()
    
if __name__ == '__main__':
   filename = 'python_service/db/partselect-data.txt'
   dt = scrape_and_save("https://www.partselect.com/Dishwasher-Parts.htm", "https://www.partselect.com")
   ft = scrape_and_save("https://www.partselect.com/Refrigerator-Parts.htm", "https://www.partselect.com")
   concise_text = itemize_text(dt + ft)
   save_content_to_file(concise_text,filename)
