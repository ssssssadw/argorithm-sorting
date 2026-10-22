import os
from flask import Blueprint, Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # CORS 설정: GAS 및 브라우저 요청 허용

# url_prefix를 '/search'로 지정하여 해당 경로로 들어오는 모든 요청을 처리
bp = Blueprint('api', __name__, url_prefix='/search')


class FixedSizeQueue:
  """고정 길이 원형 큐 (Fixed-Size Circular Queue) 클래스"""

  def __init__(self, capacity=20):
    self.capacity = int(capacity)
    self.queue = [None] * self.capacity
    self.front = 0
    self.rear = -1
    self.size = 0

  def is_empty(self):
    """큐가 비어있는지 확인 - 시간 복잡도: O(1)"""
    return self.size == 0

  def is_full(self):
    """큐가 가득 찼는지 확인 - 시간 복잡도: O(1)"""
    return self.size == self.capacity

  def push(self, item):
    """데이터 삽입 (Rear 방향) - 시간 복잡도: O(1)"""
    if self.is_full():
      raise OverflowError("큐가 가득 찼습니다 (Overflow).")
    self.rear = (self.rear + 1) % self.capacity
    self.queue[self.rear] = item
    self.size += 1
    return self.get_state()

  def pop(self):
    """데이터 삭제 및 추출 (Front 방향) - 시간 복잡도: O(1)"""
    if self.is_empty():
      raise IndexError("큐가 비어있습니다 (Underflow).")
    item = self.queue[self.front]
    self.queue[self.front] = None
    self.front = (self.front + 1) % self.capacity
    self.size -= 1
    return item, self.get_state()

  def peek(self):
    """전면(Front) 데이터 확인 - 시간 복잡도: O(1)"""
    if self.is_empty():
      raise IndexError("큐가 비어있습니다.")
    return self.queue[self.front]

  def clear(self):
    """큐 전체 초기화 - 시간 복잡도: O(N)"""
    self.queue = [None] * self.capacity
    self.front = 0
    self.rear = -1
    self.size = 0
    return self.get_state()

  def find_index(self, value):
    """특정 값의 논리적 인덱스 검색 - 시간 복잡도: O(N)"""
    current = self.front
    for i in range(self.size):
      if self.queue[current] == value:
        return i
      current = (current + 1) % self.capacity
    return -1

  def count_value(self, value):
    """특정 값의 개수 확인 - 시간 복잡도: O(N)"""
    cnt = 0
    current = self.front
    for _ in range(self.size):
      if self.queue[current] == value:
        cnt += 1
      current = (current + 1) % self.capacity
    return cnt

  def contains(self, value):
    """특정 값의 존재 여부 검사 - 시간 복잡도: O(N)"""
    return self.count_value(value) > 0

  def dump(self):
    """전면부터 후면까지의 전체 데이터 출력 - 시간 복잡도: O(N)"""
    result = []
    current = self.front
    for _ in range(self.size):
      result.append(self.queue[current])
      current = (current + 1) % self.capacity
    return result

  def get_state(self):
    """현재 큐의 상태 정보를 딕셔너리로 반환"""
    return {
        "capacity": self.capacity,
        "size": self.size,
        "front": self.front,
        "rear": self.rear,
        "queue_array": self.queue,
        "dump": self.dump(),
        "is_empty": self.is_empty(),
        "is_full": self.is_full(),
    }


# 전역 큐 인스턴스 생성 기본값을 20으로 설정
queue_instance = FixedSizeQueue(20)


@bp.route("/", methods=["GET"])
def index():
  """서버 정상 작동 확인용 엔드포인트 (/search/)"""
  return jsonify({
      "status": "online",
      "message": (
          "Fixed-Size Queue Server with /search prefix (Capacity: 20) is"
          " running!"
      ),
  })


@bp.route("/api/init", methods=["POST"])
def api_init():
  """1. 고정 길이 큐 초기화 API"""
  data = request.get_json() or {}
  capacity = data.get("capacity", 20)
  global queue_instance
  try:
    queue_instance = FixedSizeQueue(int(capacity))
    return jsonify({
        "success": True,
        "message": f"큐가 용량 {capacity}(으)로 초기화되었습니다.",
        "data": queue_instance.get_state(),
    })
  except Exception as e:
    return jsonify({"success": False, "error": str(e)}), 400


