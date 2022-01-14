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
- Use virtualenv package to create a virtual python environment:
```sh
sudo apt-get install python-virtualenv
```
- Clone the repository:
```sh
git clone git@github.com:olivier-2018/SoftwareEngg_project.git
```
- Create a virtual environment within the repo:
```sh
virtualenv venv
```
- Activate the virtual environment:
```sh
source venv/bin/activate
```
- Install dependencies:
```sh
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
