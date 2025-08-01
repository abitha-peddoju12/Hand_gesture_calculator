import cv2
import mediapipe as mp
import time
from gesture_utils import count_fingers, is_pinching
from calculator_logic import evaluate_expression

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

expression = ""
last_action_time = 0
cooldown = 1.0  # seconds

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    lmList = []
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append((id, cx, cy))
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    if lmList:
        fingers = count_fingers(lmList)
        totalFingers = sum(fingers)

        # Display gesture count
        cv2.putText(img, f'Fingers: {totalFingers}', (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Pinch action to add gesture to expression
        if is_pinching(lmList) and (time.time() - last_action_time > cooldown):
            if totalFingers == 0:
                expression = ""  # Clear
            elif totalFingers == 1:
                expression += "1"
            elif totalFingers == 2:
                expression += "2"
            elif totalFingers == 3:
                expression += "3"
            elif totalFingers == 4:
                expression += "+"
            elif totalFingers == 5:
                expression += "-"
            elif totalFingers == 6:
                expression += "="  # Use 6 fingers or custom rule for '='
            last_action_time = time.time()

        # If expression includes '=' → evaluate it
        if "=" in expression:
            expression = expression.replace("=", "")
            result = evaluate_expression(expression)
            expression = str(result)

    # Display current expression
    cv2.putText(img, f'Expr: {expression}', (10, 130),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 2)

    # Show output
    cv2.imshow("Hand Gesture Calculator", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
