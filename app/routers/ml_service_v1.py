# file: app/routers/ml_service_v1.py


from typing import List
import torch
import torchaudio
import io
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime

from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, File, UploadFile
from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User, ServiceCall
from ..schemas import PredictionInput, PredictionOutput, ServiceCallCreate, SegmentPrediction
from ..ml_models.v1 import PlaceholderMLModelV1
from .auth import get_current_user

router = APIRouter(prefix='/mlservice/v1', tags=['mlservice/v1'])

placeholder_ml_model_v1 = PlaceholderMLModelV1()


############### DEPENDENCIES ###############
async def get_ml_model_v1(model: PlaceholderMLModelV1 = Depends()) -> PlaceholderMLModelV1:
    """Dependency to lazy-load a ML model"""
    if not model.loaded:
        await model.load_model()
    return model


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
ml_model_v1_dependency = Annotated[PlaceholderMLModelV1, Depends(get_ml_model_v1)]




############### ROUTES ###############
@router.get('/healthcheck', status_code=status.HTTP_200_OK)
async def check_service_v1(user: user_dependency, db: db_dependency) -> dict:
    if user is None or not user.get('has_access_v1'):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return {'status': 'healthy'}


@router.post('/predict', status_code=status.HTTP_200_OK)
async def make_prediction_v1(
    user: user_dependency, 
    db: db_dependency, 
    model: ml_model_v1_dependency,
    prediction_input: PredictionInput = Depends(PredictionInput.as_form), 
):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is None")
    
    if not user.get('has_access_v1'):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User does not have access to the service")
    
    ################## AUDIO PROCESSING ##################
    # Create a file-like object from the uploaded file data
    audio_data = io.BytesIO(prediction_input.audio_file)
    
    # Process the audio data here, before calling model.predict
    waveform, sample_rate = torchaudio.load(audio_data)
    if sample_rate != 16000:  # Adjust the sample rate to the model's requirements
        waveform = torchaudio.transforms.Resample(sample_rate, 16000)(waveform)
    target_length = 80000  # Adjust the target length to the model requirements
    if waveform.shape[1] < target_length:
        waveform = torch.nn.functional.pad(waveform, (0, target_length - waveform.shape[1]))
    elif waveform.shape[1] > target_length:
        waveform = waveform[:, :target_length]
    
    
    ####################### PREDICTION / DB FLOW ###################
    request_time = datetime.now()
    prediction_output = await model.predict(waveform)  # Adjusted to pass preprocessed waveform
    completion_time = datetime.now()
    duration = (completion_time - request_time).total_seconds()
    
    service_call_data = ServiceCallCreate(
        service_version='v1',
        success=True,
        owner_id=user['id'],
        request_time=request_time,
        completion_time=completion_time,
        duration=duration
    )
    service_call = ServiceCall(**service_call_data.dict())
    db.add(service_call)
    db.commit()
    db.refresh(service_call)
    
    return prediction_output


'''
@router.post('/predict', status_code=status.HTTP_200_OK)
async def make_prediction_v1(
    user: user_dependency, 
    db: db_dependency, 
    model: ml_model_v1_dependency,
    prediction_input: PredictionInput = Depends(PredictionInput.as_form), 
):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is None")
    
    if not user.get('has_access_v1'):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User does not have access to the service")
    
    request_time = datetime.now()
    prediction_output = await model.predict(prediction_input)
    completion_time = datetime.now()
    duration = (completion_time - request_time).total_seconds()
    
    service_call_data = ServiceCallCreate(
        service_version='v1',
        success=True,
        owner_id=user['id'],
        request_time=request_time,
        completion_time=completion_time,
        duration=duration
    )
    service_call = ServiceCall(**service_call_data.dict())
    db.add(service_call)
    db.commit()
    db.refresh(service_call)
    
    return prediction_output
'''