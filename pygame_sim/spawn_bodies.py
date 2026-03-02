import pygame as pg
import numpy as np
import random

GRAVITY_CONSTANT = 1

dt = 0.05

to_remove = []

time = int(input("How many seconds: "))
bodies_num = int(input("How many bodies: "))
min_mass = float(input("minimum mass of each body: "))
max_mass = float(input("maximum mass of each body: "))
min_shiftx = float(input("minimum shift in x direction: "))
max_shiftx = float(input("maximum shift in x direction: "))
min_shifty = float(input("minimum shift in y direction: "))
max_shifty = float(input("maximum shift in y direction: "))

class Body:
    def __init__(self, mass, x, y, shiftx, shifty):
        self.mass = mass

        self.size = (self.mass ** (1/3)) * 0.8

        self.x = x
        self.y = y

        self.shiftx = shiftx
        self.shifty = shifty

        self.velocity = np.array([self.shiftx, self.shifty], dtype=float)
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
            elif distance < (self.size + body.size):
              if self not in to_remove:
                total_mass = self.mass + body.mass

                self.velocity = (
                  self.mass * self.velocity +
                  body.mass * body.velocity
                  ) / total_mass

                self.mass = total_mass
                self.size = (self.mass ** (1/3)) * 0.8
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
        self.velocity = self.velocity + acceleration * dt


bodies = []

def askBodies():

    for i in range(bodies_num):
        mass = random.uniform(min_mass, max_mass)
        x = random.randint(0, 499)
        y = random.randint(0, 499)
        shiftx = random.uniform(min_shiftx, max_shiftx)
        shifty = random.uniform(min_shifty, max_shifty)

        bodies.append(Body(mass, x, y, shiftx, shifty))

    return time

def spawnBody(x, y):
    bodies.append(Body(random.uniform(min_mass, max_mass), int(x), int(y), random.uniform(min_shiftx, max_shiftx), random.uniform(min_shifty, max_shifty)))

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
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                spawnBody(mouse_pos[0], mouse_pos[1])

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

                  pg.draw.circle(window, (255, 255, 255), body.position.astype(int), body.size)

          pg.display.update()

main()