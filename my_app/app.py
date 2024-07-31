#importing necessary libraries
from flask import Flask, request, jsonify, render_template
import torch
import librosa as lb
import os
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC

app = Flask(__name__)

# Loading your trained models from specified paths
processor_high = Wav2Vec2Processor.from_pretrained("C:/Users/gbiko/OneDrive/Desktop/Ashesi-Capstone/model_high")
model_high = Wav2Vec2ForCTC.from_pretrained("C:/Users/gbiko/OneDrive/Desktop/Ashesi-Capstone/model_high")

processor_medium = Wav2Vec2Processor.from_pretrained("C:/Users/gbiko/OneDrive/Desktop/Ashesi-Capstone/model_medium")
model_medium = Wav2Vec2ForCTC.from_pretrained("C:/Users/gbiko/OneDrive/Desktop/Ashesi-Capstone/model_medium")

processor_baseline = Wav2Vec2Processor.from_pretrained("C:/Users/gbiko/OneDrive/Desktop/Ashesi-Capstone/model_baseline")
model_baseline = Wav2Vec2ForCTC.from_pretrained("C:/Users/gbiko/OneDrive/Desktop/Ashesi-Capstone/model_baseline")

def loading_audio_file(audio_path):
    waveform, sample_rate = lb.load(audio_path, sr=16000)
    return waveform, sample_rate

def tokenizing_waveform(waveform, sr, processor):
    input_values = processor(waveform, sampling_rate=sr, return_tensors="pt").input_values
    return input_values

def get_transcript(input_values, processor, model):
    with torch.no_grad():
        logits = model(input_values).logits
        pred_ids = torch.argmax(logits, dim=-1)
        transcription = processor.batch_decode(pred_ids)[0]
    return transcription

@app.route('/')
def index():
    return render_template('Interface_high.html')

@app.route('/interface_medium')
def interface_medium():
    return render_template('Interface_medium.html')

@app.route('/interface_baseline')
def interface_baseline():
    return render_template('Interface_baseline.html')

# transcribing using high accuracy model
@app.route('/transcribe_high', methods=['POST'])
def transcribe_high():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'Empty file name'}), 400
        
        # Save the uploaded file to a temporary location
        file_path = 'temp_high.webm'  # Save as WebM
        file.save(file_path)
        
        waveform, sample_rate = loading_audio_file(file_path)
        input_values = tokenizing_waveform(waveform, sample_rate, processor=processor_high)
        transcription = get_transcript(input_values, processor=processor_high, model=model_high)

        os.remove(file_path)
        
        return jsonify({'transcription': transcription})
    
    except Exception as e:
        app.logger.error(f"Error processing file: {str(e)}")
        return jsonify({'error': 'Error uploading file.'}), 500

# transcribing using medium accuracy model
@app.route('/transcribe_medium', methods=['POST'])
def transcribe_medium():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'Empty file name'}), 400
        
        # Save the uploaded file to a temporary location
        file_path = 'temp_medium.webm'  # Save as WebM
        file.save(file_path)
        
        waveform, sample_rate = loading_audio_file(file_path)
        input_values = tokenizing_waveform(waveform, sample_rate, processor=processor_medium)
        transcription = get_transcript(input_values, processor=processor_medium, model=model_medium)

        os.remove(file_path)
        
        return jsonify({'transcription': transcription})
    
    except Exception as e:
        app.logger.error(f"Error processing file: {str(e)}")
        return jsonify({'error': 'Error uploading file.'}), 500

# transcribing using baseline accuracy model
@app.route('/transcribe_baseline', methods=['POST'])
def transcribe_baseline():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'Empty file name'}), 400
        
        # Save the uploaded file to a temporary location
        file_path = 'temp_baseline.webm'  # Save as WebM
        file.save(file_path)
        
        waveform, sample_rate = loading_audio_file(file_path)
        input_values = tokenizing_waveform(waveform, sample_rate, processor=processor_baseline)
        transcription = get_transcript(input_values, processor=processor_baseline, model=model_baseline)

        os.remove(file_path)
        
        return jsonify({'transcription': transcription})
    
    except Exception as e:
        app.logger.error(f"Error processing file: {str(e)}")
        return jsonify({'error': 'Error uploading file.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
