import cv2
import mediapipe as mp
import webbrowser

#print(cv2.__version__)
#print(mp.__version__)

# Python 3.11.0
# cv2.__version__ = 4.10.0
# mp.__version__ = 0.10.18

mp_drawing = mp.solutions.drawing_utils          # mediapipe 繪圖方法
mp_drawing_styles = mp.solutions.drawing_styles  # mediapipe 繪圖樣式
mp_hands = mp.solutions.hands                    # mediapipe 偵測手掌方法

#　trigger_zone
url = 'https://www.youtube.com/' # 連結網址
Filepath = 'C:/Users/user/Desktop/HCI/HCI HW5/' # 照片儲存路徑

# 設定三個熱區範圍 (x_start, x_end, y_start, y_end)
# 長寬比例預設為Length: 120, Width: 100
trigger_zones = {
    'Close': (50, 170, 50, 150),  # 左
    'Open Link': (250, 370, 50, 150),  # 中
    'Capture Photo': (450, 570, 50, 150)  # 右
}

cap = cv2.VideoCapture(0) # 開啟鏡頭

# mediapipe 啟用偵測手掌
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

    while True:
        ret, img = cap.read()
        if not ret:
            print("無法成功讀取")
            break

        run = False 

        size = img.shape   # 取得攝影機影像尺寸
        w_ = size[1]        # 取得畫面寬度
        h_ = size[0]        # 取得畫面高度
        
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   # 將 BGR 轉換成 RGB
        # 顯示熱區的位置
        for command, (x, y, w, h) in trigger_zones.items():
            cv2.rectangle(img, (x, w), (y, h), (255, 0, 0), 2)  # 藍框
            cv2.putText(img, command, (x, w - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        results = hands.process(img2)                 # 偵測手掌
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                x = hand_landmarks.landmark[7].x * w_   # 取得食指末端 x 座標
                y = hand_landmarks.landmark[7].y * h_   # 取得食指末端 y 座標
                
                if 50 < y < 150 :
                    if 50 < x < 170 :
                        print('關閉程式')
                        run = True
                    elif 250 < x < 370 :
                        print('開啟連結')
                        webbrowser.open_new_tab(url)
                        run = True
                    elif 450 < x < 570 :
                        print('拍照')
                        cv2.imwrite(Filepath + 'img.png', img)
                        print('照片儲存成功')
                        run = True

                    if run:
                        print('指令啟動座標:',(x,y))
                        cap.release()
                        cv2.destroyAllWindows()
                        exit()

                # 將節點和骨架繪製到影像中
                mp_drawing.draw_landmarks(
                    img,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

        cv2.imshow('Mediapipe test', img)
        if cv2.waitKey(5) == ord('q'):
            break    # 按下 q 鍵停止
cap.release()
cv2.destroyAllWindows()