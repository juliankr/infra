from flask import Flask, request, send_from_directory, redirect, jsonify
import yaml
import os
from pythonjsonlogger import jsonlogger
import logging


app = Flask(__name__)

# Configure root logging
rootLogger = logging.getLogger()
jsonHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
jsonHandler.setFormatter(formatter)
rootLogger.addHandler(jsonHandler)
rootLogger.setLevel(logging.INFO)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/')
def home():
    return send_from_directory('static', 'index.html')


@app.route('/videos')
def videos():
    with open('data/videos.yaml', 'r') as file:
        videos = yaml.safe_load(file)
    return jsonify(videos)


@app.route('/', methods=['POST'])
def add_video():
    title = request.form.get('title')
    youtube_id = request.form.get('youtube_id')
    new_video = {'title': title, 'youtube_id': youtube_id}

    with open('data/videos.yaml', 'r') as file:
        videos = yaml.safe_load(file)

    # Check if the title or YouTube ID already exists
    for video in videos['videos']:
        if video['title'] == title or video['youtube_id'] == youtube_id:
            return 'Conflict: Video with this title or YouTube ID already exists', 409

    videos['videos'].append(new_video)

    with open('data/videos.yaml', 'w') as file:
        yaml.dump(videos, file)

    return redirect('/', code=302)


@app.route('/delete_video/<youtube_id>', methods=['POST'])
def delete_video(youtube_id):
    with open('data/videos.yaml', 'r') as file:
        videos = yaml.safe_load(file)

    # Find the video with the matching YouTube ID and remove it
    videos['videos'] = [video for video in videos['videos'] if video['youtube_id'] != youtube_id]

    with open('data/videos.yaml', 'w') as file:
        yaml.dump(videos, file)

    return redirect('/', code=302)

# Start the server on port 3000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
