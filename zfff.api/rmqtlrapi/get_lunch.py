import urllib.request
import urllib.parse
import json
from datetime import datetime

def get_today_lunch():
    # 자운고등학교 학교 코드 및 교육청 코드
    ATPT_OFCDC_SC_CODE = "B10" # 서울특별시교육청
    SD_SCHUL_CODE = "7010703" # 자운고등학교

    # 오늘 날짜 가져오기 (YYYYMMDD 형식)
    today = datetime.now().strftime("%Y%m%d")

    # 나이스 급식 API URL 파라미터 조합
    base_url = "https://open.neis.go.kr/hub/mealServiceDietInfo"
    params = {
        "Type": "json",
        "pIndex": 1,
        "pSize": 10,
        "ATPT_OFCDC_SC_CODE": ATPT_OFCDC_SC_CODE,
        "SD_SCHUL_CODE": SD_SCHUL_CODE,
        "MLSV_YMD": today
    }
    
    query_string = urllib.parse.urlencode(params)
    url = f"{base_url}?{query_string}"

    try:
        # 내장 모듈인 urllib.request를 사용하여 API 호출 (추가 설치 필요 없음)
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            response_data = response.read().decode('utf-8')
            data = json.loads(response_data)

        # 급식 데이터가 있는지 확인
        if "mealServiceDietInfo" in data:
            row_data = data["mealServiceDietInfo"][1]["row"][0]
            
            # 급식 메뉴 추출 및 정리
            raw_menu = row_data["DDISH_NM"]
            # <br/> 태그를 줄바꿈으로 변경
            clean_menu = raw_menu.replace("<br/>", "\n")
            
            calorie = row_data["CAL_INFO"]
            
            print(f"[{datetime.now().strftime('%Y년 %m월 %d일')} 자운고등학교 중식 메뉴]")
            print("-" * 30)
            print(clean_menu)
            print("-" * 30)
            print(f"칼로리: {calorie}")
            
        else:
            print(f"오늘은 급식 정보가 없습니다. ({data.get('RESULT', {}).get('MESSAGE', '알 수 없는 오류')})")

    except Exception as e:
        print(f"API 요청 중 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    get_today_lunch()
