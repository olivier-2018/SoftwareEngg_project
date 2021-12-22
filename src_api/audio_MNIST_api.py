from flask import Flask, render_template, request, redirect
import os
import logging
import librosa
import tensorflow
import numpy as np
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='../templates')

logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(filename='app.log', level=logging.DEBUG,format=’%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s’)

app.logger.info("ROOT FOLDER: "+app.root_path)
APP_FOLDER = os.path.abspath(os.path.join(app.root_path, os.pardir))
app.logger.info("APP FOLDER: "+APP_FOLDER)
UPLOAD_FOLDER = os.path.join(app.root_path, '../static/client/wav')
# UPLOAD_FOLDER = app.instance_path+"/../static/client/wav/"
app.logger.info("UPLOAD FOLDER: "+UPLOAD_FOLDER) 

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["ALLOWED_EXTENSIONS"] = set(["wav"])


@app.route("/", methods=["GET", "POST"])
def index():
    app.logger.info('starting web page') 
    prediction = ""
    if request.method == "POST":
        print("FORM DATA RECEIVED")

        if "file" not in request.files:
            return redirect(request.url)

        audiofile = request.files["file"]
        
        if audiofile.filename == "":
            return redirect(request.url)

        if audiofile:
            app.logger.info("AUDIO FILENAME: "+audiofile.filename)

            audiofile.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(audiofile.filename)))
            app.logger.info("Audio file saved.")

            model_path = APP_FOLDER+"/ML_model/audio_MNIST_v1.tf"
            app.logger.info("MODEL PATH: "+model_path)
            model = tensorflow.keras.models.load_model(model_path)
            app.logger.info("Model loaded.") 
            
            SAMPLING_RATE=16_000
            MAX_DURATION_S=0.5

            audio = np.zeros(int(MAX_DURATION_S * SAMPLING_RATE))
            path = os.path.join(app.config['UPLOAD_FOLDER'], audiofile.filename)

            app.logger.info("Reading audio file with librosa.") 
            waveform, __ = librosa.load(path, sr=SAMPLING_RATE)
            waveform = waveform[:len(audio)]
            audio[:len(waveform)] = waveform
            audio_input = audio.reshape((1,8000,1))

            app.logger.info("Making prediction.") 
            prediction_proba = model.predict(audio_input)
            
            app.logger.info("Taking argmax of prediction probability.") 
            prediction = np.argmax(prediction_proba)

    return render_template('index.html', model_prediction=prediction)



# def load_audio(path, sampling_rate=SAMPLING_RATE, duration_s=MAX_DURATION_S):
#     audio = np.zeros(int(duration_s * sampling_rate))
#     waveform, __ = librosa.load(path, sr=sampling_rate)
#     waveform = waveform[:len(audio)]
#     audio[:len(waveform)] = waveform
#     return audio

if __name__ == "__main__":
    app.run(debug=False) #debug=False, threaded=True)
    
