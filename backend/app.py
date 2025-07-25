from backend import create_app
from backend.routes import main

app = create_app()
app.register_blueprint(main)

if __name__ == '__main__':
    app.run(debug=True) 