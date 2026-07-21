import ast
import operator

OPERATORS= {
    ast.Add:operator.add,
    ast.Sub:operator.sub,
    ast.Mult:operator.mul,
    ast.Div:operator.truediv,
    ast.Mod:operator.mod,
    ast.Pow:operator.pow,
    ast.USub:operator.neg,
    ast.UAdd:operator.pos
}

OPERATOR_NAMES = {
    ast.FloorDiv: "//",
    ast.LShift: "<<",
    ast.RShift: ">>",
    ast.BitAnd: "&",
    ast.BitOr: "|",
    ast.BitXor: "^",
}

def arithmetic_calculator(expression:str)-> int | float | str:

    if not isinstance(expression,str):
        return "Error: Expression must be string"

    expression = expression.strip()

    if not expression:
        return "Error: Expression is empty"

    expression = (
        expression.replace("x","*").replace("÷","/").replace("^","**").replace("×", "*")
    )

    try:
        tree = ast.parse(expression,mode="eval")
        return evaluate(tree.body)
    
    except SyntaxError:
        return "Error: Invalid Expression"

    except ZeroDivisionError:
        return "Error: Division by zero"

    except ValueError as e:
        return f"Error: {e}"

    except Exception as e:
        return f"Unexpected error: {e}"


def evaluate(node):

    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only numeric values are supported.")

    if isinstance(node, ast.BinOp):

        if type(node.op) not in OPERATORS:
            symbol = OPERATOR_NAMES.get(type(node.op), type(node.op).__name__)
            raise ValueError(f"Unsupported operator: {symbol}")
        
        left = evaluate(node.left)
        right = evaluate(node.right)
        operator = OPERATORS[type(node.op)]
        return operator(left,right)

    if isinstance(node, ast.UnaryOp):

        if type(node.op) not in OPERATORS:
            symbol = OPERATOR_NAMES.get(type(node.op), type(node.op).__name__)
            raise ValueError(f"Unsupported operator: {symbol}")
        
        operand = evaluate(node.operand)
        operator = OPERATORS[type(node.op)]
        return operator(operand)

    raise ValueError(f"Unsupported expression: {type(node).__name__}")



def percentage_of(percent: float, number: float) -> float:
    return (percent/100)*number

def increase_percentage(number: float, percent: float) -> float:
    return number + percentage_of(percent, number)

def decrease_percentage(number: float, percent: float) -> float:
    return number - percentage_of(percent, number)

def find_percentage(part: float, whole: float) -> float:
    if whole == 0:
        raise ValueError("Whole cannot be zero")
    return (part/whole)*100





