# modal_logic_parser.py

# Classes pour représenter la structure des formules logiques modales
class Formula:
    pass # Classe de base

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

class Box(Formula): # Necessarily (□)
    def __init__(self, operand):
        if not isinstance(operand, Formula): raise TypeError("Operand must be a Formula")
        self.operand = operand
    def __repr__(self):
        return f"□{self.operand}"

class Diamond(Formula): # Possibly (◇)
    def __init__(self, operand):
        if not isinstance(operand, Formula): raise TypeError("Operand must be a Formula")
        self.operand = operand
    def __repr__(self):
        return f"◇{self.operand}"

# --- Fonction de Parsing Simplifiée (Optionnelle, pour convertir une chaîne) ---
# ATTENTION : Ce parseur est très basique et ne gère pas la précédence correctement
# ni les parenthèses complexes. Il est fourni à titre d'exemple limité.
# Il est PRÉFÉRABLE de construire l'arbre de la formule manuellement avec les classes ci-dessus.

def parse_simple_formula(formula_str):
    """Tente de parser une formule simple (non recommandé pour des cas complexes)."""
    formula_str = formula_str.strip()

    # Cas de base: Proposition
    if ' ' not in formula_str and not any(op in formula_str for op in ['¬', '□', '◇', '∧', '∨', '→', '(', ')']):
        return Prop(formula_str)

    # Opérateurs unaires préfixes
    if formula_str.startswith('¬'):
        return Not(parse_simple_formula(formula_str[1:]))
    if formula_str.startswith('□'):
        return Box(parse_simple_formula(formula_str[1:]))
    if formula_str.startswith('◇'):
        return Diamond(parse_simple_formula(formula_str[1:]))

    # Gestion simple des parenthèses externes
    if formula_str.startswith('(') and formula_str.endswith(')'):
         # Ceci est très naïf, ne gère pas les parenthèses internes correctement
        return parse_simple_formula(formula_str[1:-1])

    # Recherche d'opérateurs binaires (ordre de priorité très simple: →, ∨, ∧)
    # Attention: ceci ne respecte pas les règles de précédence standard sans parenthèses
    split_pos = -1
    op_symbol = None

    # Cherche '→' (le moins prioritaire dans cet exemple)
    # Note: besoin d'ignorer les opérateurs dans les sous-formules parenthésées
    # Ceci devient rapidement complexe. Pour cette démo, on suppose des structures simples.
    if '→' in formula_str:
        split_pos = formula_str.rfind('→') # Prend le dernier pour associativité à droite
        op_symbol = '→'
        left = parse_simple_formula(formula_str[:split_pos].strip())
        right = parse_simple_formula(formula_str[split_pos+1:].strip())
        return Implies(left, right)

    if '∨' in formula_str:
        split_pos = formula_str.rfind('∨')
        op_symbol = '∨'
        left = parse_simple_formula(formula_str[:split_pos].strip())
        right = parse_simple_formula(formula_str[split_pos+1:].strip())
        return Or(left, right)

    if '∧' in formula_str:
        split_pos = formula_str.rfind('∧')
        op_symbol = '∧'
        left = parse_simple_formula(formula_str[:split_pos].strip())
        right = parse_simple_formula(formula_str[split_pos+1:].strip())
        return And(left, right)


    raise ValueError(f"Impossible de parser la formule simple : '{formula_str}'")
