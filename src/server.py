from flask import Flask, request, jsonify
import google.generativeai as genai
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

def generate_content(job_description):
   GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
   genai.configure(api_key=GEMINI_API_KEY)
   model = genai.GenerativeModel('gemini-pro')
   response = model.generate_content("""I have the following Job Description:
                {job_description}
                Based on the above job description, extract technical keywords that best describe the 
                skillsets and technologies required for the above job. Pay special attention to programming 
                languages, tools, and technologies mentioned.
                Use the following format separated by commas:
                <keywords>
                """)
   return response.text

@app.route('/', methods = ['GET','POST'])
def process_request():
    data = request.get_json()

    selected_text = data.get('text','')
    processed_text = generate_content(selected_text)

    print("Processed Text: ", processed_text)
    return jsonify({'processed_text': processed_text})

if __name__ == '__main__':
    print("I am here")
    app.run(debug=True, host='0.0.0.0', port=8080)
