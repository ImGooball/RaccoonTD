import pygame
from src.entities.tower import Tower
from src.entities.enemy import Enemy
from src.entities.button import Button
from src.game.stages import stages

COLUMN_WIDTH = 200  # Width of the side column

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.towers = []
        self.enemies = []
        self.phase = 0  # 0: Stage selection, 1: Placement phase, 2: Combat phase
        self.currency = 100
        self.health = 10
        self.spawn_interval = 1000
        self.spawn_timer = 0
        self.spawn_duration = 10000
        self.start_time = pygame.time.get_ticks()
        self.round_active = False
        self.selected_tower = None
        self.current_stage = None
        self.current_round = 1
        self.total_rounds = 50
        self.start_button = Button(820, 50, 150, 50, "Start Round", self.start_round)
        self.restart_button = Button(820, 150, 150, 50, "Restart", self.restart_game)

    def start_round(self):
        if self.phase == 1:
            print(f"Starting round {self.current_round}")
            self.round_active = True
            self.start_time = pygame.time.get_ticks()
            self.spawn_timer = self.start_time
            self.enemies = []
            self.phase = 2  # Switch to combat phase

    def restart_game(self):
        print("Restarting game")
        self.enemies = []
        self.towers.clear()
        self.start_time = pygame.time.get_ticks()
        self.spawn_timer = self.start_time
        self.health = 10
        self.currency = 100
        self.phase = 0
        self.round_active = False
        self.selected_tower = None
        self.current_round = 1

    def is_overlapping(self, x, y):
        new_rect = pygame.Rect(x - 32, y - 32, 64, 64)
        for tower in self.towers:
            if new_rect.colliderect(tower.rect):
                return True
        return False

    def handle_event(self, event):
        if self.phase == 0:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 100 < x < 300 and 200 < y < 250:
                    self.current_stage = "Stage 1"
                    print("Selected Stage 1")
                    self.phase = 1
                elif 100 < x < 300 and 300 < y < 350:
                    self.current_stage = "Stage 2"
                    print("Selected Stage 2")
                    self.phase = 1
        elif self.phase == 1:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                tower_clicked = False
                for tower in self.towers:
                    if tower.rect.collidepoint(x, y):
                        self.selected_tower = tower
                        tower_clicked = True
                        break
                if not tower_clicked:
                    self.selected_tower = None

                if x < 800 and not self.is_overlapping(x, y) and self.currency >= 50:  # Assume tower cost is 50 and x < 800 prevents placing in column
                    self.towers.append(Tower(x, y))
                    self.currency -= 50
                    print(f"Placed tower at ({x}, {y})")
                self.start_button.is_clicked(event)
            self.restart_button.is_clicked(event)
        elif self.phase == 2:
            self.restart_button.is_clicked(event)

    def update(self, current_time):
        if self.phase == 2:
            if self.round_active:
                # Spawn enemies for a set amount of time
                if current_time - self.start_time < self.spawn_duration:
                    if current_time - self.spawn_timer > self.spawn_interval:
                        new_enemy = Enemy(stages[self.current_stage][0][0], stages[self.current_stage][0][1], 2)
                        new_enemy.set_path(stages[self.current_stage])
                        self.enemies.append(new_enemy)
                        self.spawn_timer = current_time
                        print("Spawned enemy")

                # Move enemies along the path
                for enemy in self.enemies:
                    if len(enemy.path) == 0:
                        continue
                    target_x, target_y = enemy.path[0]
                    direction = pygame.math.Vector2(target_x - enemy.rect.centerx, target_y - enemy.rect.centery)
                    if direction.length() > enemy.speed:
                        direction = direction.normalize() * enemy.speed
                        enemy.rect.move_ip(direction)
                    else:
                        enemy.rect.center = (target_x, target_y)
                        enemy.path.pop(0)
                        if len(enemy.path) == 0 and enemy.rect.center == stages[self.current_stage][-1]:
                            self.health -= 1
                            print("Enemy reached the end, lost health")
                            self.enemies.remove(enemy)

                # Towers attack and update projectiles
                for tower in self.towers:
                    tower.attack(self.enemies, current_time)
                    tower.update_projectiles(self.screen)

                # Remove dead enemies
                for enemy in self.enemies[:]:
                    if enemy.health <= 0:
                        self.enemies.remove(enemy)
                        self.currency += 10  # Reward for killing an enemy
                        print("Enemy killed, gained currency")

                if not self.enemies and current_time - self.start_time >= self.spawn_duration:
                    print("Round ended")
                    self.round_active = False
                    self.current_round += 1
                    if self.current_round > self.total_rounds:
                        print("You won!")
                        self.restart_game()
                    else:
                        self.phase = 1  # Return to placement phase

    def draw(self):
        self.screen.fill((0, 0, 0))

        # Draw entities
        for tower in self.towers:
            tower.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)

        # Draw the path for the current stage
        if self.current_stage:
            for point in stages[self.current_stage]:
                pygame.draw.circle(self.screen, (255, 255, 255), point, 5)
            pygame.draw.lines(self.screen, (255, 255, 255), False, stages[self.current_stage], 2)

        # Draw the side column
        pygame.draw.rect(self.screen, (50, 50, 50), (800, 0, COLUMN_WIDTH, 600))

        # Draw selected tower range
        if self.selected_tower:
            pygame.draw.circle(self.screen, (0, 0, 255, 100), self.selected_tower.rect.center, self.selected_tower.range, 1)

        # Draw UI elements
        if self.phase == 0:
            font = pygame.font.SysFont(None, 50)
            stage1_text = font.render("Stage 1", True, (255, 255, 255))
            stage2_text = font.render("Stage 2", True, (255, 255, 255))
            self.screen.blit(stage1_text, (100, 200))
            self.screen.blit(stage2_text, (100, 300))
        elif self.phase == 1:
            self.start_button.draw(self.screen)
        self.restart_button.draw(self.screen)

        # Draw currency and health
        if self.phase != 0:
            font = pygame.font.SysFont(None, 40)
            currency_text = font.render(f"Currency: {self.currency}", True, (255, 255, 255))
            health_text = font.render(f"Health: {self.health}", True, (255, 255, 255))
            round_text = font.render(f"Round: {self.current_round}/{self.total_rounds}", True, (255, 255, 255))
            self.screen.blit(currency_text, (10, 10))
            self.screen.blit(health_text, (10, 50))
            self.screen.blit(round_text, (10, 90))
