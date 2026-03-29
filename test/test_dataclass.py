from dataclasses import dataclass,asdict

@dataclass
class myData:
    name: str
    age: int
    height: float

data1 = myData("Alice", 25, 1.75)
print(data1)
print(asdict(data1))
print(data1.__dict__)
print(data1.name)
print(data1.age)
print(data1.height)

