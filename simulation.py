import pygame
import random


pygame.init()
WIDTH, HEIGHT = 900, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Traffic Flow & Congestion Simulator - Phase 1")
clock = pygame.time.Clock()


class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.target_y = y
        self.change_speed = 2.5
        self.width = 16
        self.height = 10
        self.max_speed = random.uniform(2.0, 5.5)
        self.speed= self.max_speed
        
        
        self.speed = random.uniform(2.0, 5.5)
        
        
        if self.speed > 4.0:
            self.color = (255, 70, 70)
        elif self.speed > 3.0:
            self.color = (255, 200, 0)
        else:
            self.color = (70, 150, 255)


    def try_overtake(self, cars):
        if self.y != self.target_y:
            return
        
        BARRIER_X = 500
        BLOCKED_Y = 240

        possible_lanes = []
        if self.y > 180:
            possible_lanes.append(self.y - 60)
        if self.y < 300:
            possible_lanes.append(self.y + 60)

        for target_y in possible_lanes:
            if target_y == BLOCKED_Y and self.x > (BARRIER_X - 60):
                continue

            lane_clear = True
            for other in cars:
                if other != self and (other.y == target_y or other.target_y == target_y):
                    if abs(other.x - self.x) < 85:
                        lane_clear = False
                        break

            if lane_clear:
                self.target_y = target_y
                break

    def update(self, cars):
        BARRIER_X = 500
        BLOCKED_Y = 240

        if self.y < self.target_y:
            self.y = min(self.y + self.change_speed, self.target_y)
        elif self.y > self.target_y:
            self.y = max(self.y - self.change_speed, self.target_y)


        self.speed = self.max_speed

        if (self.y == BLOCKED_Y or self.target_y == BLOCKED_Y) and 0 < (BARRIER_X - self.x) < 150:
            self.try_overtake(cars)

            if self.target_y == BLOCKED_Y and 0 < (BARRIER_X - self.x) < 35:
                self.speed = 0
        
        for other in cars:
            if other != self:
                
                same_lane = (abs(self.target_y - other.target_y) < 10 or 
                             abs(self.y - other.y) < 25 or 
                             abs(self.target_y - other.y) < 25)
                
                if same_lane:
                    distance = other.x - self.x
                    
                    if 0 < distance < 45:
                        self.try_overtake(cars)
                        
                        self.speed = min(self.speed, other.speed)
                    
                    if 0 < distance < 20:
                        self.speed = min(self.speed, max(0, other.speed - 0.5))
        

        self.x += self.speed

        
        if self.x > WIDTH:
    
            available_lanes = [180, 240, 300]
            random.shuffle(available_lanes)
            
            selected_lane = available_lanes[0] 
            for lane in available_lanes:
                lane_clear = True
                for other in cars:
                    if other != self and (other.y == lane or other.target_y == lane):
                        
                        if other.x < 50:
                            lane_clear = False
                            break
                if lane_clear:
                    selected_lane = lane
                    break

            self.x = -self.width
            self.y = selected_lane
            self.target_y = selected_lane

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (int(self.x), int(self.y), self.width, self.height))


lanes = [180, 240, 300]


cars = []
for _ in range(35):
    lane_y = random.choice(lanes) 
    cars.append(Car(random.randint(-WIDTH, WIDTH), lane_y))


running = True
while running:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    for car in cars:
        car.update(cars)

    
    screen.fill((30, 30, 35))
    

    pygame.draw.line(screen, (100, 100, 100), (0, 150), (WIDTH, 150), 2)
    pygame.draw.line(screen, (100, 100, 100), (0, 350), (WIDTH, 350), 2)
    pygame.draw.rect(screen, (255, 100, 0), (500, 235, 40, 20))
    
    for car in cars:
        car.draw(screen)

    pygame.display.flip()

pygame.quit()