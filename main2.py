import random
class Student:

 def __init__(self, name):
    self.name = name
    self.gladness = 50
    self.progress = 0
    self.money = 100
    self.alive = True
 def to_study(self):
    print("Time to study")
    self.progress += 0.2
    self.gladness -= 10
    self.money -= 15
 def to_sleep(self):
    print("I will sleep")
    self.gladness += 5
 def to_chill(self):
    print("Rest time")
    self.gladness += 5
    self.progress -= 0.1
    self.money -= 20
 def to_work(self):
     print('i am working')
     self.money += 60
 def is_alive(self):
     if self.progress < -1:
      print("Cast out...")
      self.alive = False
     elif self.gladness <= 0:
      print("Depression...")
      self.alive = False
     elif self.progress > 5:
      print("Passed externally...")
      self.alive = False
     elif self.money < 1:
         print('no money')
         self.alive = False

 def end_of_day(self):
    print(f"Gladness = {self.gladness}")
    print(f"Progress = {round(self.progress,                          2)}")
    print(f"money = {self.money} ")
 def live(self, day):
    day = "Day" +  str(day) +  "of"   +  self.name +           "life"
    print(f"{day:=^50}")
    if self.progress <= 0:
        print()
        self.to_study()
    elif self.gladness <= 10:
        self.to_chill() or self.to_sleep()
    elif self.money <= 10:
        self.to_work()
    elif self.progress > 0 and self.gladness >10 and self.money > 10:
        live_cube = random.randint(1, 4)
        if live_cube == 1:
            self.to_study()
        elif live_cube == 2:
            self.to_sleep()
        elif live_cube == 3:
            self.to_chill()
        elif self.money:
            self.to_work()
    self.end_of_day()
    self.is_alive()
nick = Student(name="Nick")
for day in range(365):
    if nick.alive == False:
        break
    nick.live(day)