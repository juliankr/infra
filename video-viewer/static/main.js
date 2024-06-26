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

function validateForm() {
    var title = document.getElementById('title').value;
    var youtube_id = document.getElementById('youtube_id').value;
    document.getElementById('submit').disabled = !(title && youtube_id);
}

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

window.onload = function() {
    fetch('/videos')
        .then(response => response.json())
        .then(data => {
            var videoList = document.getElementById('video-list');
            data.videos.forEach(video => {
                var videoElement = document.createElement('div');
                videoElement.innerHTML = `
                    <h1>${video.title}<button class="delete-button" onclick="deleteVideo('${video.youtube_id}')">Delete</button></h1>
                    <div class="video-container">
                        <iframe class="video-frame" src="https://www.youtube.com/embed/${video.youtube_id}?start=10" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                    </div>
                `;
                videoList.appendChild(videoElement);
            });
        });
}

