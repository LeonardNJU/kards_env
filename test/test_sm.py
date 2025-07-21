class A:
    def __init__(self):
        self.x = 1

    def method(self):
        return self.x
    
class B:
    def __init__(self):
        self.y = 2

    def method(self):
        return self.y
    
C=A
result = C().method()  # This will call A's method
print(result)  # Output: 1