import cv2
import numpy as np

class MapCreator:
    def __init__(self, map_width, map_height, field_color=(0, 128, 0)):
        """Initialize map creator with specified dimensions and field color"""
        self.map_width = map_width
        self.map_height = map_height
        self.field_color = field_color  # Green field color
        self.map_image = self.create_football_field()

    def create_football_field(self):
        """Create a football field with standard markings"""
        # Create a green field background
        field = np.zeros((self.map_height, self.map_width, 3), dtype=np.uint8)
        field[:] = self.field_color

        # Define white color for field lines
        line_color = (255, 255, 255)
        line_thickness = 2

        # Draw field border
        cv2.rectangle(field, (5, 5), (self.map_width - 5, self.map_height - 5), line_color, line_thickness)
        # Draw center line
        cv2.line(field, (self.map_width // 2, 5), (self.map_width // 2, self.map_height - 5), line_color, line_thickness)
        # Draw center circle
        cv2.circle(field, (self.map_width // 2, self.map_height // 2), 40, line_color, line_thickness)
        # Draw center spot
        cv2.circle(field, (self.map_width // 2, self.map_height // 2), 3, line_color, -1)

        # Draw penalty areas
        # Left penalty area
        cv2.rectangle(field, (5, self.map_height // 2 - 80), (100, self.map_height // 2 + 80), line_color, line_thickness)
        # Right penalty area
        cv2.rectangle(field, (self.map_width - 100, self.map_height // 2 - 80), (self.map_width - 5, self.map_height // 2 + 80), line_color, line_thickness)

        # Draw goal areas
        # Left goal area
        cv2.rectangle(field, (5, self.map_height // 2 - 40), (40, self.map_height // 2 + 40), line_color, line_thickness)
        # Right goal area
        cv2.rectangle(field, (self.map_width - 40, self.map_height // 2 - 40), (self.map_width - 5, self.map_height // 2 + 40), line_color, line_thickness)

        return field

    def draw_player(self, x, y, color, radius=5):
        """Draw a player as a colored circle on the field map"""
        cv2.circle(self.map_image, (int(x), int(y)), radius, color, -1)

    def draw_ball(self, x, y, color=(255, 255, 255), radius=3):
        """Draw the ball as a white circle on the field map"""
        cv2.circle(self.map_image, (int(x), int(y)), radius, color, -1)

    def get_map(self):
        """Return a copy of the current field map"""
        return self.map_image.copy()

    def reset_map(self):
        """Reset the field map to its original state (clears player/ball positions)"""
        self.map_image = self.create_football_field()
