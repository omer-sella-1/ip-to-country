from src.app import create_app
from src.config import Config
from src.startup import bootstrap_application

bootstrap_application()

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.PORT)
