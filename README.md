## Software Engineering project
*API development in Machine Learning applications*

### Project requirements:
- Develop an API from a trained machine learning model.
- Use GIT concept through the API development.
- Use of CI/CD pipeline is recommended for additional credits.
- The API should include testing, code formating and logging.
- The API should be executable.
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
export FLASK_ENV=development

Windows powershell:
$env:FLASK_APP = 'run.py'
$env:FLASK_ENV = 'development'
```
- Launch the API locally:
```sh
flask run
```
- The API will automatically deploy to Heroku upon succesful build on the main branch.   
 Nb: The Heroku app address is kept private not to reach the free account usage limit during the app development.
 
### Testing:
- Files are created and deleted. Local Tests therefor are to be run with pytest to ensure files are deleted after tests:
```sh
pytest -v -W ignore
```

### Documentation:
The Documentation can be found in Wiki here: 

**https://github.com/olivier-2018/SoftwareEngg_project/wiki/Documentation-Project**
