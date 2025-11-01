import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class Config:
    """Configuration class to handle environment variables."""
    
    # Data folder where the YAML file will be stored
    DATA_FOLDER = os.getenv('WISHLIST_DATA_FOLDER', './data')
    
    # Images folder where uploaded images will be stored
    IMAGES_FOLDER = os.getenv('WISHLIST_IMAGES_FOLDER', './images')
    
    # Maximum file size for uploads (10MB)
    MAX_FILE_SIZE = 10 * 1024 * 1024
    
    # Allowed image extensions
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    @classmethod
    def ensure_directories(cls):
        """Create data and images directories if they don't exist."""
        os.makedirs(cls.DATA_FOLDER, exist_ok=True)
        os.makedirs(cls.IMAGES_FOLDER, exist_ok=True)
    
    @classmethod
    def is_allowed_file(cls, filename):
        """Check if file extension is allowed for upload."""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in cls.ALLOWED_EXTENSIONS