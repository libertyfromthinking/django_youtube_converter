# django_youtube_converter

https://freethinking.herokuapp.com/
유튜브 영상과 재생목록을 mp4등 각각의 포맷의 동영상으로 스트리밍하는 googlevideo 사이트로 연결해줍니다. 

## 설치방법(우분투 18.04 기준)
가상환경을 설치합니다
```sh
$ python3 -m virtualenv .venv
```

가상환경을 활성화합니다
```sh
$ source .venv/bin/activate
```

git 저장소를 clone 합니다
```sh
$ git clone https://github.com/libertyfromthinking/django_youtube_converter.git 
```

프로젝트 디렉토리로 이동 후 pip를 업데이트 합니다
```sh
$ cd django_youtube_converter
$ pip install --upgrade pip 
```

requirements.txt 파일로 패키지들을 설치합니다
```sh
$ pip install -r requirements.txt
```

https://miniwebtool.com/django-secret-key-generator/
해당 사이트에서 secret_key를 생성 후 환경변수로 설정합니다
```sh
$ export YOUTUBE_SECRET_KEY='secret_key'
```

static 파일을 모아줍니다.
```sh
$ python3 manage.py collectstatic
```

django 서버를 실행합니다.
```sh
$ python3 manage.py runserver
```
