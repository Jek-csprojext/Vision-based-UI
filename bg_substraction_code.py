import cv2
import webbrowser
import numpy as np
import time

# Python version = 3.13.0
# cv2.__version__ = 4.10.0
# np.__version__ = 2.1.3

bg_subtractor = cv2.createBackgroundSubtractorMOG2()

url = 'https://www.youtube.com/' # 連結網址
Filepath = 'C:/Users/user/Desktop/HCI HW4/' # 照片儲存路徑

hold_time = 0.8 # 手需停留在熱區超過0.8s才能觸發指令
last_enter_time = {
    'Close': None,'Open Link': None, 'Capture Photo': None
    }

# 設定三個熱區範圍 (x_start, x_end, y_start, y_end)
# 長寬比例預設為Length: 120, Width: 100
trigger_zones = {
    'Close': (50, 170, 50, 150),  # 左
    'Open Link': (250, 370, 50, 150),  # 中
    'Capture Photo': (450, 570, 50, 150)  # 右
}

# 啟動攝影機
cap = cv2.VideoCapture(0)

# 確認攝影機成功讀取畫面
while True:
    ret, frame = cap.read()
    if not ret:
        print('無法成功讀取')
        break

    # 背景相減
    fg_mask = bg_subtractor.apply(frame)

    # 顯示熱區的位置
    for command, (x, y, w, h) in trigger_zones.items():
        cv2.rectangle(frame, (x, w), (y, h), (255, 0, 0), 2)  # 藍框
        cv2.putText(frame, command, (x, w - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # 檢查熱區
    for command, (x, y, w, h) in trigger_zones.items():
        
        # 擷取熱區範圍
        # ROI = Region of Interest
        roi = fg_mask[w:h, x:y]
        change_count = np.sum(roi > 180)  # 計算熱區中像素值>130的數量

        # 設定閾值
        threshold = 1500
        if change_count > threshold:
            if last_enter_time[command] == None:
                last_enter_time[command] = time.time() # 第一次進入熱區的時間
            elif time.time() -  last_enter_time[command] >= hold_time: # 停留時間超過hold_time則觸發指令
                if command == 'Close':
                    print('關閉程式')
                elif command == 'Open Link':
                    print('開啟連結')
                    webbrowser.open_new_tab(url)
                else:
                    print('拍照')
                    cv2.imwrite(Filepath + 'img.png', frame)
                    print('照片儲存成功')

                cap.release()
                cv2.destroyAllWindows()
                exit()

        else:
            last_enter_time[command] = None # 重新計算

    # 顯示影像
    cv2.imshow('Background substraction test', frame)

    # 按q退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
