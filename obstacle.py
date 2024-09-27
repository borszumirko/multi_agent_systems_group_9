import pygame

class Obstacle():
    def __init__(self, left, top, width, height):
        self.left = left
        self.top = top
        self.height = height
        self.width = width
        self.center = pygame.Vector2(left + width // 2, top + height // 2)

    def away_from_obst(self, agent_x, agent_y):
        vector = pygame.Vector2(agent_x - self.center.x, agent_y - self.center.y)
        return vector, vector.length()

    def draw(self, screen):
        pygame.draw.rect(screen, (208, 184, 48), (self.left, self.top, self.width, self.height))