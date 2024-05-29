import requests

url = 'http://localhost:5000/predict_api'
r = requests.post(url,json={"sr" : 1,"rr" : 2,"bt" : 3,"lm" : 4,"bo" : 5
                            ,"rem" : 6,"sh" : 7,"hr": 8})

print(r.json())