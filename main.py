import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720), pygame.SCALED)
pygame.display.set_caption("Prueba")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 56)

pos = (640, 360)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION):
            pos = event.pos

    screen.fill((16, 18, 28))
    txt = font.render("Hola Android - pygame funciona", True, (0, 220, 255))
    screen.blit(txt, txt.get_rect(center=(640, 100)))
    pygame.draw.circle(screen, (255, 200, 50), pos, 40)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()