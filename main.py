from datetime import timedelta
from dotenv import load_dotenv
from datetime import timedelta

from app import create_app, db

load_dotenv()

app = create_app()
app.permanent_session_lifetime = timedelta(days=5)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)