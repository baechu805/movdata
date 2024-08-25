import requests
import os
import json
import time
from tqdm import tqdm

API_KEY = os.getenv('MOVIE_API_KEY')

def save_json(data, file_path):
    # 파일저장 경로 MKDIR
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def req(url):
    r = requests.get(url).json()
    return r

def read_movies(year):
    home_path = os.path.expanduser("~")
    file_path = f'{home_path}/data/movies/year={year}/data.json'

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return data

def save_movies_Info(year, sleep_time=1):
    home_path = os.path.expanduser("~")
    file_path = f'{home_path}/data/movies/year={year}/dataInfo.json'

    movies = read_movies(year)

    movieCd = []

    for mv in movies:
        movieCd.append(mv['movieCd'])

    if os.path.exists(file_path):
        print(f"데이터가 이미 존재합니다: {file_path}")
        print("영화 상세정보 불러오기를 종료합니다.")
        return True

    url_base = f"https://kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?key={API_KEY}&movieCd="
    print(f"{year}년 영화 상세정보를 불러옵니다.")
    all_data = []

    for i in tqdm(movieCd):
        time.sleep(sleep_time)
        r = req(url_base + i)

        if 'movieInfoResult' in r:
            d = r['movieInfoResult']['movieInfo']
            all_data.append(d)
        else:
            print(f"Error: 'movieInfoResult' not found for movieCd {i}. Skipping this entry.")

    save_json(all_data, file_path)
    print("영화상세정보 불러오기를 종료합니다.")
    return True

for date in range(2015, 2022):
    save_movies_Info(year=date, sleep_time=0.1)

