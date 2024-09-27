# Ground Flip - Geocoding Server
그라운드 플립의 geocoding 서버이다. 주소를 알고 싶은 좌표를 요청으로 보내면 해당 좌표가 속한 시군구의 이름과 id 를 반환한다.

간단하게 python 으로 개발 하였고 flask 를 사용하여 서버로 띄울 수 있게 구현하였다.

# 실행시키는 방법
이 깃 레파지토리에 시군구 분류에 필요한 대한민국 시군구 shp 파일이 포함되어있기 때문에 이 레파지토리만 다운로드 하면 바로 사용할 수 있다.
1. 레파지토리 클론
```
git clone https://github.com/SWM-M3PRO/GroundFlip-GeoCodingServer.git
```

2. docker image 빌드
```
docker build -t geocoding-server .
```

3. docker 실행
```
docker run -d -p 3030:3030 geocoding-server
```
# API 문서
이 API는 위도와 경도 좌표를 기반으로 해당 좌표가 속한 시군구 정보를 조회할 수 있는 기능을 제공합니다. GET 요청으로 좌표를 보내면 시군구 이름과 ID를 반환합니다.
### Base URL
`http://<서버-IP>:3030`

`<서버-IP>`를 실제 Flask 애플리케이션이 실행 중인 IP 주소 또는 도메인으로 대체하세요.

## 엔드포인트

### 1. 시군구 정보 조회

- **엔드포인트:** `/find_district`
- **메서드:** `GET`
- **설명:** 주어진 위도와 경도 좌표에 해당하는 시군구의 이름과 ID를 반환합니다.

#### 요청 파라미터

| 파라미터 | 타입   | 필수 여부 | 설명                                |
|----------|--------|-----------|-------------------------------------|
| `lon`    | float  | 필수      | 조회할 위치의 경도 (Longitude)      |
| `lat`    | float  | 필수      | 조회할 위치의 위도 (Latitude)       |

#### 성공 응답

```json
{
  "region": "서울특별시 중구",
  "region_id": 101
}
```

- region: 주어진 좌표가 속하는 시군구 이름
- region_id: 해당 시군구의 고유 ID
- 대한민국 시군구에 속하지 않는 좌표의 경우 region 과  region_id 모두 null 로 반환
#### 오류 응답
```json
{
  "error": "해당 좌표는 시군구에 속하지 않습니다."
}
```
- error: 좌표 형식이 올바르지 않거나 오류인 경우

#### 요청 예시
```bash
curl -X GET "http://<서버-IP>:3030/find_district?lon=126.9780&lat=37.5665"
```

# 주의점
- shp 파일이 포함되어있기 때문에 레파지토리의 용량이 꽤 크다.
- 도커 이미지 파일의 크기가 744.18 MB 이다.
- 이미지 빌드시 많은 라이브러리를 다운하기 때문에 시간이 꽤 걸릴 수 있다.