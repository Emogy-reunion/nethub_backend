from app import create_app
from app.routes.authentication import auth
from app.routes.upload import post

app = create_app()


app.register_blueprint(auth, url_prefix='api')
app.register_blueprint(post, url_prefix='api')

if __name__ == '__main__':
    app.run(debug=True)
