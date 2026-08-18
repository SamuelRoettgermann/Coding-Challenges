import ctypes

def dereference(address: int) -> object:
    return ctypes.cast(address, ctypes.py_object).value

variable = "monke"
print(f"{variable = }")
print(f"{id(variable) = }")
print(f"{dereference(id(variable)) = }")