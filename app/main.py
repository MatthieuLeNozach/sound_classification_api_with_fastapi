# file: app/main.py

import os
from dotenv import load_dotenv
from fastapi import FastAPI


from .ml_models.v1 import PlaceholderMLModelV1
from .models import Base
from .database import engine, SessionLocal
from .routers import auth, admin, users, ml_service_v1 
from .devtools import create_superuser, remove_superuser

load_dotenv(override=True) # loads environment variables from the .environment folder

############## ML MODELS ###############
placeholder_ml_model_v1 = PlaceholderMLModelV1()

############### API ###############
app = FastAPI()
app.include_router(auth.router) 
app.include_router(admin.router)
app.include_router(users.router)
app.include_router(ml_service_v1.router)


############### DATABASE ###############
Base.metadata.create_all(bind=engine)


############### LIFESPAN ###############
@app.on_event('startup')
async def startup_event():
    if os.getenv('CREATE_SUPERUSER', 'false').lower() == 'true':
        db = SessionLocal()
        create_superuser(db)
        db.close()
                
    await ml_service_v1.placeholder_ml_model_v1.load_model()
        
        
        
@app.on_event('shutdown')
async def shutdown_event():
    if os.getenv('CREATE_SUPERUSER', 'false').lower() == 'true':
        db = SessionLocal()
        remove_superuser(db)
        db.close()


############### ROUTES ###############
@app.get('/healthcheck')
def get_healthcheck():
    return {'status': 'healthy'}

