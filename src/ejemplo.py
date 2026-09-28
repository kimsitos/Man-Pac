import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

font = pygame.font.Font(None, 50)

estado = "MENU"

# Botón
play_text = font.render("JUGAR", True, (255, 255, 255))
play_rect = play_text.get_rect(center=(WIDTH//2, 250))

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if estado == "MENU":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    estado = "JUGANDO"

    screen.fill((0, 0, 0))

    if estado == "MENU":

        # Cambiar color si el ratón está encima
        if play_rect.collidepoint(pygame.mouse.get_pos()):
            color = (255, 255, 0)
        else:
            color = (255, 255, 255)

        play_text = font.render("JUGAR", True, color)
        screen.blit(play_text, play_rect)

    elif estado == "JUGANDO":

        texto = font.render("PACMAN INICIADO", True, (0, 255, 0))
        screen.blit(texto, (180, 250))

    pygame.display.flip()

pygame.quit()
