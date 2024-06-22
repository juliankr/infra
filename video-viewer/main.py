from flask import Flask, request, send_from_directory, redirect
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
    with open('data/videos.yaml', 'r') as file:
        videos = yaml.safe_load(file)['videos']
    html = '<!DOCTYPE html><html><body>'
    html += generate_reset_button_html()
    html += generate_video_html(videos)
    html += generate_form_html()
    html += generate_delete_toggle_html()
    return html

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

def generate_reset_button_html():
    return '''
    <style>
    button {
        padding: 15px 25px;
        font-size: 24px;
        text-align: center;
        cursor: pointer;
        outline: none;
        color: #fff;
        background-color: #4CAF50;
        border: none;
        border-radius: 15px;
        box-shadow: 0 9px #999;
    }

    button:hover {background-color: #3e8e41}

    button:active {
        background-color: #3e8e41;
        box-shadow: 0 5px #666;
        transform: translateY(4px);
    }
    </style>
    <button onclick="resetPage()">Reset</button>
    <script>
    function resetPage() {
        // Reset the videos
        var iframes = document.getElementsByTagName('iframe');
        for (var i = 0; i < iframes.length; i++) {
            iframes[i].src = iframes[i].src;
        }

        // Turn off deletion
        var deleteButtons = document.getElementsByClassName('delete-button');
        for (var i = 0; i < deleteButtons.length; i++) {
            deleteButtons[i].style.display = 'none';
        }

        // Uncheck the delete toggle
        document.getElementById('delete-toggle').checked = false;
    }
    </script>
    '''
    
def generate_video_html(videos):
    html = ''
    for video in videos:
        html += f'<h1>{video["title"]}<button class="delete-button" style="display: none;" onclick="deleteVideo(\'{video["youtube_id"]}\')">Delete</button></h1>'
        html += '''
        <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden;">
            <iframe style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" src="https://www.youtube.com/embed/{}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        </div>
        '''.format(video["youtube_id"])
    return html

def generate_form_html():
    return '''
     <style>
    input[type="text"], input[type="submit"] {
        width: 100%;
        padding: 12px 20px;
        margin: 8px 0;
        display: inline-block;
        border: 1px solid #ccc;
        border-radius: 4px;
        box-sizing: border-box;
        font-size: 18px;
    }
    </style>
    <form method="POST" action="/" oninput="validateForm()">
        <label for="title">Title:</label><br>
        <input type="text" id="title" name="title"><br>
        <label for="youtube_id">YouTube ID:</label><br>
        <input type="text" id="youtube_id" name="youtube_id"><br>
        <input type="submit" id="submit" value="Submit" disabled>
    </form>
    <script>
    function validateForm() {
        var title = document.getElementById('title').value;
        var youtube_id = document.getElementById('youtube_id').value;
        document.getElementById('submit').disabled = !(title && youtube_id);
    }
    </script>
    '''

def generate_delete_toggle_html():
    return '''
    <style>
    input[type="checkbox"] {
        width: 25px;
        height: 25px;
    }
    </style>
    <input type="checkbox" id="delete-toggle" onchange="toggleDelete()">Enable deletion of videos
    <script>
    function toggleDelete() {
        var deleteButtons = document.getElementsByClassName('delete-button');
        for (var i = 0; i < deleteButtons.length; i++) {
            deleteButtons[i].style.display = document.getElementById('delete-toggle').checked ? 'block' : 'none';
        }
    }
    function deleteVideo(youtube_id) {
        fetch('/delete_video/' + youtube_id, {method: 'POST'})
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                location.reload();
            })
            .catch(error => console.error('There has been a problem with your fetch operation: ', error));
        }
    </script>
    '''

# Start the server on port 3000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
