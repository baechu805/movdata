import requests
import os
import json
import time
from tqdm import tqdm

API_KEY = os.getenv("MOVIE_API_KEY")

def save_json(data, file_path):
    # 파일 저장 경로 생성
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def req(url):
    r = requests.get(url)
    j = r.json()
    return j

def save_movies(year):
    home_path = os.path.expanduser("~")
    file_path = f'{home_path}/data/movies/year={year}/airflow_data.json'

    # API URL 설정
    url_base = f"https://kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key={API_KEY}&openStartDt={year}&openEndDt={year}"

    print(f"{year}년 영화정보를 불러옵니다.")

    # 파일이 이미 존재하면 API 호출을 멈추고 종료
    if os.path.exists(file_path):
        print(f"데이터가 이미 존재합니다: {file_path}")
        return True

    all_data = []
    for page in tqdm(range(1, 11)):  # 페이지 범위는 1부터 10까지
        time.sleep(0.1)  # API 요청 간 대기 시간
        r = req(url_base + f"&curPage={page}")
        d = r['movieListResult']['movieList']
        all_data.extend(d)

    save_json(all_data, file_path)
    return True

