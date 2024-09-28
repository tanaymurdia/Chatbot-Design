import json
from flask import Flask, jsonify, request
from utils.openai_api import rephrase_question, get_open_ai_resp, content_checking, get_open_ai_non_relevant_resp
from utils.data_retrieval import read_text
import os

app = Flask(__name__)

previous_conv = ""

@app.route('/getapimessage', methods=['GET'])
def get_api_message():
 global previous_conv
 userInput = request.args.get('input') 
 reference_document = read_text('python_service/db/partselect-data.txt')
 previous_conv= previous_conv + "{role: user, content: " + userInput + "} "
 if content_checking(previous_conv,reference_document,userInput):
   rephrase_question_output = rephrase_question(previous_conv,reference_document,userInput)
   openairesp = get_open_ai_resp(previous_conv,rephrase_question_output)
 else:
   openairesp = get_open_ai_non_relevant_resp(userInput)
 message = {
    "role": "assistant",
    "content": openairesp
  }
 previous_conv = previous_conv + "{role: assistant, content: " + openairesp + "} "
 response = jsonify(message)
 response.headers.add("Access-Control-Allow-Origin", "*")
 return response

if __name__ == '__main__':
   app.run(port=5000)