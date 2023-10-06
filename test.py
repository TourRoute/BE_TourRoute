from haversine import haversine
from pymongo import MongoClient
from src.config import settings
import random
import re


def navigation_algorithm(response_body, request_body):
    short_distance_info = {}
    short_distance = float('inf')

    for x in range(len(request_body)):
        s_point = (float(response_body[-1]["latitude"]), float(response_body[-1]["longitude"]))
        destination = (float(request_body[x]["latitude"]), float(request_body[x]["longitude"]))
        distance = haversine(s_point, destination)
        if short_distance > distance:
            short_distance = distance
            short_distance_info = request_body[x]

    response_body.append(short_distance_info)
    request_body.remove(short_distance_info)

    return response_body, request_body


'''
tourspot -> ok
restaurant -> ok
park -> ok
mountain -> ok
museum -> ok
'''

result_list = [
  [
    {
      "도시": "대구",
      "시설명": "대구섬유박물관",
      "소재지도로명주소": "대구광역시 동구 팔공로 227",
      "소재지지번주소": "",
      "평일관람시작시각": "9:00",
      "평일관람종료시각": "18:00",
      "공휴일관람시작시각": "9:00",
      "공휴일관람종료시각": "18:00",
      "휴관정보": "월(단, 월요일이 공휴일인 경우 당일은 개관하고 그 다음 첫번째 평일에 휴관)",
      "어른관람료": "0",
      "청소년관람료": "0",
      "어린이관람료": "0",
      "관리기관전화번호": "053-980-1004",
      "category": "museum",
      "latitude": "35.9190995",
      "longitude": "128.640295"
    },
    {
      "store_name": "대덕식당",
      "store_address": "대구광역시 남구 앞산순환로 443",
      "picture_url": "https://img.siksinhot.com/place/1675994014832232.jpg?w=560&h=448&c=X",
      "menu": {
        "선짓국": "7,000 원",
        "갈비탕": "8,000 원",
        "옛날간장찜닭": "25,000 원"
      },
      "lat_lng": "",
      "latitude": "35.831079",
      "longitude": "128.573586",
      "category": "restaurant"
    },
    {
      "도시": "대구",
      "관광지명": "운암지수변공원",
      "소재지도로명주소": "",
      "소재지지번주소": "대구광역시 북구 구암동 349",
      "관광지소개": "대구광역시 북구 8경사진찍기좋은명소",
      "관리기관전화번호": "053-665-2344",
      "category": "tourspot",
      "latitude": "35.93241418",
      "longitude": "128.5674979"
    }
  ],
  [
    {
      "도시": "대구",
      "시설명": "대구교육박물관",
      "소재지도로명주소": "대구광역시 북구 대동로1길 40",
      "소재지지번주소": "대구광역시 북구 산격동 1285",
      "평일관람시작시각": "9:00",
      "평일관람종료시각": "18:00",
      "공휴일관람시작시각": "9:00",
      "공휴일관람종료시각": "18:00",
      "휴관정보": "월+1월 1일+설 당일+추석 당일",
      "어른관람료": "0",
      "청소년관람료": "0",
      "어린이관람료": "0",
      "관리기관전화번호": "053-231-1790",
      "category": "museum",
      "latitude": "35.89736822",
      "longitude": "128.6118404"
    },
    {
      "store_name": "고씨네 대구경북대본점",
      "store_address": "대구광역시 북구 대학로23길 26",
      "picture_url": "https://img.siksinhot.com/place/1562828534966576.jpg?w=560&h=448&c=Y",
      "menu": {
        "돈까스카레": "7,000 원",
        "스페셜카레": "9,500 원",
        "떡갈비카레": "7,000 원"
      },
      "lat_lng": "",
      "latitude": "35.893531",
      "longitude": "128.6095886",
      "category": "restaurant"
    },
    {
      "도시": "대구",
      "관광지명": "함지공원",
      "소재지도로명주소": "대구광역시 북구 동암로38길 9",
      "소재지지번주소": "대구광역시 북구 구암동 775-6",
      "관광지소개": "대구광역시 북구 8경사진찍기좋은명소",
      "관리기관전화번호": "053-665-2344",
      "category": "tourspot",
      "latitude": "35.9424608",
      "longitude": "128.570482"
    }
  ],
  [
    {
      "도시": "대구",
      "시설명": "방짜유기박물관",
      "소재지도로명주소": "대구광역시 동구 도장길 29",
      "소재지지번주소": "",
      "평일관람시작시각": "10:00",
      "평일관람종료시각": "18:00",
      "공휴일관람시작시각": "10:00",
      "공휴일관람종료시각": "19:00",
      "휴관정보": "월(공휴일인 경우 다음 평일)+1월 1일+설 당일+추석 당일",
      "어른관람료": "0",
      "청소년관람료": "0",
      "어린이관람료": "0",
      "관리기관전화번호": "053-606-6172",
      "category": "museum",
      "latitude": "35.96545542",
      "longitude": "128.7013639"
    },
    {
      "store_name": "화요옥(롯데백화점 대구점 10층)",
      "store_address": "대구광역시 북구 태평로 161",
      "picture_url": "https://img.siksinhot.com/place/1610586808850138.jpg?w=560&h=448&c=Y",
      "menu": {
        "불고기만두전골(작은꽃)": "27,000 원",
        "주꾸미만두전골(작은꽃)": "27,000 원",
        "얼큰만두전골(작은꽃)": "22,000 원"
      },
      "lat_lng": "",
      "latitude": "35.8758026",
      "longitude": "128.5959092",
      "category": "restaurant"
    },
    {
      "도시": "대구",
      "관광지명": "금호강하중도",
      "소재지도로명주소": "",
      "소재지지번주소": "대구광역시 북구 노곡동 673",
      "관광지소개": "대구광역시 북구 8경사진찍기좋은명소",
      "관리기관전화번호": "053-665-2344",
      "category": "tourspot",
      "latitude": "35.90019471",
      "longitude": "128.5595886"
    }
  ],
  [
    {
      "도시": "대구",
      "시설명": "대구향토역사관",
      "소재지도로명주소": "대구광역시 중구 달성공원로 35",
      "소재지지번주소": "",
      "평일관람시작시각": "9:00",
      "평일관람종료시각": "18:00",
      "공휴일관람시작시각": "9:00",
      "공휴일관람종료시각": "18:00",
      "휴관정보": "월(단, 월요일이 공휴일인 경우 당일은 개관하고 그 다음 첫번째 평일에 휴관)+설날+추석",
      "어른관람료": "0",
      "청소년관람료": "0",
      "어린이관람료": "0",
      "관리기관전화번호": "053-606-6425",
      "category": "museum",
      "latitude": "35.87339859",
      "longitude": "128.5759183"
    },
    {
      "store_name": "대구막창",
      "store_address": "대구 중구 달구벌대로 2232-6",
      "picture_url": "https://img.siksinhot.com/place/1531206927115269.jpg?w=560&h=448&c=Y",
      "menu": {},
      "lat_lng": "",
      "latitude": "35.861853",
      "longitude": "128.6069228",
      "category": "restaurant"
    },
    {
      "도시": "대구",
      "관광지명": "달성토성마을",
      "소재지도로명주소": "대구광역시 서구 국채보상로 83길 21 (비산동) 일대",
      "소재지지번주소": "대구광역시 서구 비산동 404-5",
      "관광지소개": "집안에 있는 화분을 골목으로 꺼내놓으며 시작된 골목정원",
      "관리기관전화번호": "053-663-2181",
      "category": "tourspot",
      "latitude": "35.87331563",
      "longitude": "128.5753765"
    }
  ],
  [
    {
      "도시": "대구",
      "시설명": "대구약령시한의약박물관",
      "소재지도로명주소": "대구광역시 중구 달구벌대로415길 49",
      "소재지지번주소": "",
      "평일관람시작시각": "9:00",
      "평일관람종료시각": "18:00",
      "공휴일관람시작시각": "9:00",
      "공휴일관람종료시각": "18:00",
      "휴관정보": "월(단, 월요일이 공휴일인 경우 당일은 개관하고 그 다음 첫번째 평일에 휴관)",
      "어른관람료": "0",
      "청소년관람료": "0",
      "어린이관람료": "0",
      "관리기관전화번호": "053-253-4729",
      "category": "museum",
      "latitude": "35.868522",
      "longitude": "128.5899085"
    },
    {
      "store_name": "홍익돈까스 대구반야월점",
      "store_address": "대구 동구 안심로 240",
      "picture_url": "https://img.siksinhot.com/place/1419367839463470.jpg?w=560&h=448&c=Y",
      "menu": {
        "돈까스": "8,900 원"
      },
      "lat_lng": "",
      "latitude": "35.8659085",
      "longitude": "128.7107905",
      "category": "restaurant"
    },
    {
      "도시": "대구",
      "관광지명": "침산정",
      "소재지도로명주소": "대구광역시 북구 침산남로9길 118",
      "소재지지번주소": "대구광역시 북구 침산동 1168-3",
      "관광지소개": "대구광역시 북구 8경사진찍기좋은명소",
      "관리기관전화번호": "053-665-2344",
      "category": "tourspot",
      "latitude": "35.897221",
      "longitude": "128.5848591"
    }
  ]
]

