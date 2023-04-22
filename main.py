from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import io, base64
from PIL import Image 
from deepface import DeepFace
import json
import requests
import os
from datetime import datetime, date

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
def analyse():
	try:

		res = requests.get("http://localhost:1337/api/reoprt-firs")
		res = res.json()
		femaleCount = 0
		maleCount = 0
		years={}
		city={}
		found = 0
		notFound = 0
		today = date.today()
		thisYear = today.strftime("%Y")	
		montlyStats = {}
		result={}
		montlyStatsList = []
		yearList=[]
		for i in res["data"]:
			# found not found stats
			
			if(i["attributes"]["found"] ):
				found = found +1
			else:
				notFound = notFound + 1

			# gender stats
			if(i["attributes"]["gender"] == "Female"):
				femaleCount = femaleCount +1
			else:
				maleCount = maleCount + 1
			
			# yearly stats
			year = i["attributes"]["dom"][:4]
			
			if not year in years:
				years[year] = {"Found" : 0, "Not Found" : 0}
			if(i["attributes"]["found"]):
				years[year]["Found"] +=1
			else:
				years[year]["Not Found"] +=1

			#city Stats
			place = i["attributes"]["pom"]
			
			if not place in city:
				city[place] = 1
			else:
				city[place] += 1

			
			#montly Stats
			if(year == thisYear):
				checkmonth = i["attributes"]["dom"][5:7]			
				datetime_object = datetime.strptime(checkmonth, "%m")
				month_name = datetime_object.strftime("%b")
				month_name = month_name +" " + year
				if not month_name in montlyStats:
					montlyStats[month_name] = {"Found" : 0, "Not Found" : 0}
				if(i["attributes"]["found"]):
					montlyStats[month_name]["Found"] +=1
				else:
					montlyStats[month_name]["Not Found"] +=1
		
		#monthy
		for month_name ,month_stats in montlyStats.items():
			month_stats["Month"] = month_name
			montlyStatsList.append(month_stats)
		
		montlyStatsList.sort(key = lambda x: datetime.strptime(x["Month"].split(" ")[0], '%b').month)
		
		#yearly
		for year ,year_stats in years.items():
			year_stats["Year"] = year
			yearList.append(year_stats)		
		yearList.sort(key = lambda x: x["Year"])

		regionAnalytics = [{"Region" : cityName, "Count" : count} for cityName,count in city.items()]

		result={
			"genderAnalytics":{
				"female":femaleCount, 
				"male":maleCount
			},
			"regionalAnalytics": regionAnalytics,
			"yearlyAnalytics": yearList,
			"analytics": {
				"found":found, 
				"notFound":notFound
			},
			"monthlyStatistics": montlyStatsList
		}
		
		return {"data": result}

	except Exception as e:
		print(e)
		return {"data": {}, "error": e}