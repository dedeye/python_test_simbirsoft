from animals import app
from pathlib import Path


Path(app.instance_path + "/img").mkdir(parents=True, exist_ok=True)
app.run(debug=True)
