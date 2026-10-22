from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # CORS 허용

# 고정 길이 큐 설정 (사이즈: 20)
CAPACITY = 20
queue = []

# 1. 초기화
@app.route('/api/init', methods=['POST'])
def api_init():
    global queue
    queue = []
    return jsonify({"success": True, "message": "큐가 초기화되었습니다.", "size": CAPACITY, "queue": queue})

# 2. Push & Pop
@app.route('/api/push', methods=['POST'])
def api_push():
    data = request.json
    value = data.get('value')
    if len(queue) >= CAPACITY:
        return jsonify({"success": False, "message": "Queue Overflow (Full)"}), 400
    queue.append(value)
    return jsonify({"success": True, "queue": queue})

@app.route('/api/pop', methods=['POST'])
def api_pop():
    if len(queue) == 0:
        return jsonify({"success": False, "message": "Queue Underflow (Empty)"}), 400
    popped = queue.pop(0) # Front에서 제거
    return jsonify({"success": True, "popped": popped, "queue": queue})

# 3. 현재 데이터 개수(길이/크기) 반환
@app.route('/api/size', methods=['GET'])
def api_size():
    return jsonify({"success": True, "count": len(queue)})

# 4. 상태 검사 (full, empty)
@app.route('/api/status', methods=['GET'])
def api_status():
    is_empty = len(queue) == 0
    is_full = len(queue) >= CAPACITY
    return jsonify({
        "success": True,
        "isEmpty": is_empty,
        "isFull": is_full,
        "size": len(queue),
        "capacity": CAPACITY
    })

# 5. 전면(Front) 데이터 확인
@app.route('/api/front', methods=['GET'])
def api_front():
    if len(queue) == 0:
        return jsonify({"success": True, "front": None, "message": "큐가 비어 있습니다."})
    return jsonify({"success": True, "front": queue[0]})

# 6. 큐 전체 데이터 삭제
@app.route('/api/clear', methods=['POST'])
def api_clear():
    global queue
    queue = []
    return jsonify({"success": True, "message": "큐의 모든 데이터가 삭제되었습니다.", "queue": queue})

# 7. 값의 index 검색
@app.route('/api/index/<int:val>', methods=['GET'])
def api_index(val):
    try:
        idx = queue.index(val)
        return jsonify({"success": True, "value": val, "index": idx})
    except ValueError:
        return jsonify({"success": True, "value": val, "index": -1, "message": "값이 존재하지 않습니다."})

# 8. 값의 개수(길이/크기) 반환
@app.route('/api/count/<int:val>', methods=['GET'])
def api_count(val):
    cnt = queue.count(val)
    return jsonify({"success": True, "value": val, "count": cnt})

# 9. 값의 존재 여부 검사
@app.route('/api/contains/<int:val>', methods=['GET'])
def api_contains(val):
    exists = val in queue
    return jsonify({"success": True, "value": val, "exists": exists})

# 10. Front부터 Rear까지 출력
@app.route('/api/print', methods=['GET'])
def api_print():
    return jsonify({"success": True, "queue": queue})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
