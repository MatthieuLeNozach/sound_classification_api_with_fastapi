# **Sound file classification API with FastAPI**
### 

Project started from [this template](https://github.com/MatthieuLeNozach/api_basemodel_for_machine_learning_with_fastapi/tree/main)



The `PyTorch` model comes from [kaggle.com/salimhammadi07](https://www.kaggle.com/code/salimhammadi07/esc-50-environmental-sound-classification)
The training dataset is [Environmental Sound Classification 50](https://www.kaggle.com/datasets/mmoreaux/environmental-sound-classification-50)


1. [**Installation**](#installation)
2. [**Getting started**](#getting-started)



## **Installation** <a name="installation"></a>
```bash
git clone https://github.com/MatthieuLeNozach/sound_classification_api_with_fastapi
```

## **Getting started** <a name="getting-started"></a>

### **A. Securize the project**
- **Add `.env` file (may be hidden) to the `.gitignore` file** to stop exposing sensitive information
- **Modify the file**:
```bash
nano .env
...
```


### **B. Run app**

To get the api service up and running, use the Makefile commands:

```bash
# Load environment variables and start services with Docker Compose:
make up-superuser

# To stop containers, networks, and the default network bridge:
make down

```
#### **The app runs on `http://localhost:5555`**
- Access Fastapi Docs interface to test the API at `http://localhost:5555/docs`
- `superuser` argument initializes a first admin
  - username: `superuser@example.com`
  - password: `8888`





## **Access Machine Learning services**

From `http://localhost:8080/docs`:

1. **Authenticate:**
    - Click on the lock
  ![alt text](<readme/4.png>)
    - Fill username (ex: `superuser@example.com`)
    - Fill password (ex `8888`)
  ![alt text](<readme/2.png>)

1. **Send input (WAV file)**
  ![alt text](<readme/5.png>)
    - Endpoint: [localhost:5555/mlservice/v1/predict/](http://localhost:5555/mlservice/v1/predict/):

2. **Get output**
    - Sentiment:
![alt text](<readme/7.png>)



### **3.3. Tests**

A container tests the service with audio files after startup, and logs the request results in `/e2e_tests/logs`  
Example:

```bash
2024-03-29 07:31:26,135 - INFO - Upload successful: File='doberman-pincher_daniel-simion (1).wav', Size=2504020 bytes, Response='[{'predictions': [{'category': 'dog', 'probability': 0.5526291728019714}, {'category': 'dog', 'probability': 0.5526291728019714}]}]'

```

