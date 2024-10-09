import tkinter as tk
import pygame
import threading
import time

# Global variable to store the current target color
target_color = (255, 255, 255)  # Initial color (white)

# Function to interpolate between two colors
def interpolate_color(color1, color2, t):
    r = int(color1[0] + (color2[0] - color1[0]) * t)
    g = int(color1[1] + (color2[1] - color1[1]) * t)
    b = int(color1[2] + (color2[2] - color1[2]) * t)
    return (r, g, b)

# Function to display gradient with dynamic color transitions
def display_gradient():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))  # Windowed mode (800x600)
    pygame.display.set_caption("Dynamic Color Transitions")

    global target_color
    current_color = target_color

    running = True

    while running:
        start_time = time.time()

        # Transition from current_color to target_color
        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time
            t = min(elapsed_time / 2, 1)  # Normalize time to [0, 1] for a 2-second transition

            # Interpolate the current color
            new_color = interpolate_color(current_color, target_color, t)

            # Fill the screen with the current color
            screen.fill(new_color)
            pygame.display.flip()

            # Update current color to the new color
            if t >= 1:
                current_color = target_color
                break

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
    global target_color
    target_color = new_color

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
