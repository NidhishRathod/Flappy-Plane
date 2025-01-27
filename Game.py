import cv2
import mediapipe as mp
import pygame
import random
import threading
import tkinter as tk
from pygame.locals import *

# Initialize MediaPipe Hand Tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils  # Drawing utility

# Initialize Pygame
pygame.init()

# Game Window Variables
WIDTH, HEIGHT = 800, 600
game_screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Plane")

# Game Variables
plane_x = 100
plane_y = HEIGHT // 2
plane_width = 60
plane_height = 60
distance_covered = 0
score = 0

# Buildings
building_width = 80
building_gap = 200
buildings = []

# Load Plane & Explosion
plane_img = pygame.image.load('Flappy.png')
plane_img = pygame.transform.scale(plane_img, (plane_width, plane_height))
background_img = pygame.image.load('Bg.png')
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
boom_img = pygame.image.load('blast.png')
boom_img = pygame.transform.scale(boom_img, (80, 80))

# Load Sounds
crash_sound = pygame.mixer.Sound('Boom.mp3')

# Hand Tracking Variables
hand_detected = False
hand_y = HEIGHT // 2

# Function to generate random building height
def generate_building():
    return random.randint(100, HEIGHT - building_gap - 100)

# **SEPARATE CAMERA FEED THREAD (Now Controls Plane)**
def camera_feed():
    global hand_detected, hand_y
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)  # Flip for correct hand tracking
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                palm_y = int(hand_landmarks.landmark[0].y * HEIGHT)
                hand_detected = True
                hand_y = palm_y
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        else:
            hand_detected = False

        cv2.imshow("Camera Feed", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# **Function to Draw Realistic Buildings**
def draw_building(x, height, is_top):
    building_color = (100, 100, 100)  # Grey building color
    window_color = (255, 255, 0)  # Yellow windows
    border_color = (50, 50, 50)  # Darker border

    if is_top:
        pygame.draw.rect(game_screen, border_color, (x, 0, building_width, height))  # Border
        pygame.draw.rect(game_screen, building_color, (x + 2, 2, building_width - 4, height - 4))  # Building
    else:
        pygame.draw.rect(game_screen, border_color, (x, height + building_gap, building_width, HEIGHT - height - building_gap))  # Border
        pygame.draw.rect(game_screen, building_color, (x + 2, height + building_gap + 2, building_width - 4, HEIGHT - height - building_gap - 4))  # Building

    # Add windows
    window_size = 10
    gap_x, gap_y = 5, 5
    start_y = 5 if is_top else height + building_gap + 5

    for row in range(3, (height // (window_size + gap_y)) - 2):
        for col in range(2, (building_width // (window_size + gap_x)) - 1):
            window_x = x + col * (window_size + gap_x)
            window_y = start_y + row * (window_size + gap_y)
            pygame.draw.rect(game_screen, window_color, (window_x, window_y, window_size, window_size))

# **MAIN GAME LOOP**
def game_loop():
    global plane_y, score, distance_covered, buildings
    clock = pygame.time.Clock()
    run_game = True

    while run_game:
        game_screen.blit(background_img, (0, 0))

        if hand_detected:
            plane_y = hand_y

        distance_covered += 1

        if len(buildings) == 0 or buildings[-1][0] < WIDTH - 300:
            height = generate_building()
            buildings.append([WIDTH, height])

        for i, (x, h) in enumerate(buildings):
            x -= 5
            buildings[i][0] = x

            if x < -building_width:
                buildings.pop(i)
                score += 1

            # **Draw Top and Bottom Buildings**
            draw_building(x, h, is_top=True)
            draw_building(x, h, is_top=False)

            # Collision detection
            if plane_x + plane_width > x and plane_x < x + building_width:
                if plane_y < h or plane_y + plane_height > h + building_gap:
                    crash_sound.play()
                    game_screen.blit(boom_img, (plane_x, plane_y))
                    pygame.display.update()
                    pygame.time.delay(500)
                    game_over_screen()
                    return

        if plane_y < 0:
            plane_y = 0
        if plane_y > HEIGHT - plane_height:
            plane_y = HEIGHT - plane_height

        game_screen.blit(plane_img, (plane_x, plane_y))

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        game_screen.blit(score_text, (20, 20))
        distance_text = font.render(f"Distance: {distance_covered}", True, (0, 0, 0))
        game_screen.blit(distance_text, (20, 50))

        pygame.display.update()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                run_game = False
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                run_game = False

    pygame.quit()

# **GAME OVER SCREEN**
def game_over_screen():
    root = tk.Tk()
    root.title("Game Over")

    def restart():
        root.destroy()
        restart_game()

    restart_button = tk.Button(root, text="Restart Game", command=restart)
    restart_button.pack(padx=50, pady=100)
    root.mainloop()

# **RESTART GAME FUNCTION**
def restart_game():
    global plane_y, score, distance_covered, buildings
    plane_y = HEIGHT // 2
    score = 0
    distance_covered = 0
    buildings = []
    game_loop()

# **START CAMERA FEED IN A SEPARATE THREAD**
camera_thread = threading.Thread(target=camera_feed, daemon=True)
camera_thread.start()

# **Run Game**
game_loop()
