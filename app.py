from flask import Flask, request, send_file, render_template, jsonify
import os
import ffmpeg

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'

# Ensure upload and output directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Serve the frontend form
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/trim-video', methods=['POST'])
def trim_video():
    try:
        # Get the video file and start/end timestamps from the request
        video = request.files['video']
        start_time = request.form['start_time']  # e.g., '00:01:30'
        end_time = request.form['end_time']  # e.g., '00:02:30'

        # Save the uploaded video temporarily
        video_path = os.path.join(UPLOAD_FOLDER, video.filename)
        video.save(video_path)

        # Output file path
        output_path = os.path.join(OUTPUT_FOLDER, f'trimmed_{video.filename}')

        # Use ffmpeg-python to trim the video
        stream = ffmpeg.input(video_path, ss=start_time, to=end_time)
        stream = ffmpeg.output(stream, output_path)
        ffmpeg.run(stream)

        # Send the trimmed video back to the user
        return send_file(output_path, as_attachment=True)

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
