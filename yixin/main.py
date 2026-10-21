from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
# CORS 설정: 브라우저에서 직접 Cloud Run API를 호출할 수 있도록 허용
CORS(app)

@app.route("/search", methods=["POST", "OPTIONS"])
def binary_search_api():
    """
    클라이언트로부터 정렬된 배열과 찾고자 하는 값(target)을 받아
    이진 검색을 수행하고, 각 단계별 포인터 변화 과정을 기록하여 반환하는 엔드포인트
    """
    # 프리플라이트(Preflight) 요청 처리
    if request.method == "OPTIONS":
        return "", 200

    try:
        data = request.get_json()
        # 입력된 배열이 없거나 정렬되지 않은 경우를 대비해 정렬 수행
        arr = sorted(data.get("array", [1, 3, 5, 7, 9, 11, 13, 15]))
        target = int(data.get("target", 7))
        
        steps = []
        low = 0
        high = len(arr) - 1
        found_index = -1
        
        # 0단계: 초기 상태 기록
        steps.append({
            "step": 0,
            "array": list(arr),
            "low": low,
            "high": high,
            "mid": -1,
            "message": f"초기 상태: 탐색 대상 값({target})을 찾기 위해 low={low}, high={high}로 설정합니다."
        })
        
        # 이진 검색 알고리즘 수행 루프
        while low <= high:
            mid = (low + high) // 2
            
            steps.append({
                "step": len(steps),
                "array": list(arr),
                "low": low,
                "high": high,
                "mid": mid,
                "message": f"중간점 계산: mid={mid} (값: {arr[mid]}). target({target})과 비교합니다."
            })
            
            if arr[mid] == target:
                found_index = mid
                steps.append({
                    "step": len(steps),
                    "array": list(arr),
                    "low": low,
                    "high": high,
                    "mid": mid,
                    "message": f"성공: 인덱스 {mid}에서 값 {target}을(를) 찾았습니다!"
                })
                break
            elif arr[mid] < target:
                steps.append({
                    "step": len(steps),
                    "array": list(arr),
                    "low": low,
                    "high": high,
                    "mid": mid,
                    "message": f"중간값({arr[mid]})이 target({target})보다 작으므로 탐색 범위를 우측으로 좁힙니다."
                })
                low = mid + 1
            else:
                steps.append({
                    "step": len(steps),
                    "array": list(arr),
                    "low": low,
                    "high": high,
                    "mid": mid,
                    "message": f"중간값({arr[mid]})이 target({target})보다 크므로 탐색 범위를 좌측으로 좁힙니다."
                })
                high = mid - 1
                
        # 탐색 실패 시 처리
        if found_index == -1:
            steps.append({
                "step": len(steps),
                "array": list(arr),
                "low": low,
                "high": high,
                "mid": -1,
                "message": f"탐색 실패: 배열에 값 {target}이(가) 존재하지 않습니다."
            })
            
        # 결과 반환 (복잡도 정보 포함)
        return jsonify({
            "status": "success",
            "server_status": "정상 작동 중 (Cloud Run)",
            "found_index": found_index,
            "steps": steps,
            "complexity": {
                "time": "O(log n)",
                "space": "O(1)"
            }
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "server_status": "오류 발생",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
