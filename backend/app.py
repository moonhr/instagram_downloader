from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import os
import shutil
from instagram_scraper import process_excel_and_download
from datetime import datetime
import threading

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# 진행 상황 저장
progress_status = {}

def process_in_background(task_id, filepath, output_dir):
    """백그라운드에서 다운로드 처리"""
    try:
        progress_status[task_id] = {
            'status': 'processing',
            'progress': 0,
            'message': '다운로드 시작...',
            'total': 0,
            'completed': 0
        }
        
        result = process_excel_and_download(filepath, output_dir, task_id, progress_status)
        
        if not result['success']:
            progress_status[task_id] = {
                'status': 'error',
                'message': result['message']
            }
            return
        
        # ZIP 파일 생성
        progress_status[task_id]['message'] = 'ZIP 파일 생성 중...'
        zip_filename = f"instagram_download_{task_id}"
        zip_path = shutil.make_archive(
            os.path.join(OUTPUT_FOLDER, zip_filename),
            'zip',
            output_dir
        )
        
        progress_status[task_id] = {
            'status': 'completed',
            'progress': 100,
            'message': result['message'],
            'download_url': f'/download/{os.path.basename(zip_path)}'
        }
        
    except Exception as e:
        import traceback
        print(f"에러 발생: {str(e)}")
        print(traceback.format_exc())
        progress_status[task_id] = {
            'status': 'error',
            'message': str(e)
        }

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': '파일이 없습니다'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '파일이 선택되지 않았습니다'}), 400
        
        if not file.filename.endswith(('.xlsx', '.xls', '.csv', '.numbers')):
            return jsonify({'error': '엑셀, CSV, Numbers 파일만 업로드 가능합니다'}), 400
        
        # 파일 저장
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{file.filename}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        print(f"파일 저장 완료: {filepath}")
        
        # 인스타그램 다운로드 처리 (백그라운드)
        output_dir = os.path.join(OUTPUT_FOLDER, timestamp)
        os.makedirs(output_dir, exist_ok=True)
        
        task_id = timestamp
        thread = threading.Thread(target=process_in_background, args=(task_id, filepath, output_dir))
        thread.start()
        
        return jsonify({
            'success': True,
            'task_id': task_id,
            'message': '다운로드를 시작했습니다'
        })
    
    except Exception as e:
        import traceback
        print(f"에러 발생: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/progress/<task_id>', methods=['GET'])
def get_progress(task_id):
    """진행 상황 조회"""
    if task_id in progress_status:
        return jsonify(progress_status[task_id])
    else:
        return jsonify({'error': '작업을 찾을 수 없습니다'}), 404

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        filepath = os.path.join(OUTPUT_FOLDER, filename)
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
