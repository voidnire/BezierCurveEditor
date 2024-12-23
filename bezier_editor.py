import pygame
import sys
import numpy as np
from pygame.locals import QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, KEYDOWN, K_c

# Inicialização do Pygame
pygame.init()


# Configurações da Tela
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Editor de Curvas de Bézier")

# Configurações do Botão
BUTTON_WIDTH, BUTTON_HEIGHT = 140, 40
BUTTON_RECT = pygame.Rect(
    (WIDTH - BUTTON_WIDTH) // 2,  # Centraliza horizontalmente
    HEIGHT - BUTTON_HEIGHT - 20,  # Coloca 20 pixels acima da borda inferior
    BUTTON_WIDTH,
    BUTTON_HEIGHT
)
BUTTON_COLOR = (255, 0, 127)  # Rosa
BUTTON_TEXT_COLOR = (255, 255, 255)  # Branco


# Definição de Cores
COLORS = {
    "BLACK": (0,0,0),
    "WHITE": (255, 255, 255),
    "PINK": (255, 0, 127),
    "PURPLE": (138, 43, 226),
    "BLUE": (56, 176, 222),
}

# Variáveis Globais
control_points = []
selected_point = None
dragging = False

def draw_button():
    pygame.draw.rect(SCREEN, BUTTON_COLOR, BUTTON_RECT)
    font = pygame.font.SysFont(None, 30)
    text_surface = font.render("Limpar Tela", True, BUTTON_TEXT_COLOR)
    SCREEN.blit(text_surface, (BUTTON_RECT.x + 10, BUTTON_RECT.y + 10))


def bezier_point(t, points):
    """Calcula um ponto na curva de Bézier usando o algoritmo de De Casteljau."""
    temp_points = points.copy()
    while len(temp_points) > 1:
        temp_points = [
            (1 - t) * np.array(p0) + t * np.array(p1)
            for p0, p1 in zip(temp_points[:-1], temp_points[1:])
        ]
    return temp_points[0]

def draw_curve():
    """Desenha a curva de Bézier."""
    if len(control_points) < 2:
        return
    bezier_points = [
        bezier_point(t, control_points)
        for t in np.linspace(0, 1, 100)
    ]
    pygame.draw.lines(SCREEN, COLORS["PINK"], False, bezier_points, 2)

def draw_control_polygon():
    """Desenha o polígono de controle."""
    if len(control_points) > 1:
        pygame.draw.lines(SCREEN, COLORS["BLUE"], False, control_points, 1)

def draw_control_points():
    """Desenha os pontos de controle e suas coordenadas."""
    font = pygame.font.SysFont(None, 24)
    for x, y in control_points:
        pygame.draw.circle(SCREEN, COLORS["PURPLE"], (x, y), 5)
        coord_text = f"({x}, {y})"
        SCREEN.blit(font.render(coord_text, True, COLORS["WHITE"]), (x + 10, y - 20))

def handle_mouse_events(event):
    """Gerencia os eventos relacionados ao mouse."""
    global selected_point, dragging

    if event.type == MOUSEBUTTONDOWN:

        if event.button == 1:  # Botão esquerdo
            mouse_pos = pygame.mouse.get_pos()

            # Verifica se o clique foi no botão
            if BUTTON_RECT.collidepoint(mouse_pos):
                control_points.clear()
            else:
                for i, point in enumerate(control_points):
                    if np.linalg.norm(np.array(point) - np.array(event.pos)) < 10:
                        selected_point = i
                        dragging = True
                        return
                control_points.append(list(event.pos))

        elif event.button == 3:  # Botão direito
            for point in control_points:
                if np.linalg.norm(np.array(point) - np.array(event.pos)) < 10:
                    control_points.remove(point)
                    break

    elif event.type == MOUSEBUTTONUP and event.button == 1:
        selected_point = None
        dragging = False

    elif event.type == MOUSEMOTION and dragging and selected_point is not None:
        control_points[selected_point] = list(event.pos)

def handle_keyboard_events(event):
    """Gerencia os eventos relacionados ao teclado."""
    if event.type == KEYDOWN and event.key == K_c:
        control_points.clear()

def main():
    """Loop principal do programa."""
    while True:
        # Controle de Eventos


        SCREEN.fill(COLORS["BLACK"])

        # Desenhar elementos
        draw_curve()
        draw_control_polygon()
        draw_control_points()
        draw_button()  

        # Eventos
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            handle_mouse_events(event)
            handle_keyboard_events(event)

        pygame.display.flip()

if __name__ == "__main__":
    main()
