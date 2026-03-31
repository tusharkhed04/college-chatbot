from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")

    from config import Config
    app.config.from_object(Config)

    try:
        conn = pymysql.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="",
        )
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS `college_chatbot` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Database 'college_chatbot' ready.")
    except Exception as e:
        print(f"❌ MySQL Error: {e}")
        raise

    db.init_app(app)

    from app.routes.main  import main_bp
    from app.routes.chat  import chat_bp
    from app.routes.auth  import auth_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    with app.app_context():
        db.create_all()
        from app.models.seed import seed_data
        seed_data()

    return app