@bp.route("/api/push", methods=["POST"])
def api_push():
  """2. 데이터 삽입 API"""
  data = request.get_json() or {}
  if "value" not in data:
    return jsonify({"success": False, "error": "값이 제공되지 않았습니다."}), 400
  try:
    state = queue_instance.push(data["value"])
    return jsonify({
        "success": True,
        "message": f"데이터 '{data['value']}' 삽입 성공",
        "data": state,
    })
  except OverflowError as e:
    return jsonify({"success": False, "error": str(e)}), 400


@bp.route("/api/pop", methods=["POST"])
def api_pop():
  """3. 데이터 삭제 API"""
  try:
    item, state = queue_instance.pop()
    return jsonify({
        "success": True,
        "message": f"데이터 '{item}' 삭제(출력) 성공",
        "popped_item": item,
        "data": state,
    })
  except IndexError as e:
    return jsonify({"success": False, "error": str(e)}), 400


@bp.route("/api/size", methods=["GET"])
def api_size():
  """4. 현재 큐 크기 반환 API"""
  return jsonify({
      "success": True,
      "size": queue_instance.size,
      "data": queue_instance.get_state(),
  })


@bp.route("/api/status", methods=["GET"])
def api_status():
  """5. 큐 상태 검사 API"""
  return jsonify({
      "success": True,
      "is_empty": queue_instance.is_empty(),
      "is_full": queue_instance.is_full(),
      "data": queue_instance.get_state(),
  })


@bp.route("/api/front", methods=["GET"])
def api_front():
  """6. 전면 데이터 확인 API"""
  try:
    item = queue_instance.peek()
    return jsonify({
        "success": True,
        "front_item": item,
        "data": queue_instance.get_state(),
    })
  except IndexError as e:
    return jsonify({"success": False, "error": str(e)}), 400


@bp.route("/api/clear", methods=["POST"])
def api_clear():
  """7. 전체 데이터 삭제 API"""
  state = queue_instance.clear()
  return jsonify({
      "success": True,
      "message": "큐가 전체 초기화되었습니다.",
      "data": state,
  })


@bp.route("/api/index", methods=["POST"])
def api_index():
  """8. 인덱스 검색 API"""
  data = request.get_json() or {}
  if "value" not in data:
    return jsonify({"success": False, "error": "값이 제공되지 않았습니다."}), 400
  idx = queue_instance.find_index(data["value"])
  return jsonify({
      "success": `True`,
      "value": data["value"],
      "index": idx,
      "data": queue_instance.get_state(),
  })


@bp.route("/api/count", methods=["POST"])
def api_count():
  """9. 값 개수 확인 API"""
  data = request.get_json() or {}
  if "value" not in data:
    return jsonify({"success": False, "error": "값이 제공되지 않았습니다."}), 400
  cnt = queue_instance.count_value(data["value"])
  return jsonify({
      "success": True,
      "value": data["value"],
      "count": cnt,
      "data": queue_instance.get_state(),
  })


@bp.route("/api/contains", methods=["POST"])
def api_contains():
  """10. 존재 여부 검사 API"""
  data = request.get_json() or {}
  if "value" not in data:
    return jsonify({"success": False, "error": "값이 제공되지 않았습니다."}), 400
  exists = queue_instance.contains(data["value"])
  return jsonify({
      "success": True,
      "value": data["value"],
      "contains": exists,
      "data": queue_instance.get_state(),
  })


@bp.route("/api/dump", methods=["GET"])
def api_dump():
  """11. 전체 데이터 출력 API"""
  return jsonify({
      "success": True,
      "dump": queue_instance.dump(),
      "data": queue_instance.get_state(),
  })


# 앱에 블루프린트 등록
app.register_blueprint(bp)

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 8080))
  app.run(host="0.0.0.0", port=port)
