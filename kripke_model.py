from typing import Set, Dict, Tuple, Optional, Any
import json

# Import the KripkeModel class from the first document
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

# Import the Formula classes from the second document
class Formula:
    pass  # Base class

class Prop(Formula):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return self.name

class Not(Formula):
    def __init__(self, operand):
        if not isinstance(operand, Formula): raise TypeError("Operand must be a Formula")
        self.operand = operand
    def __repr__(self):
        return f"¬{self.operand}"

class And(Formula):
    def __init__(self, left, right):
        if not isinstance(left, Formula): raise TypeError("Left operand must be a Formula")
        if not isinstance(right, Formula): raise TypeError("Right operand must be a Formula")
        self.left = left
        self.right = right
    def __repr__(self):
        return f"({self.left} ∧ {self.right})"

class Or(Formula):
    def __init__(self, left, right):
        if not isinstance(left, Formula): raise TypeError("Left operand must be a Formula")
        if not isinstance(right, Formula): raise TypeError("Right operand must be a Formula")
        self.left = left
        self.right = right
    def __repr__(self):
        return f"({self.left} ∨ {self.right})"

class Implies(Formula):
    def __init__(self, left, right):
        if not isinstance(left, Formula): raise TypeError("Left operand must be a Formula")
        if not isinstance(right, Formula): raise TypeError("Right operand must be a Formula")
        self.left = left
        self.right = right
    def __repr__(self):
        return f"({self.left} → {self.right})"

class Box(Formula):  # Necessarily (□)
    def __init__(self, operand):
        if not isinstance(operand, Formula): raise TypeError("Operand must be a Formula")
        self.operand = operand
    def __repr__(self):
        return f"□{self.operand}"

class Diamond(Formula):  # Possibly (◇)
    def __init__(self, operand):
        if not isinstance(operand, Formula): raise TypeError("Operand must be a Formula")
        self.operand = operand
    def __repr__(self):
        return f"◇{self.operand}"

def parse_simple_formula(formula_str):
    """Tente de parser une formule simple (non recommandé pour des cas complexes)."""
    formula_str = formula_str.strip()

    # Basic case: Proposition
    if ' ' not in formula_str and not any(op in formula_str for op in ['¬', '□', '◇', '∧', '∨', '→', '(', ')']):
        return Prop(formula_str)

    # Unary prefix operators
    if formula_str.startswith('¬'):
        return Not(parse_simple_formula(formula_str[1:]))
    if formula_str.startswith('□'):
        return Box(parse_simple_formula(formula_str[1:]))
    if formula_str.startswith('◇'):
        return Diamond(parse_simple_formula(formula_str[1:]))

    # Simple handling of external parentheses
    if formula_str.startswith('(') and formula_str.endswith(')'):
        return parse_simple_formula(formula_str[1:-1])

    # Search for binary operators
    if '→' in formula_str:
        split_pos = formula_str.rfind('→')
        left = parse_simple_formula(formula_str[:split_pos].strip())
        right = parse_simple_formula(formula_str[split_pos+1:].strip())
        return Implies(left, right)

    if '∨' in formula_str:
        split_pos = formula_str.rfind('∨')
        left = parse_simple_formula(formula_str[:split_pos].strip())
        right = parse_simple_formula(formula_str[split_pos+1:].strip())
        return Or(left, right)

    if '∧' in formula_str:
        split_pos = formula_str.rfind('∧')
        left = parse_simple_formula(formula_str[:split_pos].strip())
        right = parse_simple_formula(formula_str[split_pos+1:].strip())
        return And(left, right)

    raise ValueError(f"Cannot parse formula: '{formula_str}'")

