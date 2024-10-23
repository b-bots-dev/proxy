from flask import Flask, Response, request
import requests

app = Flask(__name__)


@app.route('/proxy_video')
def proxy_video():
    video_url = request.args.get('url')

    # Nagłówki, które przeglądarka używa do pobierania pliku
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                      " Chrome/130.0.0.0 Safari/537.36",
    }

    # Pobranie pliku z zewnętrznego serwera
    response = requests.get(video_url, headers=headers, stream=True)

    # Jeśli status odpowiedzi jest 200 OK, przekazujemy strumień danych dalej
    if response.status_code == 200:
        return Response(response.iter_content(chunk_size=1024), content_type=response.headers['Content-Type'])
    else:
        return f"Error {response.status_code}: Could not fetch the video", response.status_code


if __name__ == '__main__':
    app.run(debug=True)
