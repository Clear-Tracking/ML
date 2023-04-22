# ML

This is repository for ML model which is used for Face Recognition.

## Installation

#### Clone the repository
```
git clone https://github.com/Clear-Tracking/ml-model.git
```

#### Navigate to the project directory
```
cd ml-model
```

#### Create virtual environment
```
python3 -m venv venv
```
#### Activate virtual environment
```
.\venv\Scripts\activate
```

#### Install dependencies
```
pip install -r requirements.txt
```

#### Run the application
```
uvicorn main:app --port 3500 --reload
```

#### Application will be running on http://localhost:3500

### Note:
```
Create folder named "faces" in the root directory of the project. And add all images from aadhar card data with name as Aadhar Card Number.
```
