from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from extensions import db, mail
from app.models import Cars, Images, Title_info
from collections import defaultdict
from sqlalchemy import select
from dotenv import load_dotenv
from flask_wtf import CSRFProtect

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "dev-secret-key")
    csrf = CSRFProtect(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///data.db")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
    app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")

    @app.context_processor
    def images_to_page():
        all_images = Images.query.all()
        images = defaultdict(list)
        for img in all_images:
            images[img.image_name].extend(img.image_file_path)
        return dict(images=dict(images))


    @app.context_processor
    def context_processor():
        car_content = select(Cars.content)
        all_row = db.session.execute(car_content).mappings().all()
        car_vars = {}
        for i, row in enumerate(all_row, start=1):
            car_vars[f'vehicle{i}'] = row['content']
        return {"car_vars": car_vars}


    @app.context_processor
    def info_to_page():
        all_info = [row.to_dict() for row in Title_info.query.all()]
        return dict(all_info=all_info)
    
    from .routes import main_bp
    app.register_blueprint(main_bp)

    db.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)

    from app import models

    return app