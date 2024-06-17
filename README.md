# ML Model API C241-PS095
This repository contains the APIs for the prediction and histories feature in our capstone project <br>

## Token
Token created and signed using JWT and contains the user_id as the payload

## Predict

### Create Disease Prediction
- Method: `POST`
- Path: `/predict/disease`
- Description: Predict the image sent by User.
- Request Header: <br>
  Key   : Authorization <br>
  Value : (token)
- Request Body: Image sent in form-data 
- Response Body:
  
  ```json
  {
    "image_url": "<image_url>",
    "prediction": "<prediction>",
    "user_id": "<user_id>"
  }
  ```

### Create Prediction
- Method: `POST`
- Path: `/predict`
- Description: Predict the image sent by User.
- Request Header: <br>
  Key   : Authorization <br>
  Value : (token)
- Request Body: Image sent in form-data 
- Response Body:
  
  ```json
  {
    "image_url": "<image_url>",
    "prediction": "<prediction>",
    "user_id": "<user_id>"
  }
  ```

## History

### Create History
- Description: Create a history for the predicted images and store it to database. 
- Additional info: Automatically executed when calling Create Prediction API.

### Get All Histories
- Method: `GET`
- Path: `/predict/histories`
- Description: Retreive all prediction histories of the logged in User.
- Request Header: <br>
  Key   : Authorization <br>
  Value : (token) 
- Response Body:
  
  ```json
  {
    "histories": [
        {
          "createdAt": "<created_at>",
          "history_id": "<history_id>",
          "image_url": "<image_url>",
          "prediction": "<prediction>",
          "userId": "<user_id>"
        },
    ...
    ]
  }
  ```

### Get History by Id
- Method: `GET`
- Path: `/predict/histories/<history_id>`
- Description: Retreive a prediction history of the logged in User.
- Request Header: <br>
  Key   : Authorization <br>
  Value : (token)
- Response Body:
  
  ```json
  {
    "history":{
        "createdAt": "<created_at>",
        "history_id": "<history_id>",
        "image_url": "<image_url>",
        "prediction": "<prediction>",
        "userId": "<user_id>"
    }
  }
  ```

### Delete All Histories
- Method: `DELETE`
- Path: `/predict/histories/`
- Description: Delete all prediction histories of the logged in User.
- Request Header: <br>
  Key   : Authorization <br>
  Value : (token)
- Response Body:
  
  ```json
  {
    "message": "All histories deleted successfully"
  }
  ```

### Delete History by Id
- Method: `DELETE`
- Path: `/predict/histories/<history_id>`
- Description: Delete a prediction history of the logged in User.
- Request Header: <br>
  Key   : Authorization <br>
  Value : (token)
- Response Body:
  
  ```json
  {
    "message": "History deleted successfully"
  }
  ```