from langchain.tools import tool
import math
import numexpr # Use numexpr for safe evaluation of math expressions

@tool
def calculator(expression: str) -> str:
  """
  Evaluates a mathematical expression.
  Use this tool for calculations involving numbers and basic math operations.
  Example: "2+2", "sqrt(144)", "(5*3)/2"
  """
  try:
      # Use numexpr for safer evaluation than eval()
      result = numexpr.evaluate(expression.strip("'\" "))
      return f"The result of '{expression}' is {result}"
  except Exception as e:
      return f"Error evaluating expression '{expression}': {e}. Please provide a valid mathematical expression."

# You might want to refine the error handling or input validation