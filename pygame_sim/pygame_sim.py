import pygame as pg
import numpy as np

GRAVITY_CONSTANT = 1

dt = 0.05

to_remove = []

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
            distance = np.sqrt(np.linalg.norm(r)**2 + epsilon**2)

            if distance == 0:
              continue
            elif distance < 10:
                if self not in to_remove:
                  total_mass = self.mass + body.mass

                  self.velocity = (
                    self.mass * self.velocity +
                    body.mass * body.velocity
                    ) / total_mass

                  self.mass = total_mass
                  to_remove.append(body)
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
    time = int(input("How many seconds: "))
    bodies_num = int(input("How many bodies: "))

    for i in range(bodies_num):
        mass = float(input("Enter the mass of body: "))
        x = int(input("Enter the x of body: "))
        y = int(input("Enter the y of body: "))

        bodies.append(Body(mass, x, y))

    return time

def main():
    time = askBodies()
    running = True  

    pg.font.init()
    font = pg.font.SysFont("Arial", 20)

    window = pg.display.set_mode((500, 500))
    pg.display.set_caption("SIMULATION") 

    clock = pg.time.Clock()
    elapsed = 0 
    while running and elapsed < time:

          dt_real = clock.tick(240) / 1000
          elapsed += dt_real

          for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

          window.fill((0,0,0))

          time_text = font.render(f"Time: {elapsed:.2f}s", True, (255,255,255))
          window.blit(time_text, (10, 10))

          for body in bodies:
            body.calculatePosition()

          for body in to_remove:
              if body in bodies:
                bodies.remove(body)

          to_remove.clear()
    
          for body in bodies:
            body.updateVel()
            
          for body in bodies:
                  body.updatePos()

                  pg.draw.circle(window, (255, 255, 255), body.position.astype(int), 5)

          pg.display.update()

main()