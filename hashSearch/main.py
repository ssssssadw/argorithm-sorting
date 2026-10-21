from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
# CORS 설정: 브라우저에서 직접 Cloud Run 서버로 요청을 보낼 수 있도록 허용
CORS(app)

class Node:
    """이진 검색 트리의 각 노드를 나타내는 클래스"""
    def __init__(self, key, value=None):
        self.key = key                                  # 노드의 키 (정렬 기준)
        self.value = value if value is not None else key # 노드의 값
        self.left = None                                # 좌측 자식 노드
        self.right = None                               # 우측 자식 노드

class binarySearchTree:
    """이진 검색 트리(BST) 클래스 및 알고리즘 구현"""
    def __init__(self):
        """1) init: 이진 검색 트리 초기화"""
        self.root = None

    def to_dict(self, node):
        """현재 트리 구조를 클라이언트 시각화를 위해 JSON 직렬화 가능한 딕셔너리로 변환"""
        if not node:
            return None
        return {
            "key": node.key,
            "value": node.value,
            "left": self.to_dict(node.left),
            "right": self.to_dict(node.right)
        }

    def search_steps(self, key):
        """2) search: 키를 검색하고 탐색 과정을 단계별로 기록"""
        steps = []
        curr = self.root
        
        steps.append({
            "step": len(steps),
            "tree": self.to_dict(self.root),
            "active_key": None,
            "message": f"검색 시작: 루트 노드에서 키 '{key}'를 찾기 시작합니다."
        })
        
        while curr:
            steps.append({
                "step": len(steps),
                "tree": self.to_dict(self.root),
                "active_key": curr.key,
                "message": f"현재 노드({curr.key})와 찾는 키({key})를 비교합니다."
            })
            
            if key == curr.key:
                steps.append({
                    "step": len(steps),
                    "tree": self.to_dict(self.root),
                    "active_key": curr.key,
                    "message": f"검색 성공: 노드 키 '{curr.key}'(값: {curr.value})를 찾았습니다!"
                })
                return True, curr.value, steps
            elif key < curr.key:
                steps.append({
                    "step": len(steps),
                    "tree": self.to_dict(self.root),
                    "active_key": curr.key,
                    "message": f"키({key})가 현재 노드({curr.key})보다 작으므로 좌측 서브트리로 이동합니다."
                })
                curr = curr.left
            else:
                steps.append({
                    "step": len(steps),
                    "tree": self.to_dict(self.root),
                    "active_key": curr.key,
                    "message": f"키({key})가 현재 노드({curr.key})보다 크므로 우측 서브트리로 이동합니다."
                })
                curr = curr.right
                
        steps.append({
            "step": len(steps),
            "tree": self.to_dict(self.root),
            "active_key": None,
            "message": f"검색 실패: 트리에 키 '{key}'가 존재하지 않습니다."
        })
        return False, None, steps

    def add_steps(self, key, value):
        """3) add: 노드를 추가(삽입)하고 과정을 단계별로 기록"""
        steps = []
        
        if not self.root:
            self.root = Node(key, value)
            steps.append({
                "step": len(steps),
                "tree": self.to_dict(self.root),
                "active_key": key,
                "message": f"트리가 비어있어 루트 노드({key})로 추가했습니다."
            })
            return True, steps
            
        curr = self.root
        steps.append({
            "step": len(steps),
            "tree": self.to_dict(self.root),
            "active_key": curr.key,
            "message": f"삽입 시작: 루트 노드({curr.key})부터 위치를 탐색합니다."
        })
        
        while True:
            if key == curr.key:
                curr.value = value
                steps.append({
                    "step": len(steps),
                    "tree": self.to_dict(self.root),
                    "active_key": curr.key,
                    "message": f"키 '{key}'가 이미 존재하므로 값을 '{value}'로 갱신했습니다."
                })
                return True, steps
            elif key < curr.key:
                if not curr.left:
                    curr.left = Node(key, value)
                    steps.append({
                        "step": len(steps),
                        "tree": self.to_dict(self.root),
                        "active_key": key,
                        "message": f"노드({curr.key})의 좌측에 새 노드({key})를 추가했습니다."
                    })
                    break
                else:
                    curr = curr.left
                    steps.append({
                        "step": len(steps),
                        "tree": self.to_dict(self.root),
                        "active_key": curr.key,
                        "message": f"좌측 자식 노드({curr.key})로 이동하여 탐색을 계속합니다."
                    })
            else:
                if not curr.right:
                    curr.right = Node(key, value)
                    steps.append({
                        "step": len(steps),
                        "tree": self.to_dict(self.root),
                        "active_key": key,
                        "message": f"노드({curr.key})의 우측에 새 노드({key})를 추가했습니다."
                    })
                    break
                else:
                    curr = curr.right
                    steps.append({
                        "step": len(steps),
                        "tree": self.to_dict(self.root),
                        "active_key": curr.key,
                        "message": f"우측 자식 노드({curr.key})로 이동하여 탐색을 계속합니다."
                    })
        return True, steps

    def remove_steps(self, key):
        """4) remove: 노드를 삭제하고 과정을 단계별로 기록"""
        steps = []
        
        steps.append({
            "step": len(steps),
            "tree": self.to_dict(self.root),
            "active_key": None,
            "message": f"삭제 시작: 키 '{key}'를 탐색합니다."
        })
        
        def _remove(node, k):
            if not node:
                return None, False
            
            if k < node.key:
                node.left, deleted = _remove(node.left, k)
                return node, deleted
            elif k > node.key:
                node.right, deleted = _remove(node.right, k)
                return node, deleted
            else:
                # 삭제할 노드 발견 (자식 개수에 따른 분기)
                if not node.left:
                    return node.right, True
                elif not node.right:
                    return node.left, True
                
                # 자식이 둘인 경우: 우측 서브트리의 최솟값 노드와 교체
                temp = node.right
                while temp.left:
                    temp = temp.left
                node.key = temp.key
                node.value = temp.value
                node.right, _ = _remove(node.right, temp.key)
                return node, True

        self.root, deleted = _remove(self.root, key)
        if deleted:
            steps.append({
                "step": len(steps),
                "tree": self.to_dict(self.root),
                "active_key": key,
                "message": f"키 '{key}' 노드가 성공적으로 삭제되었습니다."
            })
        else:
            steps.append({
                "step": len(steps),
                "tree": self.to_dict(self.root),
                "active_key": None,
                "message": f"삭제 실패: 트리에 키 '{key}'가 존재하지 않습니다."
            })
        return deleted, steps

    def min_key_steps(self):
        """5) min_key: 트리의 최솟값 키를 탐색하고 과정을 기록"""
        steps = []
        if not self.root:
            steps.append({
                "step": len(steps),
                "tree": None,
                "active_key": None,
                "message": "트리가 비어있습니다."
            })
            return None, steps
            
        curr = self.root
        steps.append({
            "step": len(steps),
            "tree": self.to_dict(self.root),
            "active_key": curr.key,
            "message": "최솟값 탐색 시작: 가장 왼쪽 노드로 이동합니다."
        })
        
        while curr.left:
            curr = curr.left
            steps.append({
                "step": len(steps),
                "tree": self.to_dict(self.root),
                "active_key": curr.key,
                "message": f"좌측 자식 노드({curr.key})로 이동합니다."
            })
            
        steps.append({
            "step": len(steps),
            "tree": self.to_dict(self.root),
            "active_key": curr.key,
            "message": f"최솟값 발견: 키 '{curr.key}'(값: {curr.value})입니다."
        })
        return curr.key, steps

    def max_key_steps(self):
        """6) max_key: 트리의 최댓값 키를 탐색하고 과정을 기록"""
        steps = []
        if not self.root:
            steps.append({
                "step": len(steps),
                "tree": None,
                "active_key": None,
                "message": "트리가 비어있습니다."
            })
            return None, steps
            
        curr = self.root
        steps.append({
            "step": len(steps),
            "tree": self.to_dict(self.root),
            "active_key": curr.key,
            "message": "최댓값 탐색 시작: 가장 오른쪽 노드로 이동합니다."
        })
        
        while curr.right:
            curr = curr.right
            steps.append({
                "step": len(steps),
                "tree": self.to_dict(self.root),
                "active_key": curr.key,
                "message": f"우측 자식 노드({curr.key})로 이동합니다."
            })
            
        steps.append({
            "step": len(steps),
            "tree": self.to_dict(self.root),
            "active_key": curr.key,
            "message": f"최댓값 발견: 키 '{curr.key}'(값: {curr.value})입니다."
        })
        return curr.key, steps

    def dump_steps(self):
        """7) dump: 트리 전체 구조를 조회"""
        steps = [{
            "step": 0,
            "tree": self.to_dict(self.root),
            "active_key": None,
            "message": "이진 검색 트리의 전체 구조를 덤프(조회)합니다."
        }]
        return steps

