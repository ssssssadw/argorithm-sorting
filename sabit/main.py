from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
# CORS 설정: 브라우저에서 직접 Cloud Run 서버로 요청을 보낼 수 있도록 허용
CORS(app)

@app.route("/sort", methods=["POST", "OPTIONS"])
def insertion_sort_api():
    """
    클라이언트로부터 배열 데이터를 받아 단순 삽입 정렬을 수행하고,
    각 단계별(Step-by-step) 변화 과정을 기록하여 반환하는 엔드포인트
    """
    # 프리플라이트(Preflight) 요청 처리
    if request.method == "OPTIONS":
        return "", 200

    try:
        data = request.get_json() or {}
        # 요청된 배열이 없으면 기본값 사용
        arr = data.get("array", [8, 3, 5, 1, 4, 2])
        
        steps = []
        n = len(arr)
        current_arr = list(arr)
        
        # 0단계: 초기 상태 기록
        steps.append({
            "step": 0,
            "array": list(current_arr),
            "message": "초기 배열이 생성되었습니다.",
            "target": -1,
            "compared": -1
        })
        
        # 단순 삽입 정렬 알고리즘 수행 루프
        for i in range(1, n):
            key = current_arr[i]
            j = i - 1
            
            # 현재 삽입할 요소를 선택한 단계
            steps.append({
                "step": len(steps),
                "array": list(current_arr),
                "message": f"인덱스 {i}의 값({key})을 정렬된 앞부분에 삽입할 위치를 찾습니다.",
                "target": i,
                "compared": j
            })
            
            # 정렬된 원소들을 우측으로 이동시키며 올바른 위치 탐색
            while j >= 0 and current_arr[j] > key:
                current_arr[j + 1] = current_arr[j]
                j -= 1
                steps.append({
                    "step": len(steps),
                    "array": list(current_arr),
                    "message": f"비교 및 이동: 값이 더 크므로 우측으로 시프트합니다.",
                    "target": j + 1,
                    "compared": j
                })
                
            # 올바른 위치에 key 삽입
            current_arr[j + 1] = key
            steps.append({
                "step": len(steps),
                "array": list(current_arr),
                "message": f"위치 {j + 1}에 값({key}) 삽입이 완료되었습니다.",
                "target": j + 1,
                "compared": -1
            })
            
        # 최종 완료 상태 기록
        steps.append({
            "step": len(steps),
            "array": list(current_arr),
            "message": "모든 정렬이 완료되었습니다!",
            "target": -1,
            "compared": -1
        })
        
        # 성공 응답 반환 (복잡도 정보 포함)
        return jsonify({
            "status": "success",
            "server_status": "정상 작동 중 (Cloud Run)",
            "steps": steps,
            "complexity": {
                "time_best": "O(n)",
                "time_average": "O(n^2)",
                "time_worst": "O(n^2)",
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
    # Cloud Run 환경 변수 PORT를 사용하며, 기본값은 8080
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
