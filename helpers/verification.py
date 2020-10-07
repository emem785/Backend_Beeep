import json, datetime, random
from beeep.settings import BASE_DIR
# from dateutil import parser



class Verifier:
    #MAKE SURE TO IMPORT BASE_DIR FROM SETTINGS
    FILENAME = "/verification_codes.json"
    FILE_DIR = BASE_DIR.replace("\\", "/") + FILENAME

    def __init__(self, user):
        self.username = user.username
        self.user = user

    def gen_code(self):
        code = "".join([str(random.randint(0,9)) for i in range(4)])
        new_code = {"date": datetime.datetime.now().strftime("%d-%m-%Y"), "code":code}
        self.update(new_code)
    
    def read_data(self):

        try:
            file = open(self.FILE_DIR, "r")
            json.loads(file.read())
            file.close()
        except :

            file = open(self.FILE_DIR, "w")
            file.write(json.dumps({"username":{"date":"01/10/2010", "code":"1234"}}))
            file.close()

        file = open(self.FILE_DIR, "r")
        data = json.loads(file.read())

        return data
    
    def write_data(self, data):

        file = open(self.FILE_DIR, "w")
        file.write(json.dumps(data))
        file.close()

        return True

    def update(self, value, timed  = False):

        data = self.read_data()
        data[self.user.username] = value
        self.write_data(data)

        print("Successfully cached")
        return {f"cached-{self.user.username}" : True}


    def get_code(self):

        data = self.read_data().get(self.user.username, [])

        return data

    def verify_code(self, code):

        return self.get_code()['code'] == code
