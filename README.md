# Create checkerboard for findChessboardCornersSB

生成圓角棋盤圖用給 findChessboardCornersSB 用，不過也有生成一般標準棋盤的功能。    
有空再打包成命令式的    

---

# Demo 14*9

```python
x = 14
y = 9
interval = 30
img1 = get_standard_chessboard(x, y, interval, direction_circle=True)
img2 = get_SB_standard_chessboard(x, y, interval)
cv2.imshow('img1', img1)
cv2.imshow('img2', img2)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite('./standard_chessboard.png', img1)
cv2.imwrite('./SB_standard_chessboard.png', img2)
```


for findChessboardCornersSB    
![](https://github.com/we684123/create-checkerboard-for-findChessboardCornersSB/blob/main/SB_standard_chessboard.png?raw=true)

for findChessboardCorners    
![](https://github.com/we684123/create-checkerboard-for-findChessboardCornersSB/blob/main/standard_chessboard.png?raw=true)
