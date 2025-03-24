import pygame
import random
import math
import colorsys
from collision_ball import CollisionBall
import collections

SCREEN_WIDTH = 2050
SCREEN_HEIGHT = 1150
TRAIL_AMOUNT = 10

FPS = 110
BALLS_AMOUNT = 1

GRAVITY = 0.2
FRICTION = 0.004
RESTITUTION = 0.8

VELOCITY_SLEEP_EPSILON = 0.05

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.balls = [
            CollisionBall(
                center=(
                    random.uniform(r := random.uniform(10, 100), SCREEN_WIDTH - r),
                    random.uniform(r, SCREEN_HEIGHT - r)
                ),
                velocity=(random.uniform(-5, 5), random.uniform(-5, 5)),
                radius=r,
                mass=r,
                color=(
                    lambda hue: tuple(
                        int(c * 255) for c in colorsys.hsv_to_rgb(hue / 360.0, 1.0, 1.0)
                    )
                )(
                    (r - 5) / (50 - 5) * 270
                )
            )
            for _ in range(BALLS_AMOUNT)
        ]

        self.dragging_ball = None
        self.drag_offset = (0, 0)
        self.last_mouse_pos = None

        self.creating_ball = None
        self.create_start_time = None

        for ball in self.balls:
            ball.trail = collections.deque(maxlen=TRAIL_AMOUNT)

    def run(self) -> None:
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            print(f"FPS: {self.clock.get_fps():.2f}")
        pygame.quit()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                clicked_on_ball = False

                for ball in reversed(self.balls):
                    dx = mouse_pos[0] - ball.center[0]
                    dy = mouse_pos[1] - ball.center[1]
                    if (dx*dx + dy*dy) <= (ball.radius * ball.radius):
                        self.dragging_ball = ball
                        self.drag_offset = (ball.center[0] - mouse_pos[0],
                                            ball.center[1] - mouse_pos[1])
                        self.last_mouse_pos = mouse_pos
                        if hasattr(ball, "trail"):
                            ball.trail.clear()

                        clicked_on_ball = True
                        break

                if not clicked_on_ball:
                    self.creating_ball = CollisionBall(
                        center=mouse_pos,
                        velocity=(0, 0),
                        radius=10,
                        mass=10,
                        color=(255, 255, 255)
                    )
                    self.create_start_time = pygame.time.get_ticks()

                    self.dragging_ball = self.creating_ball
                    self.drag_offset = (0, 0)
                    self.last_mouse_pos = mouse_pos

                    self.balls.append(self.creating_ball)
                    self.creating_ball.trail = collections.deque(maxlen=TRAIL_AMOUNT)

            elif event.type == pygame.MOUSEBUTTONUP:
                if self.dragging_ball:
                    if self.creating_ball is self.dragging_ball:
                        hold_time = pygame.time.get_ticks() - self.create_start_time
                        final_radius = 10 + (hold_time * 0.02)
                        self.creating_ball.radius = final_radius
                        self.creating_ball.mass = final_radius

                        hue = (final_radius - 5) / (50 - 5) * 270
                        hue = max(0, min(hue, 270))
                        self.creating_ball.color = tuple(
                            int(c * 255) for c in colorsys.hsv_to_rgb(hue / 360.0, 1.0, 1.0)
                        )

                        self.creating_ball = None
                        self.create_start_time = None

                    self.dragging_ball = None
                    self.drag_offset = (0, 0)
                    self.last_mouse_pos = None

            elif event.type == pygame.MOUSEMOTION:
                if self.dragging_ball:
                    mouse_pos = event.pos
                    new_center_x = mouse_pos[0] + self.drag_offset[0]
                    new_center_y = mouse_pos[1] + self.drag_offset[1]

                    r = self.dragging_ball.radius
                    new_center_x = max(r, min(new_center_x, SCREEN_WIDTH - r))
                    new_center_y = max(r, min(new_center_y, SCREEN_HEIGHT - r))

                    self.dragging_ball.center = (new_center_x, new_center_y)

                    if self.last_mouse_pos is not None:
                        dx = mouse_pos[0] - self.last_mouse_pos[0]
                        dy = mouse_pos[1] - self.last_mouse_pos[1]
                        self.dragging_ball.velocity = (dx, dy)

                    self.last_mouse_pos = mouse_pos

    def update(self) -> None:
        if self.creating_ball and self.create_start_time is not None:
            hold_time = pygame.time.get_ticks() - self.create_start_time
            new_radius = 10 + (hold_time * 0.02)
            self.creating_ball.radius = new_radius
            self.creating_ball.mass = new_radius

            hue = (new_radius - 5) / (50 - 5) * 270
            hue = max(0, min(hue, 270))
            self.creating_ball.color = tuple(
                int(c * 255) for c in colorsys.hsv_to_rgb(hue / 360.0, 1.0, 1.0)
            )

        for ball in self.balls:
            if ball is self.dragging_ball:
                continue

            vx, vy = ball.velocity
            cx, cy = ball.center

            vy += GRAVITY

            cx += vx
            cy += vy

            if (cx + ball.radius >= SCREEN_WIDTH and vx > 0) or \
               (cx - ball.radius <= 0 and vx < 0):
                vx *= -1 * RESTITUTION
                cx = max(ball.radius, min(cx, SCREEN_WIDTH - ball.radius))

            if (cy + ball.radius >= SCREEN_HEIGHT and vy > 0) or \
               (cy - ball.radius <= 0 and vy < 0):
                vy *= -1 * RESTITUTION
                cy = max(ball.radius, min(cy, SCREEN_HEIGHT - ball.radius))

            if cy + ball.radius >= SCREEN_HEIGHT - 0.5:
                if abs(vy) < VELOCITY_SLEEP_EPSILON:
                    vy = 0
                    cy = SCREEN_HEIGHT - ball.radius
                if vx > 0:
                    vx = max(0, vx - FRICTION)
                elif vx < 0:
                    vx = min(0, vx + FRICTION)

            ball.velocity = (vx, vy)
            ball.center = (cx, cy)

            if (vx != 0 or vy != 0):
                ball.trail.append(ball.center)

        for i in range(len(self.balls)):
            for j in range(i+1, len(self.balls)):
                b1 = self.balls[i]
                b2 = self.balls[j]

                dx = b2.center[0] - b1.center[0]
                dy = b2.center[1] - b1.center[1]
                dist_sq = dx*dx + dy*dy
                sum_r = b1.radius + b2.radius

                if dist_sq <= sum_r * sum_r:
                    distance = math.sqrt(dist_sq)
                    if distance == 0:
                        continue
                    overlap = sum_r - distance
                    if overlap < 0:
                        continue

                    nx = dx / distance
                    ny = dy / distance

                    vx1, vy1 = b1.velocity
                    vx2, vy2 = b2.velocity

                    rvx = vx2 - vx1
                    rvy = vy2 - vy1
                    vel_along_normal = rvx * nx + rvy * ny

                    if vel_along_normal > 0:
                        continue

                    e = RESTITUTION
                    m1 = b1.mass
                    m2 = b2.mass

                    if b1 is self.dragging_ball:
                        m1 = 999999999
                    if b2 is self.dragging_ball:
                        m2 = 999999999

                    impulse_mag = -(1 + e) * vel_along_normal
                    impulse_mag /= (1 / m1 + 1 / m2)
                    ix = impulse_mag * nx
                    iy = impulse_mag * ny

                    vx1 -= (ix / m1)
                    vy1 -= (iy / m1)
                    vx2 += (ix / m2)
                    vy2 += (iy / m2)

                    total_mass = m1 + m2
                    if total_mass == 0:
                        move1 = move2 = overlap * 0.5
                    else:
                        move1 = (m2 / total_mass) * overlap
                        move2 = (m1 / total_mass) * overlap

                    b1cx, b1cy = b1.center
                    b2cx, b2cy = b2.center

                    b1cx -= nx * move1
                    b1cy -= ny * move1
                    b2cx += nx * move2
                    b2cy += ny * move2

                    if b1 is not self.dragging_ball:
                        b1.center = (b1cx, b1cy)
                        b1.trail.append(b1.center)
                    if b2 is not self.dragging_ball:
                        b2.center = (b2cx, b2cy)
                        b2.trail.append(b2.center)

                    b1.velocity = (vx1, vy1)
                    b2.velocity = (vx2, vy2)

        if self.dragging_ball:
            cx, cy = self.dragging_ball.center
            r = self.dragging_ball.radius
            clamped_cx = max(r, min(cx, SCREEN_WIDTH - r))
            clamped_cy = max(r, min(cy, SCREEN_HEIGHT - r))
            self.dragging_ball.center = (clamped_cx, clamped_cy)

        for ball in self.balls:
            vx, vy = ball.velocity
            if abs(vx) < VELOCITY_SLEEP_EPSILON:
                vx = 0
            if abs(vy) < VELOCITY_SLEEP_EPSILON:
                vy = 0
            ball.velocity = (vx, vy)

    def draw(self) -> None:
        self.screen.fill("black")

        for ball in self.balls:
            trail_list = list(ball.trail)
            for i, (px, py) in enumerate(trail_list):
                alpha = int(128 * ((i + 1) / len(trail_list)))

                trail_surf = pygame.Surface((2 * ball.radius, 2 * ball.radius), pygame.SRCALPHA)
                pygame.draw.circle(
                    trail_surf,
                    (ball.color[0] *0.5, ball.color[1]*0.5, ball.color[2]*0.5, alpha),
                    (ball.radius, ball.radius),
                    int(ball.radius)
                )
                self.screen.blit(trail_surf, (px - ball.radius, py - ball.radius))

        for ball in self.balls:
            pygame.draw.circle(
                self.screen,
                ball.color,
                (int(ball.center[0]), int(ball.center[1])),
                int(ball.radius)
            )

        pygame.display.flip()
