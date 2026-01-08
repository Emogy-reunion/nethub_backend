from app import create_app
from app.utils.create_upload_folder import create_upload_folder
from app.routes.authentication import auth
from app.routes.products import products_bp
from app.utils.seed import create_initial_admin

app = create_app()

with app.app_context():
    create_upload_folder()
    create_initial_admin()


app.register_blueprint(auth, url_prefix='/api')
app.register_blueprint(products_bp, url_prefix='/api')


if __name__ == '__main__':
    app.run(debug=True)
