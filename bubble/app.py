from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
  return "Bubble Sort API Server is running!"


@app.route("/bubble-sort", methods=["POST"])
def bubble_sort():
  """클라이언트로부터 배열을 받아 버블 정렬 과정을 단계별로 기록하여 반환하는 엔드포인트"""
  try:
    data = request.get_json() or {}
    arr = data.get("array", [64, 34, 25, 12, 22, 11, 90])

    steps = []
    n = len(arr)
    arr_copy = list(arr)

    # 0단계: 초기 상태
    steps.append({
        "step": 0,
        "array": list(arr_copy),
        "comparing": [],
        "swapped": False,
        "description": "초기 배열 상태입니다.",
    })

    step_count = 1

    # 버블 정렬 알고리즘 수행
    for i in range(n):
      swapped_in_pass = False
      for j in range(0, n - i - 1):
        comparing = [j, j + 1]
        is_swapped = False

        if arr_copy[j] > arr_copy[j + 1]:
          arr_copy[j], arr_copy[j + 1] = arr_copy[j + 1], arr_copy[j]
          is_swapped = True
          swapped_in_pass = True

        steps.append({
            "step": step_count,
            "array": list(arr_copy),
            "comparing": comparing,
            "swapped": is_swapped,
            "description": (
                f"패스 {i+1}: 인덱스 {j}, {j+1} 비교"
                + (" (값 교환 발생)" if is_swapped else " (교환 없음)")
            ),
        })
        step_count += 1

      if not swapped_in_pass:
        break

    steps.append({
        "step": step_count,
        "array": list(arr_copy),
        "comparing": [],
        "swapped": False,
        "description": "버블 정렬이 완료되었습니다!",
    })

    return jsonify({
        "success": True,
        "steps": steps,
        "complexity": {
            "time_worst": "O(N^2)",
            "time_best": "O(N)",
            "space": "O(1)",
        },
    })

  except Exception as e:
    return jsonify({"success": False, "error": str(e)}), 400


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8080)
