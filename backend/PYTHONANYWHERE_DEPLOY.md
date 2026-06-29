# PythonAnywhere Backend Deployment

This deploys the FastAPI `/predict` backend behind PythonAnywhere's WSGI web app runner.

## 1. Clone The Repo

In a PythonAnywhere Bash console:

```bash
git clone https://github.com/sanginicoco1812/Coolscape-AI.git
cd Coolscape-AI
```

If the repo already exists:

```bash
cd Coolscape-AI
git pull origin main
```

## 2. Create Virtualenv

Use a Python version available in your PythonAnywhere account:

```bash
python3.10 -m venv ~/.virtualenvs/heatshield
source ~/.virtualenvs/heatshield/bin/activate
pip install --upgrade pip
pip install -r backend/requirements-pythonanywhere.txt
```

## 3. Configure Web App

In PythonAnywhere:

1. Open the **Web** tab.
2. Create a new manual web app.
3. Choose the same Python version used for the virtualenv.
4. Set the virtualenv path:

```text
/home/YOUR_USERNAME/.virtualenvs/heatshield
```

5. Edit the WSGI file and replace its contents with:

```python
import sys

project_root = "/home/YOUR_USERNAME/Coolscape-AI"

if project_root not in sys.path:
    sys.path.insert(0, project_root)

from backend.pythonanywhere_wsgi import application
```

Replace `YOUR_USERNAME` with your PythonAnywhere username.

## 4. Reload

Go back to the **Web** tab and click **Reload**.

Your backend should be available at:

```text
https://YOUR_USERNAME.pythonanywhere.com/predict
```

## 5. Test API

```bash
curl -X POST https://YOUR_USERNAME.pythonanywhere.com/predict \
  -H "Content-Type: application/json" \
  -d '{
    "city": "Delhi",
    "ndvi": 0.18,
    "humidity": 72,
    "windSpeed": 6,
    "buildingDensity": 82
  }'
```

## 6. Connect Netlify

In Netlify project settings, add:

```text
VITE_API_URL=https://YOUR_USERNAME.pythonanywhere.com
```

Then redeploy the frontend.
