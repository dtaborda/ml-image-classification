import json
import os
import time

import numpy as np
import redis
import settings
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import decode_predictions, preprocess_input
from tensorflow.keras.preprocessing import image

# Connect to Redis and assign to variable `db`
# Make use of settings.py module to get Redis settings like host, port, etc.
db = redis.Redis(
    host=settings.REDIS_IP,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB_ID
)

# Load your ML model and assign to variable `model`
# See https://drive.google.com/file/d/1ADuBSE4z2ZVIdn66YDSwxKv-58U7WEOn/view?usp=sharing
# for more information about how to use this model.
model = ResNet50(weights='imagenet')


def predict(image_name):
    """
    Load image from the corresponding folder based on the image name
    received, then, run our ML model to get predictions.

    Parameters
    ----------
    image_name : str
        Image filename.

    Returns
    -------
    class_name, pred_probability : tuple(str, float)
        Model predicted class as a string and the corresponding confidence
        score as a number.
    """
    # Build the full path to the image
    img_path = os.path.join(settings.UPLOAD_FOLDER, image_name)
    
    # Load image with target size for ResNet50 (224x224)
    img = image.load_img(img_path, target_size=(224, 224))
    
    # Convert image to numpy array
    x = image.img_to_array(img)
    
    # Expand dimensions to match model input (add batch dimension)
    x = np.expand_dims(x, axis=0)
    
    # Apply ResNet50-specific preprocessing
    x = preprocess_input(x)
    
    # Get predictions from the model
    preds = model.predict(x)
    
    # Decode predictions to get human-readable class names (top 1 prediction)
    decoded = decode_predictions(preds, top=1)[0][0]
    
    # Extract class name and prediction probability
    _, class_name, pred_probability = decoded
    
    # Convert probability to float and round to 4 decimal places
    pred_probability = round(float(pred_probability), 4)

    return class_name, pred_probability


def classify_process():
    """
    Loop indefinitely asking Redis for new jobs.
    When a new job arrives, takes it from the Redis queue, uses the loaded ML
    model to get predictions and stores the results back in Redis using
    the original job ID so other services can see it was processed and access
    the results.

    Load image from the corresponding folder based on the image name
    received, then, run our ML model to get predictions.
    """
    while True:
        # Inside this loop you should add the code to:
        #   1. Take a new job from Redis
        #   2. Run your ML model on the given data
        #   3. Store model prediction in a dict with the following shape:
        #      {
        #         "prediction": str,
        #         "score": float,
        #      }
        #   4. Store the results on Redis using the original job ID as the key
        #      so the API can match the results it gets to the original job
        #      sent
        # Hint: You should be able to successfully implement the communication
        #       code with Redis making use of functions `brpop()` and `set()`.
        
        # Take a new job from Redis (blocking right pop - waits for new jobs)
        queue_name, job_data = db.brpop(settings.REDIS_QUEUE)

        # Decode the JSON data for the given job
        job = json.loads(job_data)

        # Important! Get and keep the original job ID
        job_id = job["id"]
        image_name = job["image_name"]

        # Run the loaded ml model (use the predict() function)
        class_name, score = predict(image_name)

        # Prepare a new JSON with the results
        output = {"prediction": class_name, "score": score}

        # Convert output dict to JSON string
        output_json = json.dumps(output)

        # Store the job results on Redis using the original
        # job ID as the key
        db.set(job_id, output_json)

        # Sleep for a bit
        time.sleep(settings.SERVER_SLEEP)


if __name__ == "__main__":
    # Now launch process
    print("Launching ML service...")
    classify_process()
