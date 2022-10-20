print('hello world')
class Student:
 def __init__(self, height=160):
  self.height = height


nick = Student()
kate = Student(height=170)
print(nick.height)
print(kate.height)