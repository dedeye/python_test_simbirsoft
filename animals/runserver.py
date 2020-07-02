from animals import app
from pathlib import Path

# create img folder if not exists
Path(app.config['IMG_FOLDER']).mkdir(parents=True, exist_ok=True)

app.run()
