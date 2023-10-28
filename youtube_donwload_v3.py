import os #系統檔案存取套件
from pytube import YouTube #youtube download =套件
from pytube.cli import on_progress #Youtube 的下載進度條顯示功能
import subprocess #模擬cmd啟動套件
import tkinter as tk
import time #時間套件:取得現在系統時間


#合併file1和file2檔案, 且輸出到outputfile位置
def merge(file1, file2, output_file):
    
    '''
    file1:str, 檔案一絕對路徑
    file2:str, 檔案2絕對路徑 
    output_fil3:str, 輸出位置絕對路徑
    return:None
    '''
    
    '''
    #input to cmd:
    #kwags:
        i: input file
        c copy:merge
        y:if the same name exsits, cover it without checking
    '''
    cmd = f'ffmpeg -i \"{file1}\" -i \"{file2}\" -c copy -y \"{output_file}\"'
    cmd_cd = f'cd "{now_path}"'
    
    try:
        
        #run shell --cmd
        subprocess.run(cmd_cd, shell=True, check=True)
        subprocess.run(cmd, shell=True, check=True)
        
    except:
    
        print("命令出錯了!")

#下載youtube網址影片檔(最高畫質)和音軌(最高mp3比特率)2個檔案, 儲存至現在目錄
def download(site):
    
    '''
    site:str, youtube影片網址
    return:None
    '''
    
    #https://www.youtube.com/watch?v=BWBSkjXznIc&ab_channel=%E5%94%90%E7%B6%BA%E9%99%BD%E5%AE%98%E6%96%B9%E5%B0%88%E5%B1%AC%E9%A0%BB%E9%81%93
   
    #計算開始執行的時間
    start = time.time() 
   
    #建youtube物件 以便後續操作與訪問
    yt = YouTube(site, on_progress_callback = on_progress)
    mp4s = yt.streams.filter(type = 'video', progressive = False) #篩選物件串流 指定為video 且非包含影像與音訊
    mp4s = mp4s.order_by('resolution') #以畫質排序 由低到高

    '''
    以下非必要, 僅方便了解程式運作和除錯
    ------------------------------------
    '''
    print (yt.title) #印出影片標題
    
    try:
        
        for mp4 in reversed(mp4s): #若為串列印出全部元素
            
            print(mp4)
            print()
            
    except: #否則輸出該物件
        
        print(mp4s)
    
    print(mp4s[-1]) #印出最後一個元素 --畫質最高者
    '''
    -------------------------------------
    '''
    
    file_v = mp4s[-1].default_filename #產生影片預設檔名 --file_v
    mp4s[-1].download(filename_prefix = 'only video') #下載上2行選擇的影片
    
    #同上面只差改成audio
    audios = yt.streams.filter(type = 'audio', progressive = False)
    audios = audios.order_by('abr')
    
    '''
    以下非必要, 僅方便了解程式運作和除錯
    ------------------------------------
    '''
    try:
        
        for audio in reversed(audios):
            
            print(audio)
            print()
            
    except:
        
        print('djoajf', audio)
    
    
    print(audios[-1])
    '''
    -----------------------------
    '''
    
    file_a = audios[-1].default_filename
    audios[-1].download(filename_prefix = 'only audio')
    
    print ("merging...")
    
    #合併影片和音軌
    merge(now_path + "only video"+str(file_v), now_path+"only audio"+str(file_a), "output"+str(yt.title)+'.mp4')
    
    print ('Done')
    
    
    end = time.time()
    print (end - start) #印出執行時長

#現在工作path --now_path
now_path = os.path.abspath(os.getcwd()).replace('\\', '/')+'/'

def start():
    
    download(str(tk.Entry.get (keywords)))

#tkinter 視窗
window = tk.Tk()
window.title ('tkinter testing') #設定標題
window.geometry ("1000x750+0+0") #設定視窗大小與位置
window.resizable(0, 0)

#關鍵字輸入框
keywords = tk.Entry (window, width = 25, highlightbackground = 'black')
keywords.grid()

#關鍵字送出按鈕
button = tk.Button (window, text = "送出", bg = 'blue', fg = 'white', command = start)
button.grid()

window.mainloop() #啟動視窗