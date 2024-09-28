from openai import OpenAI
import re

api_key ='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'

def content_checking(previous_conv,document,userInput):
    global api_key
    client = OpenAI(api_key=api_key)
    system_prompt = "You are a chatbot on the website of PartSelect(https://www.partselect.com/)." + "The previous conversation is: ["+ previous_conv +"] and this is a reference document {document : " + document + "}."
    user_prompt = "Using the information provided and the user input: \"" + userInput + "\", tell me whether the user is a asking a question and that question are only about Refrigerator and Dishwasher parts. Reply just true or false"
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
           {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    )
    output = completion.choices[0].message.content
    print("content_checking: ",output)
    cleaned_string = re.sub(r'[^a-zA-Z]', '', output)
    cleaned_string = cleaned_string.lower()
    return 'true' in cleaned_string

def rephrase_question(previous_conv,document,userInput):
    global api_key
    instructions = "Make sure that the rephrasing completes the questions, so that it can be used to get the information easily."
    client = OpenAI(api_key=api_key)
    system_prompt = "You are a chatbot on the website of PartSelect(https://www.partselect.com/)." + "The previous conversation is: ["+ previous_conv +"] and this is a reference document {document : " + document + "}."
    user_prompt = "Rephrase the following into wh question, including all the information regarding part's details and description which is accurately extracted from the website to answer it: \"" + userInput + "\"" + instructions
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
           {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    )
    print("rephrase_question: ",completion.choices[0].message.content)
    return completion.choices[0].message.content

def get_open_ai_resp(previous_conv,userInput):

    # Define the prompt you want to send to the GPT model
    global api_key
    client = OpenAI(api_key=api_key)
    prompt = "The previous conversation is: ["+ previous_conv +"]. Answer the following: " + userInput
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
           {"role": "system", "content": "You are a chatbot on the website of PartSelect(https://www.partselect.com/). Answer all the questions that are relevant to partselect based on information on their website(https://www.partselect.com/). If an irrelevant question, answer it saying that it is irrelevant politely. Do no redirect to partselect, try to answer it directly"},
        {"role": "user", "content": prompt}
    ]
    )
    print("get_open_ai_resp: ",completion.choices[0].message.content)
    return completion.choices[0].message.content

def get_open_ai_non_relevant_resp(userInput):

    # Define the prompt you want to send to the GPT model
    global api_key
    client = OpenAI(api_key=api_key)
    prompt = " The user sent this message: \"" + userInput +"\". You are not suppose to answer it as your focus is only about Refrigerator and Dishwasher parts. Send a sympathetic message saying that you cannot do anything about this input"
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
           {"role": "system", "content": "You are a chatbot on the website of PartSelect(https://www.partselect.com/)."},
        {"role": "user", "content": prompt}
    ]
    )
    print("get_open_ai_non_relevant_resp: ",completion.choices[0].message.content)
    return completion.choices[0].message.content
    

