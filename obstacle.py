import pygame

class Obstacle():
    def __init__(self, left, top, width, height, color=(208, 184, 48)):
        self.left = left
        self.top = top
        self.height = height
        self.width = width
        self.center = pygame.Vector2(left + width // 2, top + height // 2)
        self.color = color
        self.rect = pygame.Rect(self.left, self.top, self.width, self.height)

    def away_from_obst(self, agent_x, agent_y):
        ''' Returns a vector that points away from the obstacle towards the agent '''
        vector = pygame.Vector2(agent_x - self.center.x, agent_y - self.center.y)
        return vector, vector.length()

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.left, self.top, self.width, self.height))

    def is_in(self, position):
        return self.rect.collidepoint(position)

