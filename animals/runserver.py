from animals import app
from pathlib import Path


Path(app.config['IMG_FOLDER']).mkdir(parents=True, exist_ok=True)
app.run(debug=True)
