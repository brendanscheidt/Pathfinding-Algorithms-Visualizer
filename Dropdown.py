import pygame

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
DARK_GREY = (200, 200, 200)
LIGHT_GREEN = (0, 150, 0)
LIGHT_WHITE = (200, 200, 200)
LIGHT_PURPLE = (203, 195, 227)
LIGHT_VIOLET = (207, 159, 255)
LILAC = (204, 204, 255)


class Dropdown:
    def __init__(self, x, y, width, height, options, default_index=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.options = options
        self.selected_option = options[default_index]
        self.is_open = False
        self.font = pygame.font.SysFont("calibri", 18)
        self.border_radius = 10  # Radius for rounded corners
        self.default_color = LIGHT_VIOLET
        self.hover_color = LILAC
        self.pressed_color = DARK_GREY
        self.color = self.default_color
        self.original_width = width
        self.original_height = height
        self.pressed = False
        self.hovered_option = None

    def press(self):
        if not self.pressed:
            self.color = self.pressed_color
            self.width -= 5
            self.height -= 5
            self.x += 2.5
            self.y += 2.5
            self.pressed = True

    def release(self):
        if self.pressed:
            self.color = self.default_color
            self.width = self.original_width
            self.height = self.original_height
            self.x -= 2.5
            self.y -= 2.5
            self.pressed = False

    def draw(self, win):
        pygame.draw.rect(
            win,
            self.color,
            (self.x, self.y, self.width, self.height),
            0,
            border_radius=self.border_radius,
        )
        pygame.draw.rect(
            win,
            BLACK,
            (self.x, self.y, self.width, self.height),
            2,
            border_radius=self.border_radius,
        )
        text = self.font.render(self.selected_option, 1, BLACK)
        text_width, text_height = text.get_size()
        win.blit(
            text,
            (
                self.x + (self.width - text_width) // 2,
                self.y + (self.height - text_height) // 2,
            ),
        )

        if self.is_open:
            for i, option in enumerate(self.options):
                color = LIGHT_PURPLE
                if (
                    i == self.hovered_option
                ):  # Check if this option is being hovered over
                    color = self.hover_color
                pygame.draw.rect(
                    win,
                    color,
                    (self.x, self.y + (i + 1) * self.height, self.width, self.height),
                    0,
                    border_radius=self.border_radius,
                )
                pygame.draw.rect(
                    win,
                    BLACK,
                    (self.x, self.y + (i + 1) * self.height, self.width, self.height),
                    2,
                    border_radius=self.border_radius,
                )
                text = self.font.render(option, 1, BLACK)
                text_width, text_height = text.get_size()
                win.blit(
                    text,
                    (
                        self.x + (self.width - text_width) // 2,
                        self.y
                        + (i + 1) * self.height
                        + (self.height - text_height) // 2,
                    ),
                )

    def handle_event(self, event):
        pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_over(pos):
                self.press()
                if self.is_open:
                    self.is_open = False
                    # Use the original height for the index calculation
                    index = int((pos[1] - self.y) // self.original_height) - 1
                    if 0 <= index < len(self.options):
                        self.selected_option = self.options[index]
                else:
                    self.is_open = True
            elif self.is_open:
                self.is_open = False
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.pressed:
                self.release()
        elif event.type == pygame.MOUSEMOTION:
            if self.is_open:
                index = int((pos[1] - self.y) // self.original_height) - 1
                if 0 <= index < len(self.options):
                    self.hovered_option = index
                else:
                    self.hovered_option = None
            if self.is_over(pos):
                self.color = self.hover_color
            else:
                self.color = self.default_color

    def is_over(self, pos):
        if self.is_open:
            return (
                self.x < pos[0] < self.x + self.width
                and self.y < pos[1] < self.y + (len(self.options) + 1) * self.height
            )
        else:
            return (
                self.x < pos[0] < self.x + self.width
                and self.y < pos[1] < self.y + self.height
            )
