## Software Engineering project
REST API development in Machine Learning applications

### Project goal & requirements:
- Develop an API from a trained machine learning model.
- Use GIT concept through the API development.
- Use of CI/CD pipeline is recommended for additional credits.
- The API should include testing, code formating and logging.
- The API should be executable.
- Documentation and presentation should be available upon submission.

### API documentation:
- The API takes the audio signal of a digit from 0 to 9 as input and returns the corresponding predicted digit.
- The selected machine learning model for this project is the audio MNIST ([Dataset](https://www.kaggle.com/sripaadsrinivasan/audio-mnist), [code](https://colab.research.google.com/github/AdvancedNLP/audio_mnist/blob/exercise/audio_mnist_tcn.ipynb)) which identifies digits from audio inputs.

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
- Set Flask environment variables, in a shell type:
```sh
export FLASK_APP=run.py
export FLASK_ENV=development
```
- Launch the API locally:
```sh
flask run
```
