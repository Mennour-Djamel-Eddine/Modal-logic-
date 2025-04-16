from typing import Set, Dict, Tuple, Optional, Any
import json

class KripkeModel:
    """
    A complete Kripke model for modal logic evaluation.
    Supports worlds (W), accessibility relations (R), and valuations (V).
    Includes serialization, validation, and advanced query methods.
    """

    def __init__(self):
        """Initialize an empty Kripke model."""
        self.W: Set[str] = set()               # Worlds (e.g., {"w1", "w2"})
        self.R: Set[Tuple[str, str]] = set()   # Relations (e.g., {("w1", "w2")})
        self.V: Dict[str, Dict[str, bool]] = {} # Valuations (e.g., {"w1": {"p": True}})
        self._default_valuation = False        # Default truth value for undefined props

    # === World Management ===
    def add_world(self, world: str) -> None:
        """Add a world to the model."""
        if not isinstance(world, str):
            raise TypeError("World must be a string.")
        self.W.add(world)
        if world not in self.V:
            self.V[world] = {}

    def remove_world(self, world: str) -> None:
        """Remove a world and all its relations/valuations."""
        if world not in self.W:
            raise ValueError(f"World '{world}' does not exist.")
        self.W.remove(world)
        self.R = {(w1, w2) for (w1, w2) in self.R if w1 != world and w2 != world}
        del self.V[world]

    # === Relation Management ===
    def add_relation(self, source: str, target: str) -> None:
        """Add an accessibility relation from `source` to `target`."""
        if source not in self.W or target not in self.W:
            raise ValueError("Both worlds must exist.")
        self.R.add((source, target))

    def remove_relation(self, source: str, target: str) -> None:
        """Remove a specific accessibility relation."""
        if (source, target) not in self.R:
            raise ValueError(f"Relation ({source}, {target}) does not exist.")
        self.R.remove((source, target))

    def make_relation_reflexive(self) -> None:
        """Ensure every world accesses itself (for T/S4/S5 logics)."""
        for w in self.W:
            self.R.add((w, w))

    def make_relation_symmetric(self) -> None:
        """Ensure all relations are bidirectional (for B/S5 logics)."""
        for (w1, w2) in list(self.R):
            self.R.add((w2, w1))

    def make_relation_transitive(self) -> None:
        """Ensure relations are transitive (for S4/S5 logics)."""
        changed = True
        while changed:
            changed = False
            for (w1, w2) in list(self.R):
                for (w3, w4) in list(self.R):
                    if w2 == w3 and (w1, w4) not in self.R:
                        self.R.add((w1, w4))
                        changed = True

    # === Valuation Management ===
    def set_valuation(self, world: str, prop: str, value: bool) -> None:
        """Set the truth value of `prop` in `world`."""
        if world not in self.W:
            raise ValueError(f"World '{world}' does not exist.")
        if not isinstance(prop, str):
            raise TypeError("Proposition must be a string.")
        self.V[world][prop] = value

    def get_valuation(self, world: str, prop: str) -> bool:
        """Get the truth value of `prop` in `world` (default: False)."""
        return self.V.get(world, {}).get(prop, self._default_valuation)

    def set_default_valuation(self, default: bool) -> None:
        """Set default truth value for undefined propositions."""
        self._default_valuation = default

    # === Model Queries ===
    def get_accessible_worlds(self, world: str) -> Set[str]:
        """Get all worlds accessible from `world`."""
        return {w2 for (w1, w2) in self.R if w1 == world}

    def is_world_reachable(self, start: str, target: str, max_steps: int = 100) -> bool:
        """Check if `target` is reachable from `start` in ≤ `max_steps`."""
        visited = set()
        stack = [(start, 0)]
        while stack:
            current, steps = stack.pop()
            if current == target:
                return True
            if steps >= max_steps:
                continue
            for (w1, w2) in self.R:
                if w1 == current and w2 not in visited:
                    visited.add(w2)
                    stack.append((w2, steps + 1))
        return False

    def validate_model(self) -> bool:
        """Check if the model is consistent (no dangling relations)."""
        for (w1, w2) in self.R:
            if w1 not in self.W or w2 not in self.W:
                return False
        for world in self.V:
            if world not in self.W:
                return False
        return True

    # === Serialization ===
    def to_dict(self) -> Dict[str, Any]:
        """Export the model to a dictionary (for JSON)."""
        return {
            "W": list(self.W),
            "R": [list(pair) for pair in self.R],
            "V": {w: props for w, props in self.V.items()},
            "default_valuation": self._default_valuation
        }

    def save_to_json(self, filepath: str) -> None:
        """Save the model to a JSON file."""
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'KripkeModel':
        """Load a model from a dictionary."""
        model = cls()
        model.W = set(data["W"])
        model.R = {tuple(pair) for pair in data["R"]}
        model.V = data["V"]
        model._default_valuation = data.get("default_valuation", False)
        return model

    @classmethod
    def load_from_json(cls, filepath: str) -> 'KripkeModel':
        """Load a model from a JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        return cls.from_dict(data)

    # === Debugging ===
    def __str__(self) -> str:
        """Pretty-print the model."""
        worlds = sorted(self.W)
        relations = sorted(self.R)
        valuations = []
        for world in sorted(self.V.keys()):
            props = [f"{p}:{'T' if v else 'F'}" for p, v in self.V[world].items()]
            valuations.append(f"{world}: {{{', '.join(props)}}}")
        return (
            f"Kripke Model:\n"
            f"Worlds: {{{', '.join(worlds)}}}\n"
            f"Relations: {{{', '.join(f'({w1}→{w2})' for (w1, w2) in relations)}}}\n"
            f"Valuations:\n  " + "\n  ".join(valuations)
        )


# === Example Usage ===
if __name__ == "__main__":
    model = KripkeModel()

    # Add worlds
    model.add_world("w1")
    model.add_world("w2")
    model.add_world("w3")

    # Add relations
    model.add_relation("w1", "w2")
    model.add_relation("w2", "w3")
    model.make_relation_reflexive()  # Ensure w1→w1, w2→w2, etc.

    # Set valuations
    model.set_valuation("w1", "p", True)
    model.set_valuation("w2", "p", False)
    model.set_valuation("w3", "p", True)

    # Save/load
    model.save_to_json("model.json")
    loaded_model = KripkeModel.load_from_json("model.json")

    print(loaded_model)
    print("\nAccessible from w1:", loaded_model.get_accessible_worlds("w1"))
    print("Is w3 reachable from w1?", loaded_model.is_world_reachable("w1", "w3"))
