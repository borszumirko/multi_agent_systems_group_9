from constants import SUBGOAL_ZONES, AGENT_RADIUS, WIDTH, HEIGHT, BASE_ZONE
from obstacle import Obstacle
import pygame

# A zone counts as entered after being obstacle_padding pixels deep
obstacle_padding = 3

def find_subgoal(subgoal_indicator, agent_location):
    """
        Takes the subgoal-id and the location of the agent and gives back the direction to the nearest subgoal-zone.
        The subgoal-zones are predefined by the constants-file.
        If the subgoal is reached the second return will be True.
    """
    subgoals_dicts = SUBGOAL_ZONES[subgoal_indicator]
    subgoals = [Obstacle(**p) for p in subgoals_dicts]

    # Calculate smallest distance to subgoal-zones and pick zone
    min_distance = float('inf')
    target = None

    for subgoal in subgoals:
        subgoal_position = pygame.Vector2((subgoal.left + subgoal.width//2), (subgoal.top + subgoal.height//2))
        x_in = (subgoal.left < agent_location.x-AGENT_RADIUS-obstacle_padding) and ((subgoal.left + subgoal.width) >= agent_location.x+AGENT_RADIUS+obstacle_padding)
        y_in = (subgoal.top < agent_location.y-AGENT_RADIUS-obstacle_padding) and ((subgoal.top + subgoal.height) >= agent_location.y+AGENT_RADIUS+obstacle_padding)
        if x_in and y_in:
            return subgoal_position, True
        
        
        if am_i_stuck(agent_location, subgoal_indicator):
            subgoal_target, _ = find_subgoal(subgoal_indicator-1, agent_location)
        else:
            if x_in:
                subgoal_target = pygame.Vector2(agent_location.x, subgoal_position.y)
            elif y_in:
                subgoal_target = pygame.Vector2(subgoal_position.x, agent_location.y)
            else:
                subgoal_target = pygame.Vector2(subgoal_position.x, subgoal_position.y)
        distance_to_subgoal = agent_location.distance_to(subgoal_position)
        
        if distance_to_subgoal < min_distance:
            min_distance = distance_to_subgoal
            target = subgoal_target
    
    return target, False


def am_i_stuck(agent_location, zone_id):
    """
        Fixing the scenario, that the agents get shoved back into the benches. So they update their subgoal to the previous one.
    """
    base_zone = Obstacle(**BASE_ZONE)
    if not zone_id:
        return False
    if base_zone.is_in(pygame.Vector2(agent_location.x+AGENT_RADIUS, agent_location.y+AGENT_RADIUS)) or base_zone.is_in(pygame.Vector2(agent_location.x-AGENT_RADIUS, agent_location.y-AGENT_RADIUS)):
        return True
    return False