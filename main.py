from urllib.parse import urlencode, unquote, quote_plus
from datetime import datetime, timedelta
from urllib.request import urlopen
import xml.etree.ElementTree as ET
import urllib
import os

# 콘솔 창 지우기
os.system("cls")

# 오늘 날짜
today = (
    "{0:04d}".format(datetime.today().year)
    + "{0:02d}".format(datetime.today().month)
    + "{0:02d}".format(datetime.today().day)
)

# 어제 날짜
yesterday = (
    "{0:04d}".format((datetime.today() - timedelta(1)).year)
    + "{0:02d}".format((datetime.today() - timedelta(1)).month)
    + "{0:02d}".format((datetime.today() - timedelta(1)).day)
)

open_api_base_url = (
    "http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19InfStateJson"
)
open_api_service_key = "발급 받은 서비스키"
queryParams = "?" + urlencode(
    {
        quote_plus("ServiceKey"): open_api_service_key,
        quote_plus("numOfRows"): "1",
        quote_plus("pageNo"): "1",
        quote_plus("startCreateDt"): yesterday,
        quote_plus("endCreateDt"): today,
    }
)

request = urllib.request.Request(open_api_base_url + unquote(queryParams))
request.get_method = lambda: "GET"
response_body = str(urlopen(request).read())
response_body = response_body[2:-1]
root = ET.fromstring(response_body)

stateYear = root[1][0][0][11].text[0:4]  # 코로나 api xml 데이터 업데이트 된 기준 연
stateMonth = root[1][0][0][11].text[4:6]  # 코로나 api xml 데이터 업데이트 된 기준 월
stateDay = root[1][0][0][11].text[6:8]  # 코로나 api xml 데이터 업데이트 된 기준 일

stateHour = root[1][0][0][12].text[0:2]  # 코로나 api xml 데이터 업데이트 된 기준 시
stateMinute = root[1][0][0][12].text[3:6]  # 코로나 api xml 데이터 업데이트 된 기준 분

# 최종 출력
print(
    f"\033[92m[{stateYear}년 {stateMonth}월 {stateDay}일 {stateHour}시 {stateMinute}분 기준]\033[0m\n현재 치료중인 코로나19 확진자는 총 \033[96m{root[1][0][0][3].text}\033[0m명 입니다."
)

os.system('pause')
