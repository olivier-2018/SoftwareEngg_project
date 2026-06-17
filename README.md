## Software Engineering project
*API development using a Machine Learning model*

### Project requirements:
- Develop an API making use of a trained machine learning model.
- Use GIT version control concept through the API development.
- The API should include testing, code formating, logging and user login features.
- The API should be executable.
- Implement a CI/CD pipeline for additional credits.
- Documentation and presentation should be available upon submission.

### API main goal:
- The API is to process a single digit (from 0 to 9) audio signal and return the corresponding predicted digit using ML model in the backend.
- The selected machine learning model for this project is the audio MNIST ([Dataset](https://www.kaggle.com/sripaadsrinivasan/audio-mnist), [code](https://colab.research.google.com/github/AdvancedNLP/audio_mnist/blob/exercise/audio_mnist_tcn.ipynb)) which identifies digits from audio inputs.

**Disclaimer:** the ML model was trained to a 94% test accuracy but does not generalize on all real life test cases due to the reduced dataset size. Training the ML model on additional / augmented data is out of the project'scope.
- The basic input method is through file selection. Additional developments are listed below if time permits..

### API optional future developments (out of project'scope):
- Capture single digit audio signal from microphone.
- Capture multiple digit audio signal from microphone and return sequence of predicted digits.
- Use multiple digit audio prediction for user login.
- Use augmented / additional data to improve generalization on model prediction (male/female voices, accents, etc).

### Getting started:

#### Prerequisites

This project uses `uv` for fast, reliable dependency management. 

**Install `uv`** (if not already installed):
```sh
# On Linux/macOS using curl:
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows using PowerShell:
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### Clone and set up the project:
```sh
# Clone the repository:
git clone git@github.com:olivier-2018/SoftwareEngg_project.git 
cd SoftwareEngg_project

# Sync dependencies using uv (creates/updates .venv automatically):
uv sync

# Alternatively, if you prefer pip and manual venv:
python -m venv venv
# Activate: source venv/bin/activate (Linux/macOS) or venv\Scripts\activate (Windows)
pip install -e .

# Copy environment config template and customize:
cp .env.example .env
# Edit .env to add a SECRET_KEY if desired (a default is provided for local dev)
```

#### Running the Development Server
```sh
# The .env file automatically loads Flask configuration
flask run 
```

The app will start on **http://localhost:5003** with **live reload enabled** (`FLASK_DEBUG=1` in .env) — changes to templates, static files, and Python code automatically reload in the browser.

### Developments

#### Testing:
- Unit and functional testing functions are located in the "tests" folder.
- Testing is automatic as part of the CI/CD pipeline but can also be launched manually using the command:
```sh
pytest -vrxXs
```

#### Pre-commit

Pre‑commit runs a set of hooks every time you run git commit.   
These hooks can:  
- auto‑format code  
- lint Python and JS
- check for syntax errors
- block commits with secrets
- validate JSON/YAML
- enforce consistent whitespace

Pre-commit can be run manually before a *git commit*,  
```sh
pre-commit run
# this will automateically read the *.pre-commit-config.yaml* cfg file
```

or automatically with each *git commit* using hooks.  
Set up hooks with  
```sh
pre-commit install
pre-commit run --all-files
```


### Deployment on VPS

To deploy on a self-hosted VPS using Docker and Docker Compose:

```sh
# On your VPS, clone the repo and set up environment:
git clone <repo-url>
cd SoftwareEngg_project

# Create production .env (do NOT commit this to git):
cp .env.example .env
# Edit .env with production values:
#   FLASK_ENV=production
#   FLASK_DEBUG=0
#   SECRET_KEY=<generate-a-secure-key>

# Build and run the containerized app:
docker compose build --no-cache
docker compose up -d 

# The app listens on port 5003. Configure a reverse proxy (e.g., nginx)
# to forward traffic to the container and handle HTTPS/TLS termination.
```

**Important:** On a VPS, the app requires **HTTPS** for the microphone recording feature (`getUserMedia` requires a secure context). Use a reverse proxy (nginx, Caddy, etc.) with Let's Encrypt certificates, or AWS load balancer, etc., to terminate TLS and forward to port 5003.



 ### Illustrations:
 #### Welcome screen
 <image src="./static/img/1_welcome_screen.png" alt="Welcome screen">

 #### Sign-up screen
 <image src="./static/img/2_sign-up.png" alt="Sign-up screen">

 #### Welcome screen
 <image src="./static/img/3_sign-in_screen.png" alt="Sign-in screen">

 #### Sign-in screen
 <image src="./static/img/3_successful_login.png" alt="Login screen">

 #### App selection
 <image src="./static/img/4_app_selection.png" alt="App selection">

 #### API call and results
 <image src="./static/img/5_API_call_and_resut.png" alt="API call and results">

 #### User profile screen
 <image src="./static/img/6_user_profile_screen.png" alt="User profile screen">

 #### App version screen
 <image src="./static/img/7_version_history_screen.png" alt="App version screen">

 #### Information screen
 <image src="./static/img/8_about_screen.png" alt="Information screen">

#### Tests
 <image src="./static/img/9_unit_fcnal_tests.png" alt="tests info">

#### CI/CD & deployment
 <image src="./static/img/10_CICD_deployment.png" alt="CICD info">
