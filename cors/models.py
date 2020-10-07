from django.http import HttpResponse

class CORS(HttpResponse):

    def allow_all(self, auth = "", status_code = 200):

        self["Access-Control-Allow-Origin"] = "*"
        self["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        self["Access-Control-Max-Age"] = "1000"
        self["Access-Control-Allow-Headers"] = "*"
        self["Authorization"] = "Token-" + str(auth)
        self["Content-Type"] = "application/json"

        self.status_code = status_code

        return self