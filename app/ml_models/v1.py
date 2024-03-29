# File: ml_models/v1.py
# Machine Learning Models

from ..schemas import PredictionInput, PredictionOutput, Prediction
import os
import io
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchaudio  
from typing import List, Tuple

        
# A dictionary to decode the categories into targets
decoder = {50: 'unknown', 51: 'unknown51', 0: 'dog', 14: 'chirping_birds', 36: 'vacuum_cleaner', 19: 'thunderstorm', 30: 'door_wood_knock',34: 'can_opening', 9: 'crow', 22: 'clapping', 48: 'fireworks', 41: 'chainsaw', 47: 'airplane', 31: 'mouse_click', 17: 'pouring_water', 45: 'train', 8: 'sheep', 15: 'water_drops', 46: 'church_bells', 37: 'clock_alarm', 32: 'keyboard_typing', 16: 'wind', 25: 'footsteps', 4: 'frog', 3: 'cow', 27: 'brushing_teeth', 43: 'car_horn', 12: 'crackling_fire', 40: 'helicopter', 29: 'drinking_sipping', 10: 'rain', 7: 'insects', 26: 'laughing', 6: 'hen', 44: 'engine', 23: 'breathing', 20: 'crying_baby', 49: 'hand_saw', 24: 'coughing', 39: 'glass_breaking', 28: 'snoring', 18: 'toilet_flush', 2: 'pig', 35: 'washing_machine', 38: 'clock_tick', 21: 'sneezing', 1: 'rooster', 11: 'sea_waves', 42: 'siren', 5: 'cat', 33: 'door_wood_creaks', 13: 'crickets'}

# A dictionary to encode the categories into targets
encoder = {'unknown51': 51, 'unknown': 51, 'dog': 0, 'chirping_birds': 14, 'vacuum_cleaner': 36, 'thunderstorm': 19, 'door_wood_knock': 30, 'can_opening': 34, 'crow': 9, 'clapping': 22, 'fireworks': 48, 'chainsaw': 41, 'airplane': 47, 'mouse_click': 31, 'pouring_water': 17, 'train': 45, 'sheep': 8, 'water_drops': 15, 'church_bells': 46, 'clock_alarm': 37, 'keyboard_typing': 32, 'wind': 16, 'footsteps': 25, 'frog': 4, 'cow': 3, 'brushing_teeth': 27, 'car_horn': 43, 'crackling_fire': 12, 'helicopter': 40, 'drinking_sipping': 29, 'rain': 10, 'insects': 7, 'laughing': 26, 'hen': 6, 'engine': 44, 'breathing': 23, 'crying_baby': 20, 'hand_saw': 49, 'coughing': 24, 'glass_breaking': 39, 'snoring': 28, 'toilet_flush': 18, 'pig': 2, 'washing_machine': 35, 'clock_tick': 38, 'sneezing': 21, 'rooster': 1, 'sea_waves': 11, 'siren': 42, 'cat': 5, 'door_wood_creaks': 33, 'crickets': 13}


class Net(nn.Module):
    
    # Defining the Constructor
    def __init__(self, num_classes=50):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=16, kernel_size=(1,8), stride=(1,1), padding="same")
        self.bn1 = nn.BatchNorm2d(16)
        self.conv2 = nn.Conv2d(in_channels=16, out_channels=16, kernel_size=(1,8), stride=(1,1), padding="same")
        self.bn2 = nn.BatchNorm2d(16)
        
        self.pool_1 = nn.MaxPool2d(kernel_size=(1,128), stride = (1,128), padding=0) 
        
        self.conv3 = nn.Conv2d(in_channels=1, out_channels=32, kernel_size=(3,3), stride=(1,1), padding=1)
        self.bn3 = nn.BatchNorm2d(32)
        self.conv4 = nn.Conv2d(in_channels=32, out_channels=32, kernel_size=(3,3), stride=(1,1), padding=1)
        self.bn4 = nn.BatchNorm2d(32)
        
        self.pool_2 = nn.MaxPool2d(kernel_size=4, padding=0) 
            
        self.conv5 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=(3,3), stride=(2,2), padding=2)
        self.bn5 = nn.BatchNorm2d(64)
        self.conv6 = nn.Conv2d(in_channels=64, out_channels=64, kernel_size=(3,3), stride=(2,2), padding=1)
        self.bn6 = nn.BatchNorm2d(64)
        
        self.pool_3 = nn.MaxPool2d(kernel_size=2, padding=0) 
        
        self.conv7 = nn.Conv2d(in_channels=64, out_channels=128, kernel_size=(3,3), stride=(2,2), padding=1)
        self.bn7 = nn.BatchNorm2d(128)
        self.conv8 = nn.Conv2d(in_channels=128, out_channels=128, kernel_size=(3,3), stride=(2,2), padding=1)
        self.bn8 = nn.BatchNorm2d(128)
        
        self.pool_4 = nn.MaxPool2d(kernel_size=(1,2), padding=0) 
        
        self.dense = nn.Linear(in_features= 256, out_features=num_classes)
        # Define proportion or neurons to dropout
        self.dropout = nn.Dropout(0.2)   

    def forward(self, x):
        x = x.unsqueeze(1).view(-1, 1, 1, 80000)
        x = F.relu(self.bn1(self.conv1(x)))
        x = self.dropout(x)
        x = F.relu(self.bn2(self.conv2(x)))
        x = self.pool_1(x)
        x = x.view((-1,1,16, 625))
        x = F.relu(self.bn3(self.conv3(x)))
        x = self.dropout(x)
        x = F.relu(self.bn4(self.conv4(x)))
        x = self.pool_2(x)
        x = F.relu(self.bn5(self.conv5(x)))
        x = self.dropout(x)
        x = F.relu(self.bn6(self.conv6(x)))
        x = self.pool_3(x)
        x = F.relu(self.bn7(self.conv7(x)))
        x = self.dropout(x)
        x = F.relu(self.bn8(self.conv8(x)))
        x = self.pool_4(x)
        x = x.view(x.size(0),-1)
        x = self.dense(x)
        x = self.dropout(x)
        return x





