# Software Engineering project 
REST API development in Machine Learning applications

## Project goal & requirements:  
- Develop an API from a trained machine learning model.  
- Use GIT concept through the API development.   
- Use of CI/CD pipeline is recommended for additional credits.  
- The API should include testing, code formating and logging.  
- The API should be executable.  
- Documentation and presentation should be available upon submission.   

## API documentation and planned scope:  
- The ML model selected for this project is the audio MNIST ([Dataset](https://www.kaggle.com/sripaadsrinivasan/audio-mnist), [code](https://colab.research.google.com/github/AdvancedNLP/audio_mnist/blob/exercise/audio_mnist_tcn.ipynb)) which identifies digits from audio inputs.  
- The API takes as input an audio signal (from file or captured audio) and returns the corresponding digit.  
 
## Getting started:  
- I recommend using the virtualenv package to create a virtual python environment: sudo apt-get install python-virtualenv
- Clone the repository: git clone git@github.com:olivier-2018/SoftwareEngg_project.git
- Create a virtual environment within the repo: virtualenv venv
- Activate the virtual environment: source venv/bin/activate
- Install dependencies: pip install -r requirements.txt
- Launch the API locally: flask run