# 전역 BST 인스턴스 생성 및 초기 샘플 데이터 주입
bst = binarySearchTree()
bst.add_steps(50, "Root")
bst.add_steps(30, "Left")
bst.add_steps(70, "Right")
bst.add_steps(20, "L.Left")
bst.add_steps(40, "L.Right")

@app.route("/bst", methods=["POST", "OPTIONS"])
def bst_api():
    """클라이언트 액션(init, search, add, remove, min_key, max_key, dump)에 따른 API 엔드포인트"""
    if request.method == "OPTIONS":
        return "", 200

    try:
        data = request.get_json() or {}
        action = data.get("action", "dump")
        key = data.get("key")
        value = data.get("value")
        
        global bst
        steps = []

        if action == "init":
            bst = binarySearchTree()
            steps = bst.dump_steps()
            steps[0]["message"] = "이진 검색 트리를 초기화했습니다."
        elif action == "search":
            if key is None:
                return jsonify({"status": "error", "message": "검색할 키를 입력해주세요."}), 400
            _, _, steps = bst.search_steps(int(key))
        elif action == "add":
            if key is None:
                return jsonify({"status": "error", "message": "추가할 키를 입력해주세요."}), 400
            val = value if value is not None else f"Val_{key}"
            _, steps = bst.add_steps(int(key), val)
        elif action == "remove":
            if key is None:
                return jsonify({"status": "error", "message": "삭제할 키를 입력해주세요."}), 400
            _, steps = bst.remove_steps(int(key))
        elif action == "min_key":
            _, steps = bst.min_key_steps()
        elif action == "max_key":
            _, steps = bst.max_key_steps()
        elif action == "dump":
            steps = bst.dump_steps()
        else:
            return jsonify({"status": "error", "message": "지원하지 않는 작업입니다."}), 400

        return jsonify({
            "status": "success",
            "server_status": "정상 작동 중 (Cloud Run)",
            "steps": steps,
            "complexity": {
                "time_search_add_remove": "평균 $O(\\log n)$ / 최악 $O(n)$",
                "time_min_max": "평균 $O(\\log n)$ / 최악 $O(n)$",
                "space": "$O(n)$"
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
