# main.py
# 구글 클라우드 런에서 구동되는 Flask 기반 삽입 정렬 API 서버
# 클라이언트로부터 배열 데이터를 받아 삽입 정렬 과정을 단계별(Step-by-step)로 기록하여 반환합니다.

from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/sort', methods=['POST'])
def insertion_sort_api():
    """
    POST 요청으로 전달된 배열 데이터를 기반으로 삽입 정렬을 수행하고,
    매 단계의 상태(비교 대상, 이동/삽입 과정)를 기록하여 반환합니다.
    """
    try:
        # 클라이언트 JSON 데이터 파싱
        req_data = request.get_json()
        arr = req_data.get('array', [8, 3, 5, 1, 4, 2])
        
        # 입력 데이터 유효성 검증
        if not isinstance(arr, list) or not all(isinstance(x, (int, float)) for x in arr):
            return jsonify({
                'success': False,
                'error': '유효한 숫자 배열을 전달해 주세요.'
            }), 400

        steps = []
        current_arr = list(arr)
        n = len(current_arr)
        
        # 0단계: 초기 상태 기록
        steps.append({
            'step': 0,
            'description': '초기 배열 상태입니다.',
            'array': list(current_arr),
            'comparing': [],
            'inserted': []
        })
        
        # 삽입 정렬 알고리즘 수행 및 단계 기록
        for i in range(1, n):
            key = current_arr[i]
            j = i - 1
            
            steps.append({
                'step': len(steps),
                'description': f'인덱스 {i} (값: {key})를 정렬된 좌측 영역에 삽입할 차례입니다.',
                'array': list(current_arr),
                'comparing': [i, j],
                'inserted': []
            })
            
            while j >= 0 and current_arr[j] > key:
                steps.append({
                    'step': len(steps),
                    'description': f'비교: {current_arr[j]} > {key}. 큰 값을 우측으로 한 칸 이동합니다.',
                    'array': list(current_arr),
                    'comparing': [j, j+1],
                    'inserted': []
                })
                current_arr[j + 1] = current_arr[j]
                j -= 1
                
                steps.append({
                    'step': len(steps),
                    'description': '원소 우측 이동 완료 후 상태',
                    'array': list(current_arr),
                    'comparing': [],
                    'inserted': []
                })
                
            current_arr[j + 1] = key
            steps.append({
                'step': len(steps),
                'description': f'올바른 위치(인덱스 {j+1})에 값 {key} 삽입 완료',
                'array': list(current_arr),
                'comparing': [],
                'inserted': [j + 1]
            })
            
        # 최종 정렬 완료 단계
        steps.append({
            'step': len(steps),
            'description': '삽입 정렬이 성공적으로 완료되었습니다!',
            'array': list(current_arr),
            'comparing': [],
            'inserted': list(range(n))
        })

        # 성공 응답 반환
        return jsonify({
            'success': True,
            'initial_array': arr,
            'sorted_array': current_arr,
            'steps': steps,
            'complexity': {
                'time_worst': 'O(n²)',
                'time_average': 'O(n²)',
                'time_best': 'O(n) [이미 정렬된 경우]',
                'space': 'O(1) [제자리 정렬]'
            }
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Cloud Run에서 지정하는 PORT 환경 변수 사용 (기본값: 8080)
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
