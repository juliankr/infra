import os
import uuid
import requests
import mimetypes
from urllib.parse import urlparse
from flask import Flask, request, jsonify, send_from_directory, send_file
from werkzeug.utils import secure_filename
from PIL import Image
from config import Config
from models import MultiWishlistManager

app = Flask(__name__, static_folder='static', static_url_path='')
app.config['MAX_CONTENT_LENGTH'] = Config.MAX_FILE_SIZE

# Initialize manager
multi_wishlist_manager = MultiWishlistManager()

# Helper function to download image from URL
def download_image_from_url(image_url):
    """Download an image from a URL and save it locally."""
    try:
        # Validate URL
        parsed_url = urlparse(image_url)
        if not parsed_url.scheme or not parsed_url.netloc:
            return None, "Invalid URL format"
        
        # Set headers to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Download the image with timeout
        response = requests.get(image_url, headers=headers, timeout=10, stream=True)
        response.raise_for_status()
        
        # Check content type
        content_type = response.headers.get('content-type', '').lower()
        if not content_type.startswith('image/'):
            return None, "URL does not point to an image"
        
        # Get file extension from content type or URL
        extension = None
        if 'jpeg' in content_type or 'jpg' in content_type:
            extension = 'jpg'
        elif 'png' in content_type:
            extension = 'png'
        elif 'gif' in content_type:
            extension = 'gif'
        elif 'webp' in content_type:
            extension = 'webp'
        else:
            # Try to get extension from URL
            path = parsed_url.path.lower()
            for ext in Config.ALLOWED_EXTENSIONS:
                if path.endswith(f'.{ext}'):
                    extension = ext
                    break
        
        if not extension:
            extension = 'jpg'  # Default fallback
        
        # Check if extension is allowed
        if extension not in Config.ALLOWED_EXTENSIONS:
            return None, f"Image type not allowed. Allowed types: {', '.join(Config.ALLOWED_EXTENSIONS)}"
        
        # Generate unique filename
        unique_filename = f"{uuid.uuid4()}.{extension}"
        file_path = os.path.join(Config.IMAGES_FOLDER, unique_filename)
        
        # Save the image
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        # Validate and optimize the image
        try:
            with Image.open(file_path) as img:
                # Verify it's a valid image
                img.verify()
                
                # Reopen for processing (verify() closes the image)
                with Image.open(file_path) as img:
                    # Convert to RGB if necessary
                    if img.mode in ('RGBA', 'P'):
                        img = img.convert('RGB')
                    
                    # Resize if too large (keep aspect ratio)
                    max_size = (1200, 1200)
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)
                    img.save(file_path, optimize=True, quality=85)
                    
        except Exception as img_error:
            # Remove the invalid file
            if os.path.exists(file_path):
                os.remove(file_path)
            return None, f"Invalid image file: {str(img_error)}"
        
        return unique_filename, None
        
    except requests.exceptions.Timeout:
        return None, "Request timeout - the image took too long to download"
    except requests.exceptions.RequestException as e:
        return None, f"Failed to download image: {str(e)}"
    except Exception as e:
        return None, f"Error processing image: {str(e)}"

