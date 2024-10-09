import tkinter as tk
import pygame
import threading
import time

# Function to interpolate between two colors
def interpolate_color(color1, color2, t):
    r = int(color1[0] + (color2[0] - color1[0]) * t)
    g = int(color1[1] + (color2[1] - color1[1]) * t)
    b = int(color1[2] + (color2[2] - color1[2]) * t)
    return (r, g, b)

# Function to display gradient with smooth color transitions
def display_gradient(color1, color2, duration=2):
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)

    start_time = time.time()
    running = True

    while running:
        current_time = time.time()
        elapsed_time = current_time - start_time
        t = min(elapsed_time / duration, 1)  # Normalize time to [0, 1]
        
        # If the transition is complete, stop
        if t >= 1:
            running = False

        # Get the interpolated color based on time
        current_color = interpolate_color(color1, color2, t)

        # Fill the screen with the current color
        screen.fill(current_color)
        pygame.display.flip()

        # Process Pygame events (to allow exiting)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                running = False

        pygame.time.wait(30)  # Frame rate control (30ms delay between frames)

    pygame.quit()

# Button click event handler
def button_click(color1, color2):
    pygame_thread = threading.Thread(target=display_gradient, args=(color1, color2))
    pygame_thread.start()

# GUI setup
def create_gui():
    root = tk.Tk()
    root.title("Smooth Gradient Transitions")

    # Create buttons
    button1 = tk.Button(root, text="Gradient 1", command=lambda: button_click((255, 0, 0), (0, 0, 255)))  # Red to Blue
    button2 = tk.Button(root, text="Gradient 2", command=lambda: button_click((0, 255, 0), (255, 255, 0)))  # Green to Yellow
    button3 = tk.Button(root, text="Gradient 3", command=lambda: button_click((255, 165, 0), (75, 0, 130)))  # Orange to Indigo

    # Pack buttons into the window
    button1.pack(pady=10)
    button2.pack(pady=10)
    button3.pack(pady=10)

    root.mainloop()

# Start the GUI
if __name__ == "__main__":
    create_gui()
