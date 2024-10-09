import tkinter as tk
import pygame
import threading
import time
import math

# Global variables to store the current and target colors
current_color = (255, 255, 255)  # Initial color (white)
target_color = (255, 255, 255)  # Target color
transition_start_time = time.time()  # Start time for the transition

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
    fluctuation_range = 80  # Increase the range to make the effect more noticeable
    fluctuation_speed = 0.5    # Speed up the fluctuation for more visible changes

    r = base_color[0] + fluctuation_range * math.sin(fluctuation_speed * time_elapsed)
    g = base_color[1] + fluctuation_range * math.sin(fluctuation_speed * time_elapsed + 2)  # Phase shift
    b = base_color[2] + fluctuation_range * math.sin(fluctuation_speed * time_elapsed + 4)  # Phase shift

    # Ensure the color values stay within valid RGB limits (0-255)
    r = max(0, min(255, int(r)))
    g = max(0, min(255, int(g)))
    b = max(0, min(255, int(b)))

    return (r, g, b)


# Function to display gradient with dynamic color transitions and fluctuation
def display_gradient():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))  # Windowed mode (800x600)
    pygame.display.set_caption("Dynamic Color Transitions with Fluctuations")

    global current_color
    global target_color
    global transition_start_time

    running = True

    while running:
        with color_lock:
            elapsed_time = time.time() - transition_start_time
            t = min(elapsed_time / 2, 1)  # Normalize time to [0, 1] for a 2-second transition

            # Interpolate between the current and target color based on time `t`
            new_color = interpolate_color(current_color, target_color, t)

            # If the transition is complete, set the current color to the target color and fluctuate around it
            if t >= 1:
                current_color = target_color
                fluctuating_color = fluctuate_color(current_color, elapsed_time)
            else:
                fluctuating_color = new_color

        # Fill the screen with the fluctuating color
        screen.fill(fluctuating_color)
        pygame.display.flip()

        # Process Pygame events (to allow exiting or pressing key)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                running = False

        pygame.time.wait(30)  # Frame rate control

    pygame.quit()

# Button click event handler
def button_click(new_color):
    global current_color  # Declare current_color as global
    global target_color  # Declare target_color as global
    global transition_start_time

    # Safely update the target color and reset the transition start time
    with color_lock:
        current_color = interpolate_color(current_color, target_color, min((time.time() - transition_start_time) / 2, 1))
        target_color = new_color
        transition_start_time = time.time()  # Reset the start time for a new transition

# GUI setup
def create_gui():
    root = tk.Tk()
    root.title("Dynamic Gradient Transitions")

    # Create buttons
    button1 = tk.Button(root, text="Gradient 1", command=lambda: button_click((255, 0, 0)))  # Red
    button2 = tk.Button(root, text="Gradient 2", command=lambda: button_click((0, 255, 0)))  # Green
    button3 = tk.Button(root, text="Gradient 3", command=lambda: button_click((0, 0, 255)))  # Blue

    # Pack buttons into the window
    button1.pack(pady=10)
    button2.pack(pady=10)
    button3.pack(pady=10)

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
