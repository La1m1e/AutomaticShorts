import pyautogui
import keyboard


def on_ctrl_pressed(e):
    if e.event_type == keyboard.KEY_DOWN and e.name == 'ctrl':
        x, y = pyautogui.position()
        print(f"pyautogui.click(x={x}, y={y})")


# Register the Ctrl key press event
keyboard.hook(on_ctrl_pressed)

# Keep the script running
keyboard.wait('esc')  # Change the key if needed
