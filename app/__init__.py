from flask import Flask
from .config import Config
from .extensions import db, jwt, migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    from app.models import User, Product, Order
    from app.routes import auth_bp
    from app.routes.user import user_bp
    from app.routes.product import product_bp
    from app.routes.order import order_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(order_bp)

    return app
