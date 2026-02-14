Это библиотека с полезными инструментами для написания кода на python. Она ещё будет меняться и дополняться. А пока здесь есть только overload. Да, перегрузка в python.

# Пример использования overload

```python
from usefultools import overload

@overload()
def multiprint(text: str):
	print(text)

@overload()
def multiprint(text: str, number: int):
	for _ in range(number):
		print(text)

multiprint("Hello World!")
multiprint("Hello!", 2)
```

И первая и вторая функции сработают.
