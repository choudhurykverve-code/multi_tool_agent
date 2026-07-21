from langchain.tools import tool

from tools.calculator import(
    arithmetic_calculator,
    percentage_of,
    increase_percentage,
    decrease_percentage,
    find_percentage,
)


def _coerce_number(value):
    if isinstance(value, (int, float)):
        return value

    if isinstance(value, str):
        value = value.strip()
        if not value:
            return value
        try:
            return float(value)
        except ValueError:
            return value

    return value


@tool
def calculator_tool(
    operation: str,
    value1: float | str,
    value2: float | str | None = None
):
    """
    Perform arithmetic and percentage calculations.

    operation options and required inputs:
    - "arithmetic": value1 = full math expression as a string, e.g. "22.3 + 87.7" or "5 * (3 + 2)". value2 not used.
    - "percentage_of": value1 = percentage, value2 = total number
    - "increase_percentage": value1 = base number, value2 = percentage to increase by
    - "decrease_percentage": value1 = base number, value2 = percentage to decrease by
    - "find_percentage": value1 = part, value2 = whole
    """

    value1 = _coerce_number(value1)
    value2 = _coerce_number(value2) if value2 is not None else None

    if operation == "arithmetic":
        return arithmetic_calculator(str(value1))

    elif operation == "percentage_of":
        if value2 is None:
            return "Error: Second value is required."
        return percentage_of(value1, value2)

    elif operation == "increase_percentage":
        if value2 is None:
            return "Error: Second value is required."
        return increase_percentage(value1, value2)

    elif operation == "decrease_percentage":
        if value2 is None:
            return "Error: Second value is required."
        return decrease_percentage(value1, value2)

    elif operation == "find_percentage":
        if value2 is None:
            return "Error: Second value is required."
        return find_percentage(value1, value2)

    else:
        return f"Error: Unsupported operation '{operation}'."

