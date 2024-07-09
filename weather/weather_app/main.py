import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from weather_app import app, db

# Load env file
load_dotenv()

if __name__ == "__main__":
    db.create_all()
    app.run(
        host=os.getenv("SERVER_ADDRESS", "127.0.0.1"),
        port=int(os.getenv("SERVER_PORT", 5000)),
        debug=True,
    )
