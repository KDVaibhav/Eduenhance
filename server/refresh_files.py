import requests, json, os
from urllib import request
server = "https://eduenhance.herokuapp.com"
page = requests.get(server + '/users/get_files')
files = json.loads(page.content)['files']
school_details = json.loads(page.content)['school']

if not os.path.exists(os.getcwd() + "/een/web/static/uploads_new"):
    os.mkdir(os.getcwd() + "/een/web/static/uploads_new")
for file in files:
    f = open(os.getcwd() + "/een/web/static/uploads_new/"+file, 'wb')
    f.write(request.urlopen(server + '/static/uploads/'+file).read())
    f.close()
    print(file + " saved.")

json.dump(school_details, open(os.getcwd() + "/local/config_new.json", 'w'), indent=2)
print('config_new.json saved')