# New function to evaluate modal formulas in a Kripke model
def evaluate_formula(model: KripkeModel, formula: Formula, world: str) -> bool:
    """
    Evaluate a modal formula in a specified world of a Kripke model.
    Returns True if the formula is satisfied in the world, False otherwise.
    """
    if not model.validate_model():
        raise ValueError("Invalid Kripke model")
    
    if world not in model.W:
        raise ValueError(f"World '{world}' does not exist in the model")
    
    # Base case: Proposition
    if isinstance(formula, Prop):
        return model.get_valuation(world, formula.name)
    
    # Negation
    elif isinstance(formula, Not):
        return not evaluate_formula(model, formula.operand, world)
    
    # Conjunction
    elif isinstance(formula, And):
        return (evaluate_formula(model, formula.left, world) and 
                evaluate_formula(model, formula.right, world))
    
    # Disjunction
    elif isinstance(formula, Or):
        return (evaluate_formula(model, formula.left, world) or 
                evaluate_formula(model, formula.right, world))
    
    # Implication
    elif isinstance(formula, Implies):
        return (not evaluate_formula(model, formula.left, world) or 
                evaluate_formula(model, formula.right, world))
    
    # Box (Necessity) operator: true if formula is true in all accessible worlds
    elif isinstance(formula, Box):
        accessible_worlds = model.get_accessible_worlds(world)
        return all(evaluate_formula(model, formula.operand, w) for w in accessible_worlds)
    
    # Diamond (Possibility) operator: true if formula is true in at least one accessible world
    elif isinstance(formula, Diamond):
        accessible_worlds = model.get_accessible_worlds(world)
        return any(evaluate_formula(model, formula.operand, w) for w in accessible_worlds)
    
    else:
        raise TypeError(f"Unknown formula type: {type(formula)}")

def evaluate_formula_in_all_worlds(model: KripkeModel, formula: Formula) -> Dict[str, bool]:
    """
    Evaluate a formula in all worlds of the model.
    Returns a dictionary mapping world names to truth values.
    """
    return {world: evaluate_formula(model, formula, world) for world in model.W}

# Main program
if __name__ == "__main__":
    # Create a sample Kripke model
    model = KripkeModel()
    
    # Add worlds
    model.add_world("w1")
    model.add_world("w2")
    model.add_world("w3")
    
    # Add relations
    model.add_relation("w1", "w2")
    model.add_relation("w2", "w3")
    model.make_relation_reflexive()  # w1→w1, w2→w2, w3→w3
    
    # Set valuations for proposition 'p'
    model.set_valuation("w1", "p", True)
    model.set_valuation("w2", "p", False)
    model.set_valuation("w3", "p", True)
    
    # Set valuations for proposition 'q'
    model.set_valuation("w1", "q", False)
    model.set_valuation("w2", "q", True)
    model.set_valuation("w3", "q", True)
    
    print("Kripke Model Structure:")
    print(model)
    
    # Create and evaluate modal formulas
    formulas = [
        (Prop("p"), "p"),
        (Not(Prop("p")), "¬p"),
        (And(Prop("p"), Prop("q")), "p ∧ q"),
        (Or(Prop("p"), Prop("q")), "p ∨ q"),
        (Implies(Prop("p"), Prop("q")), "p → q"),
        (Box(Prop("p")), "□p"),
        (Diamond(Prop("p")), "◇p"),
        (Box(Implies(Prop("p"), Prop("q"))), "□(p → q)")
    ]
    
    print("\nEvaluating Formulas:")
    for formula_obj, formula_str in formulas:
        results = evaluate_formula_in_all_worlds(model, formula_obj)
        print(f"\nFormula: {formula_str}")
        for world, result in results.items():
            print(f"  {world}: {result}")
    
    # Demonstrate formula parsing (optional)
    print("\nDemonstrating Formula Parsing:")
    try:
        parsed_formula = parse_simple_formula("□(p → q)")
        print(f"Parsed formula: {parsed_formula}")
        results = evaluate_formula_in_all_worlds(model, parsed_formula)
        print("Evaluation results:")
        for world, result in results.items():
            print(f"  {world}: {result}")
    except ValueError as e:
        print(f"Parsing error: {e}")
    
    # Interactive mode (optional)
    print("\nInteractive Mode:")
    print("Enter a modal formula to evaluate (or 'exit' to quit)")
    print("Use 'p', 'q' for propositions")
    print("Use '¬' for negation, '∧' for AND, '∨' for OR, '→' for IMPLIES")
    print("Use '□' for BOX (necessity), '◇' for DIAMOND (possibility)")
    
    while True:
        user_input = input("\nEnter formula: ")
        if user_input.lower() == 'exit':
            break
        
        try:
            parsed = parse_simple_formula(user_input)
            print(f"Parsed as: {parsed}")
            results = evaluate_formula_in_all_worlds(model, parsed)
            print("Results:")
            for world, result in results.items():
                print(f"  {world}: {result}")
        except Exception as e:
            print(f"Error: {e}")