class PlaceholderMLModelV1: # SoundClassificationModel
    def __init__(self):
        self.loaded = False
        self.model = Net()

    async def load_model(self):
        self.model = Net()  # Create a new instance of the Net class
        state_dict = torch.load('app/ml_models/trained_model.pth', map_location=torch.device('cpu'))
        self.model.load_state_dict(state_dict)
        self.model.eval()  # Set the model to evaluation mode
        self.loaded = True

    async def predict(self, waveform) -> List[PredictionOutput]:
        print("Entering model.predict")  # Initial entry into the method
        
        if not self.loaded:
            print("Model not loaded, loading now...")
            await self.load_model()
            print("Model successfully loaded")
        
        print("Model is ready for making predictions")
        print(f"Waveform shape: {waveform.shape}")
        
        print("Making prediction")
        prediction = self.model(waveform)
        print(f"Raw prediction output: {prediction}") 
        
        # Assuming the prediction tensor shape is [batch_size, num_classes] and we want the predicted class index for each item in the batch
        predicted_indices = torch.argmax(prediction, dim=1)
        print(f"Predicted indices: {predicted_indices}")
        
        prediction_outputs = []  # This will hold Prediction objects, not PredictionOutput objects
        for idx in predicted_indices:
            predicted_index = idx.item()
            if predicted_index >= len(decoder):
                print(f"Error: Predicted index {predicted_index} is out of bounds. Decoder size: {len(decoder)}")
                predicted_category = "Unknown"
                predicted_probability = 0.0
            else:
                predicted_category = decoder[predicted_index]
                predicted_probability = torch.softmax(prediction, dim=1)[0][predicted_index].item()
                print(f"Predicted category: {predicted_category}, Probability: {predicted_probability}")
            
            # Create a Prediction object for each prediction and add it to the list
            prediction_outputs.append(Prediction(category=predicted_category, probability=predicted_probability))

        # Wrap the list of Prediction objects into a PredictionOutput object
        final_prediction_output = PredictionOutput(predictions=prediction_outputs)

        # Return a list containing the single PredictionOutput object
        return [final_prediction_output]





''' FOR SINGLE PREDICTIONS
    async def predict(self, input: PredictionInput) -> PredictionOutput:
        if not self.loaded:
            await self.load_model()
        
        # Create a file-like object from the uploaded file data
        audio_data = io.BytesIO(input.audio_file)
        
        # Process the audio data and make a prediction
        waveform, sample_rate = torchaudio.load(audio_data)
        
        # Resample the audio to match the expected sample rate (if necessary)
        if sample_rate != 16000:  # Adjust the sample rate as per your model's requirements
            waveform = torchaudio.transforms.Resample(sample_rate, 16000)(waveform)
        
        # Pad or trim the audio to match the expected length (if necessary)
        target_length = 80000  # Adjust the target length as per your model's requirements
        if waveform.shape[1] < target_length:
            waveform = torch.nn.functional.pad(waveform, (0, target_length - waveform.shape[1]))
        elif waveform.shape[1] > target_length:
            waveform = waveform[:, :target_length]
        
        prediction = self.model(waveform)
        
        predicted_index = torch.argmax(prediction).item()
        predicted_category = decoder[predicted_index]
        predicted_probability = torch.softmax(prediction, dim=1)[0][predicted_index].item()
        
        return PredictionOutput(category=predicted_category, probability=predicted_probability)
'''         
