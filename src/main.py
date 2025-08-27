from src.app import create_app
from src.config import Config
from src.logging_config import setup_logging
from src.startup import bootstrap_application

setup_logging()

bootstrap_application()

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.PORT)
