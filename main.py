from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import io, base64
from PIL import Image 
from deepface import DeepFace
import json
import requests
import os

app = FastAPI()

origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class FIRPhoto(BaseModel):
	image: str
	uuid: str

class UserImage(BaseModel):
	image: str

@app.get("/")
def read_root():
    return {"Hello": "World"}
    
# @app.post("/saveFace")
# def saveFace(body: FIRPhoto):
# 	img = Image.open(io.BytesIO(base64.decodebytes(bytes(body.image.split(",")[1], "utf-8"))))
# 	img.save(f"faces/{body.uuid}.jpg")
# 	return {"res": "ho gaya"} 

@app.post("/api/validate")
def validate(body: UserImage):
	img = Image.open(io.BytesIO(base64.decodebytes(bytes(body.image.split(",")[1], "utf-8"))))
	img.save("temp.jpg")
	path = os.path.join(os.getcwd(),"faces\\representations_sface.pkl")
	if os.path.exists(path):
		os.remove(path)
	dfs = DeepFace.find(img_path = "temp.jpg"  , db_path = "faces", model_name = "SFace", distance_metric = 'cosine')
	result = json.loads(dfs[0].to_json(orient='records')) # -> list of dataframe to list of dict
	return {"data": result}

@app.get("/api/analyse")
def read_root():
	res = requests.get("http://localhost:1337/api/reoprt-firs")
	res = res.json()
	res = res["data"]
	print(len(res))
	return {"Hello": res}