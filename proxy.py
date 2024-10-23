from flask import Flask, Response, request
import requests

app = Flask(__name__)


@app.route('/')
def home():
    return 'Online'


# @app.route('/proxy_video')
# def proxy_video():
#     video_url = request.args.get('url')
#
#     # Nagłówki, które przeglądarka używa do pobierania pliku
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
#                       " Chrome/130.0.0.0 Safari/537.36",
#     }
#
#     # Pobranie pliku z zewnętrznego serwera
#     response = requests.get(video_url, headers=headers, stream=True)
#
#     # Jeśli status odpowiedzi jest 200 OK, przekazujemy strumień danych dalej
#     if response.status_code == 200:
#         return Response(response.iter_content(chunk_size=1024), content_type=response.headers['Content-Type'])
#     else:
#         return f"Error {response.status_code}: Could not fetch the video", response.status_code
#
#


@app.route('/proxy_video', methods=['GET'])
def proxy_video():
    dynamic_id = request.args.get('id')  # Pobierz dynamiczną część adresu
    url = f"https://filetransfer.io/data-package/{dynamic_id}"  # Użyj dynamicznego ID

    # Nagłówki do wysłania
    headers = {
        "accept": "*/*",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://filetransfer.io",
        "referer": url,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                      " Chrome/130.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }

    # Payload do wysłania
    data = {
        "_do": "detailForm-submit",
        "all": "1"
    }

    # Wykonanie żądania POST
    response = requests.post(url, headers=headers, data=data)

    # Sprawdzenie statusu odpowiedzi
    if response.status_code == 200:
        try:
            json_response = response.json()
            if json_response.get("applyCallback"):
                download_url = json_response["applyCallback"]["goToUrl"][0]
                print(f'dl url : {download_url}')
                # Wykonaj kolejne żądanie do pobrania pliku wideo
                video_response = requests.get(download_url, stream=True)

                # Zwróć plik wideo w odpowiedzi
                return Response(video_response.iter_content(chunk_size=8192),
                                content_type='video/mp4',
                                headers={'Content-Disposition': 'attachment; filename=video.mp4'})
            else:
                return {"error": "Nie znaleziono linku do pobrania."}, 404
        except ValueError as e:
            return {"error": f"Wystąpił błąd podczas dekodowania JSON: {e}"}, 500
    else:
        return {"error": f"Wystąpił błąd: {response.status_code}"}, response.status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
