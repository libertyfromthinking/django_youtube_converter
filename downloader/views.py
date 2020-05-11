import pafy
from pytube import Playlist
from django.http import HttpResponse
from django.shortcuts import render
from django.template.defaultfilters import filesizeformat

from .forms import DownloadForm

def download_video(request):
    ''' 
    1. 폼으로 유튜브 주소를 입력받습니다.(축약주소, 모바일주소, 플레이리스트 등..)
    2. 받은 url내에 'list' 문자열이 있으면 playlist 아니면 video로 link_type 변수에 할당합니다.
    3. url 내에 'm.' 또는 'youtu.be' 문자열 포함 여부를 확인해 축약주소, 모바일페이지를 확인합니다.
    4. 입력받은 url내에서 video_id를 추출해 pafy 객체를 만듭니다.
    5. mp4 등 포맷별로 스트림값 추출 후 해당 영상을 스트리밍하는 googlevideo 사이트를 리턴해줍니다.
    '''
    form = DownloadForm(request.POST or None)
    if form.is_valid():
        video_url = form.cleaned_data.get("url")
        video_id = ''
        link_type = ''
        if 'list' in video_url:
            link_type = 'playlist'
        else:
            link_type = 'video'
        
        if 'm.' in video_url:
            video_url = video_url.replace(u'm.', u'')
        elif 'youtu.be' in video_url:
            video_id = video_url.split('/')[-1]
            video_url = 'https://www.youtube.com/watch?v=' + video_id
        
        if link_type == 'playlist':
            list_first_index = video_url.find('list=')
            video_id = video_url[list_first_index+5:list_first_index+39]
            video_url = 'https://www.youtube.com/playlist?list=' + video_id
        else:
            video_id = video_url.split('=')[-1]
            video_url = 'https://www.youtube.com/watch?v=' + video_id
        
        if len(video_id) == 11 or len(video_id) == 34:
            pass
        else:
            return HttpResponse('Enter correct url.')
        # 단일 비디오일때
        if link_type == 'video':
            video = pafy.new(video_url) # 새로운 pafy 객체 생성
            stream = video.streams  # 해당 객체의 스트림 값 추출
            video_audio_streams = []
            for s in stream:

                video_audio_streams.append({
                    'resolution': s.resolution,
                    'extension': s.extension,
                    'file_size': filesizeformat(s.get_filesize()),
                    'video_url': s.url + "&title=" + video.title,
                    'download' : s.download
                })

            stream_video = video.videostreams
            video_streams = []
            for s in stream_video:
                video_streams.append({
                    'resolution': s.resolution,
                    'extension': s.extension,
                    'file_size': filesizeformat(s.get_filesize()),
                    'video_url': s.url + "&title=" + video.title
                })

            stream_audio = video.audiostreams
            audio_streams = []
            for s in stream_audio:
                audio_streams.append({
                    'resolution': s.resolution,
                    'extension': s.extension,
                    'file_size': filesizeformat(s.get_filesize()),
                    'video_url': s.url + "&title=" + video.title
                })
            context = {
                'form': form,
                'title': video.title, 'streams': video_audio_streams,
                'stream_video': video_streams, 'stream_audio': audio_streams,
                'thumb': video.bigthumbhd, 'video' : '1'
            }       
            return render(request, 'home.html', context)
        # 플레이리스트일 때 
        elif link_type == 'playlist':
            video_audio_streams = []
            p = Playlist(video_url)
            p.populate_video_urls()
       
            for url in p.video_urls:
                video = pafy.new(url) # 새로운 pafy 객체 생성
                stream = video.streams  # 해당 객체의 스트림 값 추출
                s = stream.pop()    # 가장 고화질의 mp4파일만 추출
                video_audio_streams.append({
                    'extension': s.extension,
                    'file_size': filesizeformat(s.get_filesize()),
                    'video_url': s.url + "&title=" + video.title,
                    'title': video.title,
                })
                    
            context = {
                'form': form,
                'streams': video_audio_streams, 'playlist' : '1'
            }
            return render(request, 'home.html', context)

    return render(request, 'home.html', { 'form': form })
