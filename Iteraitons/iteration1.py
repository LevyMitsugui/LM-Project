import tkinter as tk
import pygame
import threading

# Initialize Pygame and create a gradient display function
def display_gradient(color1, color2):
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
    
    # Create a gradient
    for i in range(1080):
        r = color1[0] + (color2[0] - color1[0]) * i // 1080
        g = color1[1] + (color2[1] - color1[1]) * i // 1080
        b = color1[2] + (color2[2] - color1[2]) * i // 1080
        pygame.draw.line(screen, (r, g, b), (0, i), (1920, i))

    pygame.display.flip()
    
    # Wait for an event (like pressing any key) to exit the display
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                running = False

    pygame.quit()

# Button click event handler
def button_click(color1, color2):
    # Run Pygame in a separate thread to avoid conflicts with Tkinter
    pygame_thread = threading.Thread(target=display_gradient, args=(color1, color2))
    pygame_thread.start()

# GUI setup
def create_gui():
    root = tk.Tk()
    root.title("Gradient Transitions")

    # Create buttons
    button1 = tk.Button(root, text="Gradient 1", command=lambda: button_click((255, 0, 0), (0, 0, 255)))
    button2 = tk.Button(root, text="Gradient 2", command=lambda: button_click((0, 255, 0), (255, 255, 0)))
    button3 = tk.Button(root, text="Gradient 3", command=lambda: button_click((255, 165, 0), (75, 0, 130)))

    # Pack buttons into the window
    button1.pack(pady=10)
    button2.pack(pady=10)
    button3.pack(pady=10)

    root.mainloop()

# Start the GUI
if __name__ == "__main__":
    create_gui()
