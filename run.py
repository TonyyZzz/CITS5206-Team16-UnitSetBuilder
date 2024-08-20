import os
from dotenv import load_dotenv
from app import create_app

load_dotenv()  # Load environment variables from .env

config_name = os.getenv('FLASK_ENV') or 'development'
app = create_app(config_name)

if __name__ == '__main__':
    app.run()
