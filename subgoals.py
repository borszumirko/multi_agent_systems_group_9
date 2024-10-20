from constants import SUBGOAL_ZONES, AGENT_RADIUS, WIDTH, HEIGHT
import pygame
import numpy as np

safety_padding = 5

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
        x_in = ((subgoal["position"][0] - subgoal["w"]//2) < agent_location.x-AGENT_RADIUS-safety_padding) and ((subgoal["position"][0] + subgoal["w"]//2) >= agent_location.x+AGENT_RADIUS+safety_padding)
        y_in = ((subgoal["position"][1] - subgoal["h"]//2) < agent_location.y-AGENT_RADIUS-safety_padding) and ((subgoal["position"][1] + subgoal["h"]//2) >= agent_location.y+AGENT_RADIUS+safety_padding)
        if x_in and y_in:
            return subgoal_position, True
        
        if x_in:
            if am_i_stuck(agent_location, subgoal_indicator):
                subgoal_target, _ = find_subgoal(subgoal_indicator-1, agent_location)
            else:
                subgoal_target = pygame.Vector2(agent_location.x, subgoal["position"][1])
            distance_to_subgoal = agent_location.distance_to(subgoal_position)
        elif y_in:
            subgoal_target = pygame.Vector2(subgoal["position"][0], agent_location.y)
            distance_to_subgoal = agent_location.distance_to(subgoal_position)
        else:
            subgoal_target = pygame.Vector2(subgoal["position"][0], subgoal["position"][1])
            distance_to_subgoal = agent_location.distance_to(subgoal_position)
        
        if distance_to_subgoal < min_distance:
            min_distance = distance_to_subgoal
            target = subgoal_target
    
    return target, False


def am_i_stuck(agent_location, id):
    """
        Fixing the scenario, that the agents get shoved back into the benches. So they update their subgoal to the previous one.
    """
    if not id:
        return False
    past_subgoals = SUBGOAL_ZONES[id-1]
    current_subgoals = SUBGOAL_ZONES[id]
    for subgoal in past_subgoals:
        x_in = ((subgoal["position"][0] - subgoal["w"]//2) < agent_location.x-AGENT_RADIUS-safety_padding) and ((subgoal["position"][0] + subgoal["w"]//2) >= agent_location.x+AGENT_RADIUS+safety_padding)
        if x_in:
            return False
    for subgoal in current_subgoals:
        y_nearly_in = ((subgoal["position"][1] - subgoal["h"]//2) < agent_location.y+AGENT_RADIUS) and ((subgoal["position"][1] + subgoal["h"]//2) >= agent_location.y-AGENT_RADIUS)
        if y_nearly_in:
            return False
    return True
