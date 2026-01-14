import os
from typing import List

from app import db
from app import settings as config
from app import utils
from app.auth.jwt import get_current_user
from app.model.schema import PredictRequest, PredictResponse
from app.model.services import model_predict
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

router = APIRouter(tags=["Model"], prefix="/model")


@router.post("/predict")
async def predict(file: UploadFile, current_user=Depends(get_current_user)):
    rpse = {"success": False, "prediction": None, "score": None, "image_file_name": None}
    
    try:
        # 1. Check if file was sent and is valid
        if not file or not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No file provided"
            )
        
        # 2. Check if file is an image
        if not utils.allowed_file(file.filename):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File type is not supported."
            )
        
        # 3. Generate hash and save file
        hashed_filename = await utils.get_file_hash(file)
        file_path = os.path.join(config.UPLOAD_FOLDER, hashed_filename)
        
        # Only save if file doesn't exist (avoid duplicates)
        if not os.path.exists(file_path):
            with open(file_path, "wb") as f:
                file_content = await file.read()
                f.write(file_content)
        
        # 4. Send to model service
        prediction, score = await model_predict(hashed_filename)
        
        # 5. Build response
        rpse["success"] = True
        rpse["prediction"] = prediction
        rpse["score"] = float(score)
        rpse["image_file_name"] = hashed_filename
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing image: {str(e)}"
        )
    
    return PredictResponse(**rpse)
