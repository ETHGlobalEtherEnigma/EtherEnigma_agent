from flask import Flask, request, jsonify
from swarm import Swarm
from flask_cors import CORS, cross_origin
from agents import based_agent  # If you're using the based_agent
import re

app = Flask(__name__)
CORS(app)
# Set up the swarm client with your OpenAI API key
client = Swarm()

def process_and_print_streaming_response(response):
    content = ""
    last_sender = ""

    for chunk in response:
        if "sender" in chunk:
            last_sender = chunk["sender"]

        if "content" in chunk and chunk["content"] is not None:
            content += chunk["content"]  # Just accumulate the content

        if "tool_calls" in chunk and chunk["tool_calls"] is not None:
            # You can choose to handle tool_calls here, if needed
            pass

        if "delim" in chunk and chunk["delim"] == "end" and content:
            content = ""  # Reset content

        if "response" in chunk:
            return chunk["response"]

    # If no response found, you might want to handle this case
    return None

# Handle preflight requests (OPTIONS)
@app.route('/api/gpt', methods=['OPTIONS'])
@cross_origin(origin='http://localhost:3000', headers=['Content-Type'])
def preflight():
    return jsonify({})

@app.route('/api/gpt', methods=['POST'])
@cross_origin(origin='http://localhost:3000', headers=['Content-Type'])
def gpt_response():
    prompt = request.json.get('prompt')
    if not prompt:
        return jsonify({'error': 'Missing prompt'}), 400
    # Use Swarm to call OpenAI's GPT API 
    messages = [{
        "role": "user",
        "content": prompt
    }]
    response = client.run(agent=based_agent, messages=messages, stream=True)  
    # Process the entire response from the generator
    response_obj = process_and_print_streaming_response(response) 
    # Clean the response to remove any HTML tags
    cleaned_response = re.sub(r'<[^>]+>', '', response_obj.messages[-1]["content"])
    return jsonify({'response': cleaned_response}) 

    # Print the response after returning JSON
    if response_obj:
        print(f"\033[94m{response_obj.messages[-1]['sender']}\033[0m:", end=" ")
        print(cleaned_response)

@app.route('/api/data', methods=['GET', 'OPTIONS'])
def get_data():
    return jsonify({"data": "This is your data."})

if __name__ == "__main__":
    app.run(debug=True)