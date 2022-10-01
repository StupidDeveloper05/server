import requests
import json
from datetime import datetime as dt

class Api:
    params = {
        "KEY" : "482c3bb7065a4918874c0f651899d31c",
        "Type" : "json"
    }

    schoolinfo = {}

    base_url = "https://open.neis.go.kr/hub/"
    
    def __init__(self, sub_url, params):
        self.sub_url = sub_url
        self.params = params
        
    def get_data(self):
        URL = Api.base_url + self.sub_url
        self.params.update(Api.params)
        self.params.update(Api.schoolinfo)
        print(self.params)
        response = requests.get(URL, params=self.params)

        try:
            j_response = json.loads(response.text)[self.sub_url]
            if j_response[0]["head"][0]["list_total_count"] == 1:
                return j_response[1]["row"][0]
            else:
                return j_response[1]["row"]
        except:
            print("찾는 데이터가 없습니다.")
            return response.text
        
    def get_school_info(self):
        data = self.get_data()
        try:
            Api.schoolinfo = {
                "ATPT_OFCDC_SC_CODE": data["ATPT_OFCDC_SC_CODE"],
                "SD_SCHUL_CODE": data["SD_SCHUL_CODE"]
            }
        except:
            pass
        
    def meal(self):
        data = self.get_data()
        try:
            string = "<조식>\n"+data[0]["DDISH_NM"].replace("<br/>", "\n")+"\n\n"
            string+= "<중식>\n"+data[1]["DDISH_NM"].replace("<br/>", "\n")+"\n\n"
            string += "<석식>\n" + data[2]["DDISH_NM"].replace("<br/>", "\n")
            return string
        except:
            try:
                string = data["DDISH_NM"].replace("<br/>", "\n")+"\n\n"
                print(data["MLSV_TO_YMD"])
                return string
            except:
                return "오늘은 급식이 없습니다."
        
if __name__ == "__main__":
    params = {
        "SCHUL_NM": "인천남동고"
    }
    Api("schoolInfo", params).get_school_info()
    msg=""

    params = {"MLSV_YMD": dt.now().strftime("%Y%m%d")}
    msg+=Api("mealServiceDietInfo", params).meal()
    print(msg)