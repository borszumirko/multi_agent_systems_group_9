from constants import SUBGOAL_ZONES, AGENT_RADIUS, WIDTH, HEIGHT, BASE_ZONE
import pygame
import numpy as np

# A zone counts as entered after being obstacle_padding pixels deep
obstacle_padding = 3

def find_subgoal(subgoal_indicator, agent_location):
    """
        Takes the subgoal-id and the location of the agent and gives back the direction to the nearest subgoal-zone.
        The subgoal-zones are predefined by the constants-file.
        If the subgoal is reached the second return will be True.
    """
    subgoals = SUBGOAL_ZONES[subgoal_indicator]

    # Calculate smallest distance to subgoal-zones and pick zone
    min_distance = float('inf')
    target = None

    for subgoal in subgoals:
        subgoal_position = pygame.Vector2(subgoal["position"][0], subgoal["position"][1])
        x_in = ((subgoal["position"][0] - subgoal["w"]//2) < agent_location.x-AGENT_RADIUS-obstacle_padding) and ((subgoal["position"][0] + subgoal["w"]//2) >= agent_location.x+AGENT_RADIUS+obstacle_padding)
        y_in = ((subgoal["position"][1] - subgoal["h"]//2) < agent_location.y-AGENT_RADIUS-obstacle_padding) and ((subgoal["position"][1] + subgoal["h"]//2) >= agent_location.y+AGENT_RADIUS+obstacle_padding)
        if x_in and y_in:
            return subgoal_position, True
        
        
        if am_i_stuck(agent_location, subgoal_indicator):
            subgoal_target, _ = find_subgoal(subgoal_indicator-1, agent_location)
        else:
            if x_in:
                subgoal_target = pygame.Vector2(agent_location.x, subgoal["position"][1])
            elif y_in:
                subgoal_target = pygame.Vector2(subgoal["position"][0], agent_location.y)
            else:
                subgoal_target = pygame.Vector2(subgoal["position"][0], subgoal["position"][1])
        distance_to_subgoal = agent_location.distance_to(subgoal_position)
        
        if distance_to_subgoal < min_distance:
            min_distance = distance_to_subgoal
            target = subgoal_target
    
    return target, False


def am_i_stuck(agent_location, zone_id):
    """
        Fixing the scenario, that the agents get shoved back into the benches. So they update their subgoal to the previous one.
    """
    if not zone_id:
        return False
    x_in = ((BASE_ZONE["position"][0] - BASE_ZONE["w"]//2) < agent_location.x+AGENT_RADIUS) and ((BASE_ZONE["position"][0] + BASE_ZONE["w"]//2) >= agent_location.x-AGENT_RADIUS)
    y_in = ((BASE_ZONE["position"][1] - BASE_ZONE["h"]//2) < agent_location.y+AGENT_RADIUS) and ((BASE_ZONE["position"][1] + BASE_ZONE["h"]//2) >= agent_location.y-AGENT_RADIUS)
    if x_in and y_in:
        return True
    return False