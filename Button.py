import pygame.font

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Button:
    def __init__(self, color, x, y, width, height, text="", hover_color=None):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.border_radius = 10
        self.text = text
        self.default_color = color  # Store the default color
        self.hover_color = (
            150,
            150,
            150,
        )  # Some gray color for hover, you can change this
        self.original_width = width
        self.original_height = height
        self.pressed_color = self.color
        self.pressed = False
        self.clicked = False
        self.state_changed = False
        self.hover_color = (
            hover_color
            if hover_color
            else (
                150,
                150,
                150,
            )
        )

    def press(self):
        if not self.pressed:  # Check if the button is not already pressed
            self.color = self.pressed_color
            self.width -= 5
            self.height -= 5
            self.x += 2.5  # Adjust to keep the button centered
            self.y += 2.5
            self.pressed = True
            self.state_changed = True

    def release(self):
        if self.pressed:  # Check if the button is pressed
            self.color = self.default_color
            self.width = self.original_width
            self.height = self.original_height
            self.x -= 2.5
            self.y -= 2.5
            self.pressed = False
            self.state_changed = True

    def handle_event(self, event):
        # Handle mouse button down and up events
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_over(pygame.mouse.get_pos()):
                self.press()
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.pressed:
                self.release()

    def set_hover_color(self, color):
        self.hover_color = color

    def draw(self, win, outline=None):
        # Draw the button with an optional outline
        if outline:
            pygame.draw.rect(
                win,
                outline,
                (self.x - 2, self.y - 2, self.width + 4, self.height + 4),
                0,
                border_radius=self.border_radius + 2,
            )
        pygame.draw.rect(
            win,
            self.color,
            (self.x, self.y, self.width, self.height),
            0,
            border_radius=self.border_radius,
        )

        # Draw the text on the button
        if self.text != "":
            font = pygame.font.SysFont("calibri", 16)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(
                text,
                (
                    self.x + (self.width / 2 - text.get_width() / 2),
                    self.y + (self.height / 2 - text.get_height() / 2),
                ),
            )

    def is_over(self, pos):
        # Check if the mouse position is over the button
        return (
            self.x < pos[0] < self.x + self.width
            and self.y < pos[1] < self.y + self.height
        )