# Tabs API endpoints
@app.route('/api/tabs', methods=['GET'])
def get_tabs():
    """Get all wishlist tabs."""
    try:
        tabs = multi_wishlist_manager.get_tabs()
        return jsonify({
            'success': True,
            'data': tabs
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/tabs', methods=['POST'])
def create_tab():
    """Create a new wishlist tab."""
    try:
        data = request.get_json()
        
        if not data or 'name' not in data:
            return jsonify({
                'success': False,
                'error': 'Tab name is required'
            }), 400
        
        name = data['name'].strip()
        if not name:
            return jsonify({
                'success': False,
                'error': 'Tab name cannot be empty'
            }), 400
        
        new_tab = multi_wishlist_manager.create_tab(name)
        
        return jsonify({
            'success': True,
            'data': new_tab
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/tabs/<tab_id>', methods=['PUT'])
def rename_tab(tab_id):
    """Rename a wishlist tab."""
    try:
        data = request.get_json()
        
        if not data or 'name' not in data:
            return jsonify({
                'success': False,
                'error': 'Tab name is required'
            }), 400
        
        name = data['name'].strip()
        if not name:
            return jsonify({
                'success': False,
                'error': 'Tab name cannot be empty'
            }), 400
        
        success = multi_wishlist_manager.rename_tab(tab_id, name)
        
        if not success:
            return jsonify({
                'success': False,
                'error': 'Tab not found'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Tab renamed successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/tabs/<tab_id>', methods=['DELETE'])
def delete_tab(tab_id):
    """Delete a wishlist tab."""
    try:
        success = multi_wishlist_manager.delete_tab(tab_id)
        
        if not success:
            return jsonify({
                'success': False,
                'error': 'Tab not found or cannot delete the last tab'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Tab deleted successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Multi-tab wishlist endpoints
@app.route('/api/tabs/<tab_id>/wishlist', methods=['GET'])
def get_tab_wishlist(tab_id):
    """Get wishlist items for a specific tab."""
    try:
        tab_manager = multi_wishlist_manager.get_wishlist_manager(tab_id)
        
        if not tab_manager:
            return jsonify({
                'success': False,
                'error': 'Tab not found'
            }), 404
        
        items = tab_manager.get_all_items()
        return jsonify({
            'success': True,
            'data': items
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/tabs/<tab_id>/wishlist', methods=['POST'])
def add_tab_wishlist_item(tab_id):
    """Add a new wishlist item to a specific tab."""
    try:
        tab_manager = multi_wishlist_manager.get_wishlist_manager(tab_id)
        
        if not tab_manager:
            return jsonify({
                'success': False,
                'error': 'Tab not found'
            }), 404
        
        data = request.get_json()
        
        if not data or 'title' not in data:
            return jsonify({
                'success': False,
                'error': 'Title is required'
            }), 400
        
        title = data['title']
        image = data.get('image')
        image_url = data.get('image_url')
        weblink = data.get('weblink')
        
        # Handle image URL download if provided
        if image_url and not image:
            downloaded_filename, error = download_image_from_url(image_url.strip())
            if error:
                return jsonify({
                    'success': False,
                    'error': f'Failed to download image: {error}'
                }), 400
            image = downloaded_filename
        
        new_item = tab_manager.add_item(title=title, image=image, weblink=weblink)
        
        return jsonify({
            'success': True,
            'data': new_item
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/tabs/<tab_id>/wishlist/<item_id>', methods=['PUT'])
def update_tab_wishlist_item(tab_id, item_id):
    """Update a wishlist item in a specific tab."""
    try:
        tab_manager = multi_wishlist_manager.get_wishlist_manager(tab_id)
        
        if not tab_manager:
            return jsonify({
                'success': False,
                'error': 'Tab not found'
            }), 404
        
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        title = data.get('title')
        image = data.get('image')
        image_url = data.get('image_url')
        weblink = data.get('weblink')
        
        # Handle image URL download if provided and no direct image filename
        if image_url and not image:
            downloaded_filename, error = download_image_from_url(image_url.strip())
            if error:
                return jsonify({
                    'success': False,
                    'error': f'Failed to download image: {error}'
                }), 400
            image = downloaded_filename
        
        updated_item = tab_manager.update_item(
            item_id=item_id,
            title=title,
            image=image,
            weblink=weblink
        )
        
        if not updated_item:
            return jsonify({
                'success': False,
                'error': 'Item not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': updated_item
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/tabs/<tab_id>/wishlist/<item_id>', methods=['DELETE'])
def delete_tab_wishlist_item(tab_id, item_id):
    """Delete a wishlist item from a specific tab."""
    try:
        tab_manager = multi_wishlist_manager.get_wishlist_manager(tab_id)
        
        if not tab_manager:
            return jsonify({
                'success': False,
                'error': 'Tab not found'
            }), 404
        
        success = tab_manager.delete_item(item_id)
        
        if not success:
            return jsonify({
                'success': False,
                'error': 'Item not found'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Item deleted successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/tabs/<tab_id>/wishlist/reorder', methods=['POST'])
def reorder_tab_wishlist(tab_id):
    """Reorder wishlist items in a specific tab."""
    try:
        tab_manager = multi_wishlist_manager.get_wishlist_manager(tab_id)
        
        if not tab_manager:
            return jsonify({
                'success': False,
                'error': 'Tab not found'
            }), 404
        
        data = request.get_json()
        
        if not data or 'item_ids' not in data:
            return jsonify({
                'success': False,
                'error': 'item_ids array is required'
            }), 400
        
        item_ids = data['item_ids']
        
        if not isinstance(item_ids, list):
            return jsonify({
                'success': False,
                'error': 'item_ids must be an array'
            }), 400
        
        success = tab_manager.reorder_items(item_ids)
        
        if not success:
            return jsonify({
                'success': False,
                'error': 'Failed to reorder items. Check that all item IDs are valid.'
            }), 400
        
        return jsonify({
            'success': True,
            'message': 'Items reordered successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/upload', methods=['POST'])
def upload_image():
    """Upload an image file."""
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file provided'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        if not Config.is_allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': f'File type not allowed. Allowed types: {", ".join(Config.ALLOWED_EXTENSIONS)}'
            }), 400
        
        # Generate unique filename
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(Config.IMAGES_FOLDER, unique_filename)
        
        # Save the file
        file.save(file_path)
        
        # Optionally resize image to optimize for web/iPad
        try:
            with Image.open(file_path) as img:
                # Resize if image is too large (keep aspect ratio)
                max_size = (1200, 1200)
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                img.save(file_path, optimize=True, quality=85)
        except Exception as resize_error:
            print(f"Warning: Could not resize image: {resize_error}")
        
        return jsonify({
            'success': True,
            'data': {
                'filename': unique_filename,
                'url': f'/api/images/{unique_filename}'
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/download-image', methods=['POST'])
def download_image():
    """Download an image from a URL."""
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({
                'success': False,
                'error': 'Image URL is required'
            }), 400
        
        image_url = data['url'].strip()
        
        if not image_url:
            return jsonify({
                'success': False,
                'error': 'Image URL cannot be empty'
            }), 400
        
        # Download and save the image
        filename, error = download_image_from_url(image_url)
        
        if error:
            return jsonify({
                'success': False,
                'error': error
            }), 400
        
        return jsonify({
            'success': True,
            'data': {
                'filename': filename,
                'url': f'/api/images/{filename}',
                'original_url': image_url
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/images/<filename>')
def serve_image(filename):
    """Serve uploaded images."""
    try:
        return send_from_directory(Config.IMAGES_FOLDER, filename)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Image not found'
        }), 404

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'success': True,
        'message': 'Wishlist API is running',
        'version': '1.0.0'
    })

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error."""
    return jsonify({
        'success': False,
        'error': f'File too large. Maximum size is {Config.MAX_FILE_SIZE // (1024 * 1024)}MB'
    }), 413

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle internal server errors."""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

# Frontend routes - serve static files
@app.route('/')
def serve_frontend():
    """Serve the main frontend application."""
    try:
        return send_file('static/index.html')
    except Exception:
        return jsonify({
            'success': False,
            'error': 'Frontend not found. Make sure the app is built properly.'
        }), 404

@app.route('/<path:path>')
def serve_static_files(path):
    """Serve static files from the frontend build."""
    try:
        return send_from_directory('static', path)
    except Exception:
        # For SPA routing, return index.html for non-API routes
        if not path.startswith('api/'):
            try:
                return send_file('static/index.html')
            except Exception:
                pass
        return jsonify({
            'success': False,
            'error': 'File not found'
        }), 404

if __name__ == '__main__':
    # Ensure directories exist
    Config.ensure_directories()
    
    # Run the application
    app.run(host='0.0.0.0', port=5000, debug=False)