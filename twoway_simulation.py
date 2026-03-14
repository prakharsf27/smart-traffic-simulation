import pygame
import random
import sys
import matplotlib.pyplot as plt

pygame.init()

# -------------------------------------------------
# WINDOW
# -------------------------------------------------
WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Smart City Traffic Simulator")
clock = pygame.time.Clock()

# -------------------------------------------------
# COLORS
# -------------------------------------------------
WHITE = (255,255,255)
GRAY = (120,120,120)
RED = (255,0,0)
GREEN = (0,200,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
ORANGE = (255,140,0)

font = pygame.font.SysFont(None,24)

# -------------------------------------------------
# CITY GRID
# -------------------------------------------------
GRID = 4                 # 4x4 intersections
ROAD_W = 70
CELL = WIDTH // (GRID+1)

# choose signal control mode: "AI" or "FIXED"
FIXED_CYCLE = 120

# vehicle scaling
MAX_CARS = 200
SPAWN_BATCH = random.randint(3,6)

intersections = []

# -------------------------------------------------
# SIGNAL CLASS
# -------------------------------------------------
class Signal:

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.state = "NS"
        self.timer = 0
        self.MIN_GREEN = 40
        self.fixed_timer = 0

    def fixed_control(self):
        self.fixed_timer += 1
        if self.fixed_timer > FIXED_CYCLE:
            if self.state == "NS":
                self.state = "EW"
            else:
                self.state = "NS"
            self.fixed_timer = 0

    def decide(self,cars):

        self.timer += 1

        ns = 0
        ew = 0
        emergency_ns = False
        emergency_ew = False

        # camera detection zone (expanded)
        for car in cars:
            if car.target == self:

                if car.direction == "NS" and abs(car.y - self.y) < 160:
                    ns += 1
                    if car.type == "ambulance":
                        emergency_ns = True

                if car.direction == "EW" and abs(car.x - self.x) < 160:
                    ew += 1
                    if car.type == "ambulance":
                        emergency_ew = True

        # Emergency priority
        if emergency_ns:
            self.state = "NS"
            self.timer = 0
            return

        if emergency_ew:
            self.state = "EW"
            self.timer = 0
            return

        # Density difference (pressure)
        pressure = ns - ew

        # adaptive green time grows with queue size
        adaptive_green = 25 + min(max(ns, ew) * 6, 120)

        # if current direction still has heavy traffic keep it green longer
        if self.state == "NS" and ns > ew:
            adaptive_green += min(ns * 2, 60)

        if self.state == "EW" and ew > ns:
            adaptive_green += min(ew * 2, 60)

        # don't switch too early
        if self.timer < adaptive_green:
            return

        # choose direction with higher density
        if pressure > 0:
            new_state = "NS"
        else:
            new_state = "EW"

        if new_state != self.state:
            self.state = new_state
            self.timer = 0

    def draw(self):

        ns_color = GREEN if self.state == "NS" else RED
        ew_color = GREEN if self.state == "EW" else RED

        # north signal
        pygame.draw.circle(screen, ns_color, (self.x, self.y-30), 8)

        # south signal
        pygame.draw.circle(screen, ns_color, (self.x, self.y+30), 8)

        # west signal
        pygame.draw.circle(screen, ew_color, (self.x-30, self.y), 8)

        # east signal
        pygame.draw.circle(screen, ew_color, (self.x+30, self.y), 8)


# create grid intersections
for i in range(GRID):
    for j in range(GRID):

        x = (j+1)*CELL
        y = (i+1)*CELL

        intersections.append(Signal(x,y))


# -------------------------------------------------
# CAR AGENT
# -------------------------------------------------
class Car:

    def __init__(self):

        self.direction = random.choice(["NS","EW"])
        self.speed = random.randint(2,4)
        self.wait = 0

        self.start_time = simulation_time
        self.crossed = False

        # choose random target intersection
        self.target = random.choice(intersections)

        # vehicle type
        self.type = random.choice(["car","bus","truck","ambulance"])

        if self.type == "car":
            self.color = BLUE
        elif self.type == "bus":
            self.color = ORANGE
        elif self.type == "truck":
            self.color = BLACK
        else:
            self.color = (255,0,255)  # ambulance (magenta)

        if self.direction == "NS":
            lane_offset = random.choice([-12, 12])
            self.x = self.target.x + lane_offset
            self.y = -40
            self.w = 20
            self.h = 40
        else:
            lane_offset = random.choice([-12, 12])
            self.x = -40
            self.y = self.target.y + lane_offset
            self.w = 40
            self.h = 20

    def move(self):

        stop = False

        # simple car-following rule to avoid overlap
        for other in cars:
            if other is self:
                continue

            if self.direction == other.direction:
                if self.direction == "NS" and abs(self.x - other.x) < 10:
                    if 0 < other.y - self.y < 50:
                        stop = True

                if self.direction == "EW" and abs(self.y - other.y) < 10:
                    if 0 < other.x - self.x < 50:
                        stop = True

        if self.direction == "NS":

            if self.y + self.h >= self.target.y - 35 and self.y < self.target.y:
                if self.target.state != "NS":
                    stop = True

            if stop:
                self.wait += 1
            else:
                self.y += self.speed

            # detect crossing the signal
            if not self.crossed and self.y > self.target.y:
                if current_mode == "AI":
                    travel_times_ai.append(simulation_time - self.start_time)
                else:
                    travel_times_fixed.append(simulation_time - self.start_time)
                self.crossed = True

        else:

            if self.x + self.w >= self.target.x - 35 and self.x < self.target.x:
                if self.target.state != "EW":
                    stop = True

            if stop:
                self.wait += 1
            else:
                self.x += self.speed

            # detect crossing the signal
            if not self.crossed and self.x > self.target.x:
                if current_mode == "AI":
                    travel_times_ai.append(simulation_time - self.start_time)
                else:
                    travel_times_fixed.append(simulation_time - self.start_time)
                self.crossed = True

    def draw(self):
        pygame.draw.rect(screen,self.color,(self.x,self.y,self.w,self.h))


# -------------------------------------------------
# GLOBAL STATE
# -------------------------------------------------
cars = []
travel_times_ai = []
travel_times_fixed = []
simulation_time = 0


# -------------------------------------------------
# DRAW CITY
# -------------------------------------------------
def draw_city():

    screen.fill(WHITE)

    # draw horizontal roads
    for i in range(GRID):
        pygame.draw.rect(screen,GRAY,(0,(i+1)*CELL-ROAD_W//2,WIDTH,ROAD_W))

    # draw vertical roads
    for i in range(GRID):
        pygame.draw.rect(screen,GRAY,((i+1)*CELL-ROAD_W//2,0,ROAD_W,HEIGHT))

    for signal in intersections:
        signal.draw()

    for car in cars:
        car.draw()


# -------------------------------------------------
# SIMULATION FUNCTION
# -------------------------------------------------

def run_simulation(mode):

    global cars, simulation_time, current_mode

    current_mode = mode

    cars = []
    simulation_time = 0

    running = True

    while running:

        clock.tick(60)
        simulation_time += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if len(cars) < MAX_CARS:
            batch = random.randint(3,6)
            for _ in range(batch):
                cars.append(Car())

        for signal in intersections:
            if mode == "AI":
                signal.decide(cars)
            else:
                signal.fixed_control()

        for car in cars:
            car.move()

        cars = [c for c in cars if c.x < WIDTH and c.y < HEIGHT]

        draw_city()

        screen.blit(font.render(f"Mode: {mode}",True,BLACK),(20,20))
        screen.blit(font.render(f"Cars: {len(cars)} / {MAX_CARS}",True,BLACK),(20,45))

        pygame.display.update()

        # stop after enough samples collected for the current mode
        if mode == "FIXED" and len(travel_times_fixed) > 200:
            running = False

        if mode == "AI" and len(travel_times_ai) > 200:
            running = False


# run fixed signal simulation
run_simulation("FIXED")

# reset intersections
for s in intersections:
    s.state = "NS"
    s.timer = 0
    s.fixed_timer = 0

# run AI simulation
run_simulation("AI")

pygame.quit()

# Plot comparison graph
plt.figure(figsize=(8,5))

if travel_times_ai:
    plt.plot(travel_times_ai, label="AI Signal", alpha=0.8)

if travel_times_fixed:
    plt.plot(travel_times_fixed, label="Fixed Signal", alpha=0.8)

plt.title("AI vs Fixed Signal: Vehicle Time to Cross")
plt.xlabel("Vehicle Index")
plt.ylabel("Time Steps to Cross")
plt.legend()
plt.grid(True)
plt.show()

sys.exit()
