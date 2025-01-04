
#application to download youtube videos with given format
from flask import Flask, request, jsonify, send_file
import yt_dlp
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

# Fetch available formats 
@app.route('/get_formats', methods=['POST'])
def get_formats():
    data = request.json
    url = data.get('url')

    try:
        ydl_opts = {}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            format=[]

            for f in info['formats']:
                if f['ext']=='mp4':
                    x={'format_id': f['format_id'],
                    'resolution': f.get('resolution'),
                    'filesize': f.get('filesize'),
                    'audio_available': f.get('audio_channels'),
                    'pixel': f.get('format_note'),
                    'ext': f['ext']}
                    format.append(x)

        return jsonify({'status': 200,'title':info['title'], 'duration':info['duration'],'formats': format,'thumbnail':info['thumbnail']})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


#url for the given format
@app.route('/downloadurl', methods=['POST'])
def downloadurl():
    data = request.json
    url = data.get('url')
    format_id = data.get('format_id')

    try:
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'quiet': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            #download url
            download_url = next((f['url'] for f in info['formats'] if f['format_id'] == format_id), None)

        if download_url:
            return jsonify({'status': 'success', 'download_url': download_url})
        else:
            return jsonify({'status': 'error', 'message': 'Format not available.'})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


if __name__ == '__main__':
    app.run(debug=True)