import cv2
import numpy as np
import pygame
import sys
import math

def spotlight_effect(frame, spotlight_size, spotlight_pos):
    mask = np.zeros_like(frame)
    h, w = frame.shape[:2]
    y, x = spotlight_pos
    rr, cc = np.meshgrid(np.arange(h), np.arange(w), indexing='ij')
    mask[((rr - y) ** 2 + (cc - x) ** 2) <= spotlight_size ** 2] = 255
    return cv2.bitwise_and(frame, mask)

def main():
    # Initialize Pygame
    pygame.init()
    width, height = 640, 480
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Video Spotlight")
    clock = pygame.time.Clock()

    # Initialize OpenCV
    cap = cv2.VideoCapture(r'C:\Users\91739\Downloads\video.mp4')

    playing = True
    spotlight_size = 100
    while playing:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (width, height))

        # Convert the frame to RGB for Pygame display
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)

        # Convert the frame to a Pygame surface
        frame_surface = pygame.surfarray.make_surface(frame)

        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Add spotlight effect
        frame_surface.blit(pygame.surfarray.make_surface(spotlight_effect(frame, spotlight_size, (mouse_x, mouse_y))), (0, 0))

        # Display frame
        screen.blit(frame_surface, (0, 0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    playing = False

        clock.tick(60)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
