import pygame

pygame.init()

# Farben
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
DARK_GRAY = (100, 100, 100)
RED = (200, 50, 50)

# Bildschirmgröße holen
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

# Vollbildmodus aktivieren
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Fullscreen Desktop Icons")

# Schriftart
pygame.font.init()
font = pygame.font.Font(None, 24)  # Standard-Schrift

class Window:
    """Erstellt ein verschiebbares Fenster mit Schließen-Button."""
    def __init__(self, x, y, width, height, title):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.title = title
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0
        self.close_button_rect = pygame.Rect(self.x + self.width - 20, self.y, 20, 20)

    def draw(self, screen):
        """Zeichnet das Fenster."""
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height), border_radius=5)
        pygame.draw.rect(screen, DARK_GRAY, (self.x, self.y, self.width, 30), border_top_left_radius=5, border_top_right_radius=5)
        pygame.draw.rect(screen, RED, self.close_button_rect, border_radius=5)

        # Titel
        title_surface = font.render(self.title, True, WHITE)
        screen.blit(title_surface, (self.x + 5, self.y + 5))

        # X-Button
        x_surface = font.render("X", True, WHITE)
        screen.blit(x_surface, (self.close_button_rect.x + 5, self.close_button_rect.y + 2))

    def handle_event(self, event):
        """Verarbeitet Maus-Events für Dragging und Schließen."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.close_button_rect.collidepoint(event.pos):
                return False  # Fenster schließen
            elif pygame.Rect(self.x, self.y, self.width, 30).collidepoint(event.pos):  # Titelleiste
                self.dragging = True
                self.offset_x = event.pos[0] - self.x
                self.offset_y = event.pos[1] - self.y

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.x = event.pos[0] - self.offset_x
            self.y = event.pos[1] - self.offset_y
            self.close_button_rect.x = self.x + self.width - 20
            self.close_button_rect.y = self.y

        return True
def show_dialog(screen, title, message, button_text, sound_path):
    pygame.mixer.init()
    sound = pygame.mixer.Sound(sound_path)  # Sound laden
    sound.play()  # Sound abspielen

    # Farben & Schriftart
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (180, 180, 180)
    font = pygame.font.Font(None, 30)
    title_font = pygame.font.Font(None, 36)

    # Dialog-Box Größe & Position
    box_width, box_height = 400, 200
    box_x = (screen.get_width() - box_width) // 2
    box_y = (screen.get_height() - box_height) // 2

    # Button Größe & Position
    button_width, button_height = 120, 40
    button_x = box_x + (box_width - button_width) // 2
    button_y = box_y + box_height - 60
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    # Dialog-Loop
    dialog_open = True
    while dialog_open:
        screen.fill((50, 50, 50))  # Hintergrund abdunkeln

        # Dialogbox zeichnen
        pygame.draw.rect(screen, WHITE, (box_x, box_y, box_width, box_height), border_radius=10)
        pygame.draw.rect(screen, GRAY, (box_x, box_y, box_width, 40), border_radius=10)  # Titelbereich

        # Titeltext
        title_surf = title_font.render(title, True, BLACK)
        title_rect = title_surf.get_rect(center=(box_x + box_width // 2, box_y + 20))
        screen.blit(title_surf, title_rect)

        # Nachrichtentext
        message_surf = font.render(message, True, BLACK)
        message_rect = message_surf.get_rect(center=(box_x + box_width // 2, box_y + 80))
        screen.blit(message_surf, message_rect)

        # Button zeichnen
        pygame.draw.rect(screen, GRAY, button_rect, border_radius=5)
        button_text_surf = font.render(button_text, True, BLACK)
        button_text_rect = button_text_surf.get_rect(center=button_rect.center)
        screen.blit(button_text_surf, button_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    dialog_open = False  # Dialog schließen

        pygame.display.flip()
# Fenster-Liste
windows = []

def open_window(title, width, height):
    """Öffnet ein neues Fenster in der Mitte des Bildschirms."""
    x = (WIDTH - width) // 2
    y = (HEIGHT - height) // 2
    windows.append(Window(x, y, width, height, title))

class DesktopIcon:
    def __init__(self, x, y, image_path, text, action):
        self.x = x
        self.y = y
        self.text = text
        self.icon_size = 64
        self.text_offset = 10
        self.action = action

        # Bild laden
        self.icon = pygame.image.load(image_path)
        self.icon = pygame.transform.scale(self.icon, (self.icon_size, self.icon_size))

        # Klick-Bereich
        self.rect = pygame.Rect(self.x, self.y, self.icon_size, self.icon_size+20)

    def draw(self, screen):
        pygame.draw.rect(screen, DARK_GRAY, (self.x-2, self.y-2, self.icon_size+4, self.icon_size+24), border_radius=5)
        pygame.draw.rect(screen, (0,0,0), (self.x, self.y, self.icon_size, self.icon_size+20), border_radius=5)
        screen.blit(self.icon, (self.x, self.y))

        text_surf = font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=(self.x + self.icon_size // 2, self.y + self.icon_size + self.text_offset))
        screen.blit(text_surf, text_rect)

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.action()

# Beispiel-Aktionen
def open_app_1():
    show_dialog(screen, "Info", "App 1 wurde geöffnet.", "OK", "assets/msgbox.wav")

def open_app_2():
    open_window("App 2", 400, 250)

# Icons erstellen
icons = [
    DesktopIcon(100, 100, "assets/ShutDown.png", "App 1", open_app_1),
    DesktopIcon(200, 100, "assets/Horizon.jpg", "App 2", open_app_2)
]

running = True
while running:
    screen.fill(GRAY)

    for icon in icons:
        icon.draw(screen)

    for window in windows:
        window.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for icon in icons:
                icon.check_click(event.pos)

        # Fenster-Events verarbeiten
        windows = [window for window in windows if window.handle_event(event)]

    pygame.display.flip()

pygame.quit()
