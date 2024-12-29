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
- Environment setup :
```sh
# Use virtualenv package to create a virtual python environment:
sudo apt-get install python-virtualenv
# Clone the repository:
git clone git@github.com:olivier-2018/SoftwareEngg_project.git  --branch development
# Create a virtual environment within the repo:
virtualenv venv
# Activate the virtual environment:
source venv/bin/activate
# Install dependencies:
pip install -r requirements.txt
```
- Set Flask environment variables:
```sh
Linux:
export FLASK_APP=run.py
export FLASK_ENV=development (or production, or testing as required)
export SECRETE_KEY="<whatever you want>" (optional, Flask will assign a secret hash if unset)

Windows powershell:
$env:FLASK_APP = 'run.py'
$env:FLASK_ENV = 'development' (or 'production', or 'testing' as required)
$env: SECRETE_KEY = <whatever you want> (optional, Flask will assign a secret hash if unset)
```
- Launch the API locally:
```sh
flask run
```
*Note: on WSL you may need to export the display with an Xserver to run flask*
- The API will automatically deploy to Heroku upon succesful build on the main branch.

*Note: The Heroku app address is kept private not to reach the free account usage limit during the app development.*

 ### Testing:
- Unit and functional testing functions are located in the "tests" folder.
- Testing is automatic as part of the CI/CD pipeline but can also be launched manually using the command:
```sh
pytest -vrxXs
```

 ### Demo
<video src="static/video/SoftwareEngg_project_demo.mp4" width="1280" height="720" controls></video>

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
