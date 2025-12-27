class Store:
    def __init__(self):
        self._default_state = {
            "score": 0,
            "homeworkList": [],
            "questions": 0,
        }
        self._state = self._default_state.copy()

    def get(self, key):
        return self._state.get(key)

    def set(self, key, value):
        self._state[key] = value

    def add_homework(self, homework):
        self._state["homeworkList"].append(homework)

    def add_question(self, count: int = 1):
        self._state["questions"] += count

    def set_score(self, number):
        self._state["score"] = number

    def reset(self):
        self._state = self._default_state.copy()

    def to_json(self):
        return self._state


store = Store()
