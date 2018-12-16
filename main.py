# from urllib.request import urlopen
from urllib.request import FancyURLopener
from urllib import parse
from bs4 import BeautifulSoup
from time import sleep
import requests

# 봇 탐지 우회를 위해서 user agent 변경
class AppURLopener(FancyURLopener):
  version = 'Mozilla/5.0'

# FancyURLopener로 해결 안됨
# requests 사용해서 해결 시도
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

basicURL = 'https://land.naver.com/article/divisionInfo.nhn?'
# -- query 정보
# rletTypeCd : 매물 종류, (A01: 아파트, A02: 오피스텔, C01: 원룸)
rletTypeCd = ['A01', 'A02', 'C01']
# tradeTypeCd : 거래 종류, (B3: 단기임대)
tradeTypeCd = 'B3'
# cortarNo : 지역 코드
# page : 페이지 번호

# # 특정 지역(시/도)의 구 코드 가져와서 address에 저장
# # 현재: 경기도
# # html = urlopen(basicURL + 'rletTypeCd=C01&tradeTypeCd=B3&hscpTypeCd=&cortarNo=4146500000&page=1')
# # html = AppURLopener().open(basicURL + 'rletTypeCd=C01&tradeTypeCd=B3&hscpTypeCd=&cortarNo=4146500000&page=1')
# html = requests.get(basicURL + 'rletTypeCd=C01&tradeTypeCd=B3&hscpTypeCd=&cortarNo=4146500000&page=1', headers=headers).text
# bsObject = BeautifulSoup(html, "html.parser")

# address = []
# for addr in bsObject.body.find('select', {'title': '시/군/구'}).find_all('option'):
#   curAddr = {
#     'name': addr.get_text(),
#     'code': addr.get('value')
#   }
#   address.append(curAddr)
#   # print(addr.get('value'), addr.get_text())
# print(address)

address = [{'name': '가평군', 'code': '4182000000'}, {'name': '고양시 덕양구', 'code': '4128100000'}, {'name': '고양시 일산동구', 'code': '4128500000'}, {'name': '고양시 일산서구', 'code': '4128700000'}, {'name': '과천시', 'code': '4129000000'}, {'name': '광명시', 'code': '4121000000'}, {'name': '광주시', 'code': '4161000000'}, {'name': '구리시', 'code': '4131000000'}, {'name': '군포시', 'code': '4141000000'}, {'name': '김포시', 'code': '4157000000'}, {'name': '남양주시', 'code': '4136000000'}, {'name': '동두천시', 'code': '4125000000'}, {'name': '부천시', 'code': '4119000000'}, {'name': '성남시 분당구', 'code': '4113500000'}, {'name': '성남시 수정구', 'code': '4113100000'}, {'name': '성남시 중원구', 'code': '4113300000'}, {'name': '수원시 권선구', 'code': '4111300000'}, {'name': '수원시 영통구', 'code': '4111700000'}, {'name': '수원시 장안구', 'code': '4111100000'}, {'name': '수원시 팔달구', 'code': '4111500000'}, {'name': '시흥시', 'code': '4139000000'}, {'name': '안산시 단원구', 'code': '4127300000'}, {'name': '안산시 상록구', 'code': '4127100000'}, {'name': '안성시', 'code': '4155000000'}, {'name': '안양시 동안구', 'code': '4117300000'}, {'name': '안양시 만안구', 'code': '4117100000'}, {'name': '양주시', 'code': '4163000000'}, {'name': '양평군', 'code': '4183000000'}, {'name': '여주시', 'code': '4167000000'}, {'name': '연천군', 'code': '4180000000'}, {'name': '오산시', 'code': '4137000000'}, {'name': '용인시 기흥구', 'code': '4146300000'}, {'name': '용인시 수지구', 'code': '4146500000'}, {'name': '용인시 처인구', 'code': '4146100000'}, {'name': '의왕시', 'code': '4143000000'}, {'name': '의정부시', 'code': '4115000000'}, {'name': '이천시', 'code': '4150000000'}, {'name': '파주시', 'code': '4148000000'}, {'name': '평택시', 'code': '4122000000'}, {'name': '포천시', 'code': '4165000000'}, {'name': '하남시', 'code': '4145000000'}, {'name': '화성시', 'code': '4159000000'}]

# 특정 구의 매물 정보 가져오기
# for addr in address:
# url querystring 만들기
# query = 'rletTypeCd=' + rletTypeCd[0] + '&tradeTypeCd=' + tradeTypeCd + '&cortarNo=' + addr['code'] + '&page=1'
addr = address[41]
print('지역명: ' + addr['name'])
for itemType in rletTypeCd:
  query = 'rletTypeCd={}&tradeTypeCd={}&cortarNo={}&page={}'.format(itemType, tradeTypeCd, addr['code'], 1)

  # html = urlopen(basicURL + query)
  # html = AppURLopener().open(basicURL + query)
  html = requests.get(basicURL + query, headers=headers).text
  bsObject = BeautifulSoup(html, "html.parser")
  # print(bsObject)

  print('타입: ' + itemType)

  # 등록된 매물이 있는지 없는지 체크하고, 있으면 매물 정보 조사하기
  houseLinks = []
  results = []
  if (bsObject.find(class_='exception_none') == None):
  # if(False):
    # 특정 지역의 하우스 목록
    for link in bsObject.body.table.find_all('a'):
      if (link.text.strip() == '네이버부동산에서 보기'):
        houseLinks.append(link.get('href'))

    # 각 하우스의 중개업소 정보
    for houseLink in houseLinks:
      # html = urlopen('https://land.naver.com' + houseLink)
      # html = AppURLopener().open('https://land.naver.com' + houseLink)
      html = requests.get('https://land.naver.com' + houseLink, headers=headers).text
      houseObject = BeautifulSoup(html, "html.parser")
      houseInfo = houseObject.select('.view_info')

      for house in houseInfo:
        # companyInfo = house.select('.last')
        info = house.find('div', class_='inner inner_ly').get_text().split(' ')
        name = info[0]
        mobile = info[6]
        phone = info[1]
        presentative = info[5]
        curAddress = house.find('p', class_='ly_tx ly_tx_v2').get_text()

        # print('{},{},{},{},{},{}'.format(name, addr['name'], mobile, phone, presentative, address))
        newInfo = {
          'name': name,
          'address': addr['name'],
          'mobile': mobile,
          'phone': phone,
          'presentative': presentative,
          'realAddr': curAddress
        }

        isNewData = True
        for compAddr in results:
          if (compAddr['mobile'] == newInfo['mobile']):
            isNewData = False
            break

        if(isNewData):    
          # results.append('{},{},{},{},{},{}'.format(name, addr['name'], mobile, phone, presentative, address))
          results.append(newInfo)
        # sleep(2)
    
    for result in results:
      print('{};{};{};{};{};{}'.format(result['name'], result['address'], result['mobile'], result['phone'], result['presentative'], result['realAddr']))

  else:
    print('등록된 매물이 없습니다.')

