import pygame

def AAfilledRoundedRect(surface, rect, color, radius=10):
    """
    Draws an anti-aliased filled rounded rectangle with a fixed corner radius.
    
    surface : destination surface
    rect    : pygame.Rect or tuple, defining the rectangle
    color   : (R, G, B, A) color tuple
    radius  : integer, fixed radius for the rounded corners
    """
    rect = pygame.Rect(rect)
    color = pygame.Color(*(isinstance(color, pygame.Color) and color or (isinstance(color, tuple) and pygame.Color(*color) or pygame.Color(color))))
    alpha = color.a
    color.a = 0  # Set alpha to 0 for blending later

    # Ensure the radius does not exceed half of the smaller dimension
    radius = max(0, min(radius, min(rect.width, rect.height) // 2))

    # Handle negative coordinates by adjusting the rectangle's position and size
    clip_rect = rect.clip(surface.get_rect())
    if clip_rect.width <= 0 or clip_rect.height <= 0:
        return  # Skip drawing if the clipped rectangle has no area

    # Adjust the rect to ensure it's within the visible area
    rectangle_surface = pygame.Surface(clip_rect.size, pygame.SRCALPHA)
    
    # Adjust the rectangle's top-left position for negative coordinates
    draw_rect = pygame.Rect(
        max(0, -rect.left), 
        max(0, -rect.top), 
        rect.width, 
        rect.height
    )

    # Create the corner surface
    circle_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    
    # Draw the filled circle (to be used as corners)
    pygame.draw.ellipse(circle_surface, (0, 0, 0), circle_surface.get_rect())

    # Blit the rounded corners onto the rectangle surface
    rectangle_surface.blit(circle_surface, draw_rect.topleft)  # Top-left
    rectangle_surface.blit(pygame.transform.flip(circle_surface, True, False), (draw_rect.width - radius * 2, 0))  # Top-right
    rectangle_surface.blit(pygame.transform.flip(circle_surface, False, True), (0, draw_rect.height - radius * 2))  # Bottom-left
    rectangle_surface.blit(pygame.transform.flip(circle_surface, True, True), (draw_rect.width - radius * 2, draw_rect.height - radius * 2))  # Bottom-right

    # Draw the center rectangle (without rounded corners)
    rectangle_surface.fill((0, 0, 0), draw_rect.inflate(-radius * 2, 0))
    rectangle_surface.fill((0, 0, 0), draw_rect.inflate(0, -radius * 2))

    # Apply the color and alpha blending
    rectangle_surface.fill(color, special_flags=pygame.BLEND_RGBA_MAX)
    rectangle_surface.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MIN)

    # Blit the final rectangle onto the target surface, respecting the original top-left offset
    return surface.blit(rectangle_surface, clip_rect.topleft)
