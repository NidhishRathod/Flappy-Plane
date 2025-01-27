# Flappy Plane (Hand Gesture Controlled)

Flappy Plane is a gesture-controlled game where players navigate a plane through buildings using **hand movements** captured via a webcam. The game utilizes **OpenCV**, **MediaPipe**, and **Pygame** for real-time hand tracking and gameplay.

## Features

- **Hand Gesture Control:** Move the plane up and down using your hand.
- **Realistic Buildings:** Dynamically drawn skyscrapers with windows and shadows.
- **Obstacle Avoidance:** Navigate through gaps in buildings.
- **Score Tracking:** Earn points for successfully passing buildings.
- **Crash Effects:** Sound and explosion animation on collision.

## Installation

### **Step 1: Install Dependencies**

Ensure you have Python installed, then run:

```
pip install opencv-python mediapipe pygame
```

### **Step 2: Run the Game**

```
python Game.py
```

## Controls

- **Move Up/Down:** Raise or lower your hand in front of the webcam.
- **Quit Game:** Press `Esc` or `Q` in the camera window.
- **Restart Game:** Click "Restart Game" on the pop-up after crashing.

## Dependencies

- Python 3.8+
- OpenCV
- MediaPipe
- Pygame
- Tkinter (for restart popup)

## How It Works

1. **Camera captures hand movements.**
2. **MediaPipe detects the hand's position.**
3. **The plane moves up/down based on hand height.**
4. **Buildings scroll from right to left.**
5. **Avoid hitting buildings and keep flying!**

## Gameplay Preview

![image](https://github.com/user-attachments/assets/ca88baa7-472b-453d-8840-43167c135af4)


## Contributing

Pull requests are welcome! Feel free to improve the code or add new features.

Happy Flying! ✈️

