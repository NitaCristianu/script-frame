import pygame

def applyCorners(surf: pygame.Surface, radius = 4):
    mask = pygame.Surface(surf.get_size(), pygame.SRCALPHA, 32)
    mask.fill((0,0,0,0))
    pygame.draw.rect(mask, (255, 255, 255, 255), pygame.Rect(0, 0, *surf.get_size()), border_radius=radius)
    cloned = surf.copy()
    cloned.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    return cloned

def AAfilledRoundedRect(surface, rect, color, radius=10):
    rect = pygame.Rect(rect)
    color = pygame.Color(*(isinstance(color, pygame.Color) and color or (isinstance(color, tuple) and pygame.Color(*color) or pygame.Color(color))))

    pygame.draw.rect(surface, color, rect, 0, int(radius))