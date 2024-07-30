## 研究方法
選擇 Python 作為編程語言，使用 Pygame 套件製作遊戲，給 ChatGPT 指令，並請它產生程式碼。

## 研究目的
1. 透過摸索掌握關鍵字詞，理解如何準確地下指令給 Chat GPT。    
2. 了解 Chat GPT 3.5 目前的能力範圍。   
  
## 使用工具
1. ChatGPT 3.5  
2. Visual Studio Code

## 研究步驟
### 1.下指令給 ChatGPT  
__ChatGPT 產生安裝 Pygame 套件的程式碼及俄羅斯方塊遊戲程式碼(省略)。__
  
![image](https://github.com/sunnyliuaviation/Tetris-in-Python-by-ChatGPT/blob/main/image/%E4%B8%8B%E6%8C%87%E4%BB%A4.png)
  
__ChatGPT 在產出程式碼之後外加說明__    
  
![image](https://github.com/sunnyliuaviation/Tetris-in-Python-by-ChatGPT/blob/main/image/ChatGPT%20%E8%AA%AA%E6%98%8E.png)

### 2.實際執行 ChatGPT 給的程式碼
__安裝 Pygame 套件__
  
```python
pip install pygame
```

__程式碼執行__  
程式碼出現錯誤，此時可以將報錯的內容給 ChatGPT ，並讓它修正。  

![image](https://github.com/sunnyliuaviation/Tetris-in-Python-by-ChatGPT/blob/main/image/Error.png)

### 3.確認程式碼可以執行  
1. 確保方塊自動落下  
2. 方塊連成一行後是否會消除並計分  
3. 方向鍵運作是否正常  
4. 按向上鍵方塊是否會旋轉   
5. 確保方塊堆到頂部時遊戲結束並跳離迴圈  
  
![image](https://github.com/sunnyliuaviation/Tetris-in-Python-by-ChatGPT/blob/main/image/%E5%9F%B7%E8%A1%8C%E9%81%8A%E6%88%B2.png)

## 研究總結  
在本次研究中，探討了使用 ChatGPT 3.5 作為輔助工具來創建經典的俄羅斯方塊遊戲，也有一些發現：  

__明確指令的重要性__  
在與 ChatGPT 互動的過程中，使用精確的關鍵字和明確的指令至關重要。具體且清晰的描述可以幫助 ChatGPT 生成更準確和有效的程式碼。

__ChatGPT 3.5 的能力範圍__  
ChatGPT 3.5 能夠產生大部分的程式碼，包括基本的遊戲邏輯和功能實現，如方塊的自動落下、方塊消除計分系統、方向鍵控制、方塊旋轉，以及遊戲結束條件等。然而，對於較複雜或特定邏輯的程式碼，則必須引導 ChatGPT 3.5 調整及修正。

__程式碼的調整與修正__  
在實際執行 ChatGPT 生成的程式碼過程中，會遇到錯誤或功能無效的情況。透過將報錯訊息提供給 ChatGPT，可以得到程式碼修正建議並解決問題，雖然並不是每項問題 ChatGPT 都能解決，但這展現 ChatGPT 在程式碼除錯的潛在應用價值。

__未來研究目標__   
探索更複雜的功能：加入按空白鍵使方塊直接落到底部功能、顯示即將出現的方塊、自動調整速度等。  
使用不同的工具與技術：嘗試使用其他開發框架或工具，拓展技術視野。  
進一步優化程式碼：包括優化遊戲性能和改善遊戲體驗。 

## 總結  
ChatGPT 3.5 仍需要人類的引導才能完成專案，但本次研究展示了它作為開發輔助工具的潛力。特別是在初學者學習編程和開發遊戲時，透過清晰明確的指令，能夠有效利用 ChatGPT 作為輔助工具，提高開發效率。
