from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from time import sleep

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', "")
genai.configure(api_key=GOOGLE_API_KEY)

app = Flask(__name__)
CORS(app)
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

loading=False
# @app.route('/fetch_gemini', methods=['POST'])
# def fetch_gemini():
#     global loading
#     url = request.form['url']
#     isYoutube = url.startswith("https://www.youtube.com/watch?v=")
#     link=url[32:43]
#     if(isYoutube):
#         transcript=""
#         try:
#             x = YouTubeTranscriptApi.get_transcript(link,languages=['en','hi'])
#             for i in range(len(x)):
#                 transcript += x[i]["text"]+" "
#         except Exception as e:
#             return jsonify({'gemini_response':f'No transcript found for the video. Please try again with other video. {e}'})
#         else:
#             if not loading :
#                 loading=True
#                 response = model.generate_content("Tell the key points in this video from the transcript given below"+transcript)
#                 loading=False
#             else:
#                 return jsonify({'gemini_response':'Please try again after a while. Gemini was loading.'})
        
#     else:
#         response = model.generate_content("Summarize the content of the given website in key points "+url)
#     answer = response.text
#     return jsonify({'gemini_response':answer})

@app.route('/fetch_gemini', methods=['POST'])
def fetch_gemini():
    global loading
    url = request.form['url']
    isYoutube = url.startswith("https://www.youtube.com/watch?v=")
    link = url[32:43]
    
    if isYoutube:
        transcript = ""
        max_retries = 3
        retry_delay = 5  # seconds

        for retry_count in range(max_retries):
            try:
                x = YouTubeTranscriptApi.get_transcript(link, languages=['en'])
                for i in range(len(x)):
                    transcript += x[i]["text"] + " "
                break  # Break out of the loop if successful
            except Exception as e:
                print(f"Error fetching transcript: {str(e)}")
                if retry_count < max_retries - 1:
                    print(f"Retrying in {retry_delay} seconds...")
                    sleep(retry_delay)
                else:
                    # Handle the case when all retries are exhausted
                    return jsonify({'gemini_response': f'Error fetching transcript: {str(e)}'})

        if not loading:
            loading = True
            response = model.generate_content("Tell the key points in this video from the transcript given below" + transcript)
            loading = False
        else:
            return jsonify({'gemini_response': 'Please try again after a while. Gemini was loading.'})

    else:
        response = model.generate_content("Summarize the content of the given website in key points " + url)

    answer = response.text
    return jsonify({'gemini_response': answer})

# for development only
# if __name__ == "__main__":
#     print("Starting Python Flask Server For Summarizing Website and YT videos")
#     app.run(debug=True)

# for production comment above