from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', "")
genai.configure(api_key=GOOGLE_API_KEY)

app = Flask(__name__)
CORS(app)

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

@app.route('/fetch_gemini', methods=['POST'])
def fetch_gemini():
    url = request.form['url']
    isYoutube = url.startswith("https://www.youtube.com/watch?v=")
    link=url[32:43]
    if(isYoutube):
        transcript=""
        x = YouTubeTranscriptApi.get_transcript(link,languages=['en','hi'])
        for i in range(len(x)):
            transcript += x[i]["text"]+" "
        response = model.generate_content("Tell the key points in this video from the transcript given below"+transcript)
    else:
        response = model.generate_content("Summarize the content of the given website in key points "+url)
    answer = response.text
    return jsonify({'gemini_response':answer})


# for development only
# if __name__ == "__main__":
#     print("Starting Python Flask Server For Summarizing Website and YT videos")
#     app.run(debug=True)

# for production comment above