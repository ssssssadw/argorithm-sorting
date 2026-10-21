from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
# CORS 설정: 브라우저에서 직접 Cloud Run 서버로 요청을 보낼 수 있도록 허용
CORS(app)

class ChainedHash:
    """
    체이닝(Chaining) 방식을 이용한 해시 테이블 클래스
    동작 과정(Step)을 추적하여 시각화할 수 있도록 기록 기능을 포함합니다.
    """
    def __init__(self, capacity=7):
        """1) init: 해시 테이블 초기화"""
        self.capacity = capacity
        self.table = [[] for _ in range(capacity)]

    def hash_value(self, key):
        """2) hash_value: 키를 해시값(버킷 인덱스)으로 변환"""
        if isinstance(key, int):
            return key % self.capacity
        # 문자열 등의 경우 파이썬 기본 hash 함수 사용 후 절대값 처리
        return abs(hash(str(key))) % self.capacity

    def search_steps(self, key):
        """3) search: 키를 검색하고 탐색 과정을 단계별로 기록"""
        steps = []
        h = self.hash_value(key)
        bucket = self.table[h]
        
        steps.append({
            "step": len(steps),
            "table": [list(b) for b in self.table],
            "action": "search",
            "key": key,
            "bucket_index": h,
            "element_index": -1,
            "message": f"해시값 계산: hash('{key}') = {h}. {h}번 버킷을 탐색합니다."
        })
        
        for i, (k, v) in enumerate(bucket):
            if k == key:
                steps.append({
                    "step": len(steps),
                    "table": [list(b) for b in self.table],
                    "action": "search",
                    "key": key,
                    "bucket_index": h,
                    "element_index": i,
                    "message": f"탐색 성공: {h}번 버킷의 인덱스 {i}에서 키 '{key}'(값: {v})를 찾았습니다!"
                })
                return True, v, steps
            else:
                steps.append({
                    "step": len(steps),
                    "table": [list(b) for b in self.table],
                    "action": "search",
                    "key": key,
                    "bucket_index": h,
                    "element_index": i,
                    "message": f"{h}번 버킷의 인덱스 {i}의 키 '{k}'는 찾는 키와 다릅니다."
                })
        
        steps.append({
            "step": len(steps),
            "table": [list(b) for b in self.table],
            "action": "search",
            "key": key,
            "bucket_index": h,
            "element_index": -1,
            "message": f"탐색 실패: {h}번 버킷에 키 '{key}'가 존재하지 않습니다."
        })
        return False, None, steps

    def add_steps(self, key, value):
        """4) add: 키와 값을 추가(또는 갱신)하고 과정을 기록"""
        steps = []
        h = self.hash_value(key)
        bucket = self.table[h]
        
        steps.append({
            "step": len(steps),
            "table": [list(b) for b in self.table],
            "action": "add",
            "key": key,
            "value": value,
            "bucket_index": h,
            "message": f"추가 시도: 키 '{key}'의 해시값은 {h}입니다. {h}번 버킷을 확인합니다."
        })
        
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                steps.append({
                    "step": len(steps),
                    "table": [list(b) for b in self.table],
                    "action": "add",
                    "key": key,
                    "value": value,
                    "bucket_index": h,
                    "message": f"키 '{key}'가 이미 존재하므로 값을 '{value}'로 갱신합니다."
                })
                return True, steps
        
        bucket.append((key, value))
        steps.append({
            "step": len(steps),
            "table": [list(b) for b in self.table],
            "action": "add",
            "key": key,
            "value": value,
            "bucket_index": h,
            "message": f"{h}번 버킷의 체인 끝에 새 데이터('{key}': '{value}')를 추가했습니다."
        })
        return True, steps

    def remove_steps(self, key):
        """5) remove: 지정한 키를 삭제하고 과정을 기록"""
        steps = []
        h = self.hash_value(key)
        bucket = self.table[h]
        
        steps.append({
            "step": len(steps),
            "table": [list(b) for b in self.table],
            "action": "remove",
            "key": key,
            "bucket_index": h,
            "message": f"삭제 시도: 키 '{key}'의 해시값은 {h}입니다. {h}번 버킷을 탐색합니다."
        })
        
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                steps.append({
                    "step": len(steps),
                    "table": [list(b) for b in self.table],
                    "action": "remove",
                    "key": key,
                    "bucket_index": h,
                    "message": f"{h}번 버킷에서 키 '{key}'를 찾아 삭제했습니다."
                })
                return True, steps
            else:
                steps.append({
                    "step": len(steps),
                    "table": [list(b) for b in self.table],
                    "action": "remove",
                    "key": key,
                    "bucket_index": h,
                    "message": f"{h}번 버킷의 키 '{k}'는 삭제할 대상이 아닙니다."
                })
        
        steps.append({
            "step": len(steps),
            "table": [list(b) for b in self.table],
            "action": "remove",
            "key": key,
            "bucket_index": h,
            "message": f"삭제 실패: {h}번 버킷에 키 '{key}'가 존재하지 않습니다."
        })
        return False, steps

    def dump_steps(self):
        """6) dump: 전체 해시 테이블 상태를 조회"""
        steps = []
        steps.append({
            "step": 0,
            "table": [list(b) for b in self.table],
            "action": "dump",
            "message": "해시 테이블의 전체 버킷 상태를 덤프(조회)합니다."
        })
        return steps

# 전역 해시 테이블 인스턴스 생성 (초기 크기: 7)
hash_table = ChainedHash(capacity=7)
# 샘플 데이터 초기 주입
hash_table.add_steps(12, "Apple")
hash_table.add_steps(25, "Banana")
hash_table.add_steps(36, "Cherry")

@app.route("/hash", methods=["POST", "OPTIONS"])
def hash_api():
    """
    클라이언트의 요청 액션(init, search, add, remove, dump)에 따라 
    해시 알고리즘을 수행하고 결과를 반환하는 통합 엔드포인트
    """
    if request.method == "OPTIONS":
        return "", 200

    try:
        data = request.get_json() or {}
        action = data.get("action", "dump")
        key = data.get("key")
        value = data.get("value")
        
        global hash_table
        steps = []

        if action == "init":
            capacity = int(data.get("capacity", 7))
            hash_table = ChainedHash(capacity=capacity)
            steps = hash_table.dump_steps()
            steps[0]["message"] = f"해시 테이블을 크기 {capacity}로 초기화했습니다."
        elif action == "search":
            if key is None:
                return jsonify({"status": "error", "message": "검색할 키를 입력해주세요."}), 400
            _, _, steps = hash_table.search_steps(key)
        elif action == "add":
            if key is None or value is None:
                return jsonify({"status": "error", "message": "추가할 키와 값을 모두 입력해주세요."}), 400
            _, steps = hash_table.add_steps(key, value)
        elif action == "remove":
            if key is None:
                return jsonify({"status": "error", "message": "삭제할 키를 입력해주세요."}), 400
            _, steps = hash_table.remove_steps(key)
        elif action == "dump":
            steps = hash_table.dump_steps()
        else:
            return jsonify({"status": "error", "message": "지원하지 않는 작업입니다."}), 400

        return jsonify({
            "status": "success",
            "server_status": "정상 작동 중 (Cloud Run)",
            "steps": steps,
            "complexity": {
                "time_search": "평균 O(1) / 최악 O(n)",
                "time_insertion": "평균 O(1)",
                "time_deletion": "평균 O(1)",
                "space": "O(n + m) (m: 버킷 개수)"
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
