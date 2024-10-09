import tkinter as tk
import pygame
import threading
import time
import math
import numpy as np
from scipy.ndimage import gaussian_filter

# Global variables to store the current and target colors for 9 quadrants
quadrants_current_colors = [(255, 255, 255)] * 9  # Start with white for all quadrants
quadrants_target_colors = [(255, 255, 255)] * 9   # Target color for each quadrant
transition_start_times = [time.time()] * 9          # Start time for each quadrant transition
blur_sigma = 5  # Standard deviation for the Gaussian blur, can be adjusted

# Lock to manage transitions safely
color_lock = threading.Lock()

# Function to interpolate between two colors
def interpolate_color(color1, color2, t):
    r = int(color1[0] + (color2[0] - color1[0]) * t)
    g = int(color1[1] + (color2[1] - color1[1]) * t)
    b = int(color1[2] + (color2[2] - color1[2]) * t)
    return (r, g, b)

# Function to add slight fluctuation to a color
def fluctuate_color(base_color, time_elapsed):
    fluctuation_range = 50  # Adjust the range for noticeable effect
    fluctuation_speed = 4    # Speed up the fluctuation

    r = base_color[0] + fluctuation_range * math.sin(fluctuation_speed * time_elapsed)
    g = base_color[1] + fluctuation_range * math.sin(fluctuation_speed * time_elapsed + 2)
    b = base_color[2] + fluctuation_range * math.sin(fluctuation_speed * time_elapsed + 4)

    # Ensure the color values stay within valid RGB limits (0-255)
    r = max(0, min(255, int(r)))
    g = max(0, min(255, int(g)))
    b = max(0, min(255, int(b)))

    return (r, g, b)

# Function to apply Gaussian blur using a specified sigma
def apply_gaussian_blur(surface, sigma):
    if sigma <= 0:
        return surface

    # Convert the surface to a numpy array
    array = pygame.surfarray.array3d(surface)

    # Apply Gaussian blur
    blurred_array = gaussian_filter(array, sigma=sigma)

    # Convert back to Pygame surface
    return pygame.surfarray.make_surface(blurred_array.astype(np.uint8))

# Function to display gradient with dynamic color transitions and fluctuations for 9 quadrants
def display_gradient():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))  # Windowed mode (800x600)
    pygame.display.set_caption("Dynamic Color Transitions with Fluctuations")

    running = True
    while running:
        screen.fill((255, 255, 255))  # White background

        with color_lock:
            for i in range(9):
                elapsed_time = time.time() - transition_start_times[i]
                t = min(elapsed_time / 2, 1)  # Normalize time to [0, 1] for a 2-second transition

                # Interpolate the color of each quadrant
                new_color = interpolate_color(quadrants_current_colors[i], quadrants_target_colors[i], t)

                # If transition is complete, fluctuate around the target color
                if t >= 1:
                    quadrants_current_colors[i] = quadrants_target_colors[i]
                    fluctuating_color = fluctuate_color(quadrants_current_colors[i], elapsed_time)
                else:
                    fluctuating_color = new_color

                # Calculate the rectangle position for each quadrant
                col = i % 3  # 0, 1, 2 for each column
                row = i // 3  # 0, 1, 2 for each row
                rect_width = screen.get_width() // 3
                rect_height = screen.get_height() // 3

                rect_x = col * rect_width
                rect_y = row * rect_height

                # Draw the quadrant with the fluctuating color
                pygame.draw.rect(screen, fluctuating_color, (rect_x, rect_y, rect_width, rect_height))

        # Apply Gaussian blur effect to the entire screen
        blurred_screen = apply_gaussian_blur(screen.copy(), blur_sigma)
        screen.blit(blurred_screen, (0, 0))

        pygame.display.flip()

        # Process Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                running = False

        pygame.time.wait(30)  # Frame rate control

    pygame.quit()

# Button click event handler for changing multiple quadrants with different colors
def button_click(color_map):
    global quadrants_current_colors  # Declare the global list of current colors
    global quadrants_target_colors  # Declare the global list of target colors
    global transition_start_times

    # Safely update the target color for the selected quadrants
    with color_lock:
        for index, new_color in color_map.items():
            quadrants_current_colors[index] = interpolate_color(
                quadrants_current_colors[index],
                quadrants_target_colors[index],
                min((time.time() - transition_start_times[index]) / 2, 1)
            )
            quadrants_target_colors[index] = new_color
            transition_start_times[index] = time.time()  # Reset the start time for a new transition

# GUI setup
def create_gui():
    root = tk.Tk()
    root.title("Dynamic Gradient Transitions")

    # Create a button for changing multiple quadrants to different colors
    button = tk.Button(root, text="Change Colors of Quadrants",
                       command=lambda: button_click({
                           0: (255, 0, 0),   # Quadrant 1 to Red
                           1: (0, 255, 0),   # Quadrant 2 to Green
                           2: (0, 0, 255),   # Quadrant 3 to Blue
                           3: (255, 255, 0), # Quadrant 4 to Yellow
                           4: (255, 0, 255), # Quadrant 5 to Magenta
                           5: (0, 255, 255), # Quadrant 6 to Cyan
                           6: (128, 0, 128), # Quadrant 7 to Purple
                           7: (255, 165, 0), # Quadrant 8 to Orange
                           8: (128, 128, 128) # Quadrant 9 to Gray
                       }))  

    # Pack button into the window
    button.pack(pady=10)

    root.mainloop()

# Start Pygame in a separate thread
def start_pygame_thread():
    pygame_thread = threading.Thread(target=display_gradient)
    pygame_thread.start()

# Main entry point
if __name__ == "__main__":
    # Start the Pygame window in the background
    start_pygame_thread()

    # Start the Tkinter GUI
    create_gui()