data_list = []

theme = "museum"
period = 5

for x in range(period):
    data_list += result_list[x]

if theme == "museum":

    other_list = []
    restaurant_list = []

    for x in range(len(data_list)):
        if data_list[x]["category"] == "restaurant":
            restaurant_list.append(data_list[x])
        else:
            other_list.append(data_list[x])

    response_body = [other_list[0]]
    other_list = other_list[1:]

    while 1:

        if len(restaurant_list) == 1 and len(other_list) == 1:
            response_body = response_body + restaurant_list + other_list
            break

        response_body, restaurant_list = navigation_algorithm(response_body, restaurant_list)

        for x in range(2):
            response_body, other_list = navigation_algorithm(response_body, other_list)

else:

    other_list = []
    restaurant_list = []

    for x in range(len(data_list)):
        if data_list[x]["category"] == "restaurant":
            restaurant_list.append(data_list[x])
        else:
            other_list.append(data_list[x])

    response_body = [restaurant_list[0]]
    restaurant_list = restaurant_list[1:]

    while 1:

        if len(restaurant_list) == 1 and len(other_list) == 1:
            response_body = response_body + other_list + restaurant_list
            break

        response_body, other_list = navigation_algorithm(response_body, other_list)

        for x in range(2):
            response_body, restaurant_list = navigation_algorithm(response_body, restaurant_list)

response_body = [response_body[i:i+3] for i in range(0, len(response_body), 3)]

for x in response_body:
    for y in x:
        print(y)




# my_client = MongoClient("127.0.0.1:27017",  username=settings.MONGODB_USER, password=settings.MONGODB_PWD, authSource=settings.MONGODB_AUTHSOURCE,authMechanism=settings.MONGODB_AUTHMECHANISM)
#
# db = my_client["touroute"]
#
#
# a = [x for x in db["restaurant"].find({"store_address": {"$regex":'^'+"대구"}})]
#
# print(len(a))


# a = "대구광역시 달서구 호산동"
# b = "부산광역시 해운대구"

# p = re.compile(r'^대구')

# print(p.search(b))
