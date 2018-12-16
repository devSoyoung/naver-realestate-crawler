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

# 특정 지역(시/도)의 구 코드 가져와서 address에 저장

# html = urlopen(basicURL + 'rletTypeCd=C01&tradeTypeCd=B3&hscpTypeCd=&cortarNo=4146500000&page=1')
# html = AppURLopener().open(basicURL + 'rletTypeCd=C01&tradeTypeCd=B3&hscpTypeCd=&cortarNo=4146500000&page=1')
html = requests.get(basicURL + 'rletTypeCd=C01&tradeTypeCd=B3&hscpTypeCd=&cortarNo=4146500000&page=1', headers=headers).text
bsObject = BeautifulSoup(html, "html.parser")

address = []
for addr in bsObject.body.find('select', {'title': '시/군/구'}).find_all('option'):
  curAddr = {
    'name': addr.get_text(),
    'code': addr.get('value')
  }
  address.append(curAddr)
  # print(addr.get('value'), addr.get_text())
# print(address)

# 특정 구의 매물 정보 가져오기
for addr in address:
  # url querystring 만들기
  # query = 'rletTypeCd=' + rletTypeCd[0] + '&tradeTypeCd=' + tradeTypeCd + '&cortarNo=' + addr['code'] + '&page=1'
  query = 'rletTypeCd={}&trageTypeCd={}&cortarNo={}&page={}'.format(rletTypeCd[0], tradeTypeCd, addr['code'], 1)

  # html = urlopen(basicURL + query)
  # html = AppURLopener().open(basicURL + query)
  html = requests.get(basicURL + query, headers=headers).text
  bsObject = BeautifulSoup(html, "html.parser")
  # print(bsObject)

  # 등록된 매물이 있는지 없는지 체크하고, 있으면 매물 정보 조사하기
  houseLinks = []
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
        address = house.find('p', class_='ly_tx ly_tx_v2').get_text()

        print(name, mobile, phone, presentative, address)
    print(addr['name'] + ' 지역의 업체 연락처를 저장했습니다.')
  else:
    print('등록된 매물이 없습니다.')
  
  sleep(1)


