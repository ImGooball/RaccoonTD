import pygame
import sys
from tower import Tower
from enemy import Enemy
from button import Button

# Initialize Pygame
pygame.init()

# Set up the game window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Tower Defense Game")

# Set up the clock for frame rate
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TRANSPARENT_BLUE = (0, 0, 255, 100)

# Game entities
tower_position = (400, 300)
towers = []
enemies = []

# Game state variables
phase = 1  # 1: Placement phase, 2: Combat phase
currency = 100  # Starting currency
health = 10  # Player health
spawn_interval = 1000  # milliseconds
spawn_timer = 0
spawn_duration = 10000  # Total time to spawn enemies in milliseconds
start_time = pygame.time.get_ticks()
round_active = False
selected_tower = None
start_button = Button(300, 550, 200, 50, "Start Round", lambda: start_round())
restart_button = Button(600, 550, 200, 50, "Restart", lambda: restart_game())

def start_round():
    global round_active, start_time, spawn_timer, enemies, phase
    if phase == 1:
        print("Starting round")
        round_active = True
        start_time = pygame.time.get_ticks()
        spawn_timer = start_time
        enemies = []
        phase = 2  # Switch to combat phase

def restart_game():
    global enemies, start_time, spawn_timer, health, currency, phase, round_active, selected_tower
    print("Restarting game")
    enemies = []
    towers.clear()
    start_time = pygame.time.get_ticks()
    spawn_timer = start_time
    health = 10
    currency = 100
    phase = 1
    round_active = False
    selected_tower = None

def is_overlapping(x, y, towers):
    new_rect = pygame.Rect(x - 32, y - 32, 64, 64)
    for tower in towers:
        if new_rect.colliderect(tower.rect):
            return True
    return False

def main():
    global spawn_timer, phase, currency, health, round_active, selected_tower
    # Main game loop
    while True:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                tower_clicked = False
                for tower in towers:
                    if tower.rect.collidepoint(x, y):
                        selected_tower = tower
                        tower_clicked = True
                        break
                if not tower_clicked:
                    selected_tower = None

                if phase == 1:
                    if not is_overlapping(x, y, towers) and currency >= 50:  # Assume tower cost is 50
                        towers.append(Tower(x, y))
                        currency -= 50
                        print(f"Placed tower at ({x}, {y})")
                    start_button.is_clicked(event)
                restart_button.is_clicked(event)

        if phase == 2:
            if round_active:
                # Spawn enemies for a set amount of time
                if current_time - start_time < spawn_duration:
                    if current_time - spawn_timer > spawn_interval:
                        enemies.append(Enemy(tower_position[0], 0, 2))
                        spawn_timer = current_time
                        print("Spawned enemy")

                # Move enemies
                for enemy in enemies:
                    enemy.move()

                # Towers attack and update projectiles
                for tower in towers:
                    tower.attack(enemies)
                    tower.update_projectiles(screen)

                # Remove dead enemies
                for enemy in enemies[:]:
                    if enemy.health <= 0:
                        enemies.remove(enemy)
                        currency += 10  # Reward for killing an enemy
                        print("Enemy killed, gained currency")
                    elif enemy.rect.y >= screen.get_height():
                        enemies.remove(enemy)
                        health -= 1  # Penalty for letting an enemy escape
                        print("Enemy escaped, lost health")

                if not enemies and current_time - start_time >= spawn_duration:
                    print("Round ended, switching to placement phase")
                    phase = 1  # Return to placement phase
                    round_active = False

        # Fill the screen with a color
        screen.fill(BLACK)

        # Draw entities
        for tower in towers:
            tower.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)

        # Draw selected tower range
        if selected_tower:
            pygame.draw.circle(screen, TRANSPARENT_BLUE, selected_tower.rect.center, selected_tower.range, 1)

        # Draw UI elements
        if phase == 1:
            start_button.draw(screen)
        restart_button.draw(screen)

        # Draw currency and health
        font = pygame.font.SysFont(None, 40)
        currency_text = font.render(f"Currency: {currency}", True, WHITE)
        health_text = font.render(f"Health: {health}", True, WHITE)
        screen.blit(currency_text, (10, 10))
        screen.blit(health_text, (10, 50))

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

if __name__ == "__main__":
    main()
