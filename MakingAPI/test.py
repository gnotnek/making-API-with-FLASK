import requests as req

BASE ="http://127.0.0.1:5000/"
data = [
    {"likes":10,"name" : "gnotnek1", "views":1060},
    {"likes":50,"name" : "gnotnek2", "views":10070},
    {"likes":90,"name" : "gnotnek3", "views":100600},
    {"likes":100,"name" : "gnotnek4", "views":107890}]
# for i in range(len(data)):
#     response = req.put(BASE + "video/" + str(i), data[i])
#     print(response.json())
# input()
# response = req.delete(BASE + "video/2")
# print(response)
# input()
# response = req.get(BASE + "video/8")
response = req.delete(BASE+'video/2')
print(response)