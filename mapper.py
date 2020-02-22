from typing import Dict, Set, List


class State:
    def __init__(self, name, is_end=False, local_map: Dict[str, Set[str]] = None, lambdas: Set[str] = None):
        """
        :param name: name of state
        :param local_map: dict in which keys are letters and values are state names to move automaton to
        """
        self.name = name
        self._is_end = is_end
        self._local_map = local_map if local_map and all(local_map.keys()) else dict()
        self._lambdas: Set[str] = lambdas or set()

    @property
    def is_final(self):
        return self._is_end

    def add_jump(self, letter: str, state: Set[str]) -> None:
        if self._local_map.get(letter):
            raise ValueError("Letter " + letter + " already exists in " + self.name + " local map")
        self._local_map[letter] = state

    def add_lambdas(self, lambda_transitions: Set[str]) -> None:
        self._lambdas.update(lambda_transitions)

    def next_states(self, letter: str) -> Set[str]:
        return self._local_map.get(letter, set()).copy()

    @property
    def nearest_lambdas(self) -> Set[str]:
        return self._lambdas.copy()

    def is_present(self, letter: str) -> bool:
        return bool(self._local_map.get(letter))

    @property
    def used_alphabet(self) -> Set[str]:
        return set(self._local_map.keys())


class Map:
    def __init__(self, alphabet: Set[str], data: List[State] = None):
        self._alphabet = alphabet
        self._data = {item.name: item for item in data} if data and alphabet else dict()
        self.check_integrity()

    def __getitem__(self, item: str) -> State:
        return self._data.get(item)

    @property
    def alphabet(self):
        return self._alphabet

    @property
    def data(self):
        return self._data.copy()

    def extend_data(self, new_data: List[State]):
        self.data.update({item.name: item for item in new_data})
        self.check_integrity()

    def all_lambdas(self, state: str, result: Set[str] = None):
        result = result if result else set()
        current_state = self[state]
        if current_state is None:
            raise RuntimeError("Cannot find state " + state + " in the map")
        if result.issuperset({current_state.name}):
            return
        result.add(current_state.name)
        for lambda_transition in current_state.nearest_lambdas:
            self.all_lambdas(lambda_transition, result)
        return result

    def step(self, current_states: Set[str]):
        pass

    @property
    def initial_state(self) -> Set[str]:
        return self.all_lambdas(
            self["q0"].name if self["q0"] else self[min(self._data.keys())].name
        )

    def check_integrity(self) -> None:
        pass
