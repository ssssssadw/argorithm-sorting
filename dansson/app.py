import os
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
  return "Selection Sort API Server is running!"


@app.route("/selection-sort", methods=["POST"])
def selection_sort():
  """클라이언트로부터 배열을 받아 선택 정렬 과정을 단계별(Step-by-Step)로 기록하여 반환하는 엔드포인트"""
  try:
    data = request.get_json() or {}
    # 입력된 배열이 없으면 기본 테스트 배열 사용
    arr = data.get("array", [64, 25, 12, 22, 11])

    steps = []
    n = len(arr)
    arr_copy = list(arr)

    # 0단계: 초기 상태 기록
    steps.append({
        "step": 0,
        "array": list(arr_copy),
        "comparing": [],
        "min_index": -1,
        "swapped": False,
        "description": "초기 배열 상태입니다.",
    })

    step_count = 1

    # 선택 정렬 알고리즘 수행
    for i in range(n - 1):
      min_idx = i
      # 최소값 후보 지정 단계 기록
      steps.append({
          "step": step_count,
          "array": list(arr_copy),
          "comparing": [],
          "min_index": min_idx,
          "swapped": False,
          "description": (
              f"패스 {i+1}: 인덱스 {i} (값: {arr_copy[i]})를 최소값 후보로"
              " 설정합니다."
          ),
      })
      step_count += 1

      for j in range(i + 1, n):
        comparing = [min_idx, j]
        is_new_min = False

        # 더 작은 값을 찾으면 최소값 인덱스 갱신
        if arr_copy[j] < arr_copy[min_idx]:
          min_idx = j
          is_new_min = True

        steps.append({
            "step": step_count,
            "array": list(arr_copy),
            "comparing": comparing,
            "min_index": min_idx,
            "swapped": False,
            "description": (
                f"비교: 인덱스 {j} (값: {arr_copy[j]})와 현재 최소값 비교"
                + (" (새로운 최소값 발견!)" if is_new_min else "")
            ),
        })
        step_count += 1

      # 패스 종료 후 최소값이 바뀌었으면 원소 교환 (Swap)
      is_swapped = False
      if min_idx != i:
        arr_copy[i], arr_copy[min_idx] = arr_copy[min_idx], arr_copy[i]
        is_swapped = True

      steps.append({
          "step": step_count,
          "array": list(arr_copy),
          "comparing": [i, min_idx] if is_swapped else [],
          "min_index": min_idx,
          "swapped": is_swapped,
          "description": (
              f"패스 {i+1} 완료:"
              + (
                  f" 인덱스 {i}와 {min_idx}의 값 교환 발생"
                  if is_swapped
                  else " 교환 없음 (이미 올바른 위치)"
              )
          ),
      })
      step_count += 1

    # 최종 완료 단계 추가
    steps.append({
        "step": step_count,
        "array": list(arr_copy),
        "comparing": [],
        "min_index": -1,
        "swapped": False,
        "description": "선택 정렬이 완료되었습니다!",
    })

    # 결과 데이터 및 시간/공간 복잡도 정보 반환
    return jsonify({
        "success": True,
        "steps": steps,
        "complexity": {
            "time_worst": "O(N^2)",
            "time_best": "O(N^2)",
            "space": "O(1)",
        },
    })

  except Exception as e:
    return jsonify({"success": False, "error": str(e)}), 400


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 8080))
  app.run(host="0.0.0.0", port=port)
