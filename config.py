import os

class Config:
    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    
    # Debug mode
    DEBUG = True
    
    # Application directory
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    # Model directory
    MODEL_DIR = os.path.join(BASE_DIR, 'model')