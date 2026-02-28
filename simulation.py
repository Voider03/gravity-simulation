import pprint
import numpy as np

time = int(input("How many seconds: "))

space = [["", "", "", "", ""], 
        ["", "", "", "", ""], 
        ["", "", "", "", ""], 
        ["", "", "", "", ""], 
        ["", "", "", "", ""]]

GRAVITY_CONSTANT = 1

dt = 0.05

class Body:
    def __init__(self, mass, x, y):
        self.mass = mass
        self.x = x
        self.y = y

        self.dx = 0
        self.dy = 0

        self.velocity = np.array([self.dx, self.dy], dtype=float)
        self.position = np.array([self.x, self.y], dtype=float)

    def calculatePosition(self):
        self.force = np.array([0.0, 0.0])

        for body in bodies:
            if body == self:
                continue

            body_mass = body.mass
            body_position = body.position

            r = body_position - self.position
            epsilon = 0.1
            distance = np.linalg.norm(r) + epsilon

            if distance == 0:
              continue

            direction = r / distance
            gravity = self.calculateGravity(distance, body_mass)

            force = direction * gravity
            self.force += force
    
    def calculateGravity(self, distance, body_mass):
        return (GRAVITY_CONSTANT * body_mass * self.mass / distance ** 2)
    
    def updatePos(self):
        self.position += self.velocity * dt

    def updateVel(self):
        acceleration = self.force / self.mass
        self.velocity += acceleration * dt


bodies = []

def askBodies():
    bodies_num = int(input("How many bodies: "))

    for i in range(bodies_num):
        mass = int(input("Enter the mass of body: "))
        x = int(input("Enter the x of body: "))
        y = int(input("Enter the y of body: "))

        bodies.append(Body(mass, x, y))

def main():
    askBodies()
    for i in range(time):
      space = [["", "", "", "", ""], 
        ["", "", "", "", ""], 
        ["", "", "", "", ""], 
        ["", "", "", "", ""], 
        ["", "", "", "", ""]]

      for body in bodies:
        body.calculatePosition()
    
      for body in bodies:
        body.updateVel()

      for body in bodies:
        body.updatePos()

        x = round(body.position[0])
        y = round(body.position[1])

        if x > 4:
            x = 4
        elif x < 0:
            x = 0
        if y > 4:
            y = 4
        elif y < 0:
            y = 0

        if space[y][x] != "0":
          space[y][x] = "0"
      print("\n\n\n\n\n")

      pprint.pprint(space)

main()