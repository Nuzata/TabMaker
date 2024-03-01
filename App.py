import os
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from TabMaker import tab_maker
import ctypes

#Windowsでtkinterウィンドウの解像度を良くする呪文。
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
except:
    pass

class Application():
    def __init__(self):
        #tabmakerクラスのインスタンス化
        self.tm = tab_maker()
        
        # rootの作成
        root = Tk()
        root.geometry("600x300")
        root.title("TabMaker")
        
        # 入力フォルダ用のフレームの作成
        input_folder_frame = ttk.Frame(root, padding=10)
        input_folder_frame.grid(row=0, column=0,columnspan=2,sticky=E)

        # 入力フォルダ用ラベルの作成
        IDirLabel = ttk.Label(input_folder_frame, text="元画像フォルダ参照＞＞", padding=(5, 2))
        IDirLabel.pack(side=LEFT)
        
        # 入力フォルダ用エントリーの作成
        self.input_folder_entry = StringVar(value="未選択")
        IDirEntry = ttk.Entry(input_folder_frame, textvariable=self.input_folder_entry, width=30)
        IDirEntry.pack(side=LEFT)

        # 入力フォルダ用ボタンの作成
        IDirButton = ttk.Button(input_folder_frame, text="参照", command=self.Idirdialog_clicked)
        IDirButton.pack(side=LEFT)
        
        # 出力フォルダ用のフレームの作成
        output_folder_frame = ttk.Frame(root, padding=10)
        output_folder_frame.grid(row=1, column=0,columnspan=2,sticky=E)

        # 出力フォルダ用ラベルの作成
        ODirLabel = ttk.Label(output_folder_frame, text="出力フォルダ参照＞＞", padding=(5, 2))
        ODirLabel.pack(side=LEFT)

        #出力フォルダ用エントリーの作成
        self.output_folder_entry = StringVar(value="未選択")
        ODirEntry = ttk.Entry(output_folder_frame, textvariable=self.output_folder_entry, width=30)
        ODirEntry.pack(side=LEFT)

        # 出力フォルダ用ボタンの作成
        ODirButton = ttk.Button(output_folder_frame, text="参照", command=self.Odirdialog_clicked)
        ODirButton.pack(side=LEFT)
        
        #インプットディレクトリ用フレームの作成
        finded_imgnum_frame = ttk.Frame(root,padding=10)
        finded_imgnum_frame.grid(row=2,column=0,sticky=E)
        
        #見つかったファイル数を示すテキストの配置
        self.finded_imgnum_label =  ttk.Label(finded_imgnum_frame,text="画像　：　0枚")
        self.finded_imgnum_label.pack(side=LEFT)
        
        #画像結合時の設定を行うフレーム
        output_img_setting_frame = ttk.Frame(root,padding = 10)
        output_img_setting_frame.grid(row=3,column=0,rowspan=2,columnspan=2,sticky=E)

        #vsepareteの説明
        vseparate_label = ttk.Label(output_img_setting_frame,
                                         text="画像一枚あたりの行数：")
        vseparate_label.pack(side=LEFT)

        #vseparate選択コンボボックス
        self.vseparate = IntVar(value=7)
        vseparate_value_list=[1,2,3,4,5,6,7,8,9,10]
        vseparate_combobox = ttk.Combobox(output_img_setting_frame,
                                               width=5,
                                               value=vseparate_value_list,
                                               textvariable=self.vseparate,
                                               state="readonly")
        vseparate_combobox.pack(side=LEFT)

        #vspacingの説明
        vspacing_label = ttk.Label(output_img_setting_frame,
                                   text="画像間の余白：")
        vspacing_label.pack(side=LEFT)

        #vspacing選択コンボボックス
        self.vspacing = IntVar(value=5)
        vspacing_value_list = [5,10,15,20,25,30]
        vspacing_combobox = ttk.Combobox(output_img_setting_frame,
                                         width=5,
                                         value=vspacing_value_list,
                                         textvariable=self.vspacing,
                                         state="readonly")
        vspacing_combobox.pack(side=LEFT)

        #実行ボタンフレームの作成
        exebutton_frame = ttk.Frame(root, padding=10)
        exebutton_frame.grid(row=5,column=1,sticky=W)

        # 実行ボタンの設置
        exebutton= ttk.Button(exebutton_frame, text="開始", command=self.conductMain)
        exebutton.pack(fill = "x", padx=30, side = TOP)  
    
        #アプリケーションの開始
        root.mainloop()
    
    #入力フォルダ指定の関数
    def Idirdialog_clicked(self):
        iDir = os.path.abspath(os.path.dirname(__file__))
        iDirPath = filedialog.askdirectory(initialdir = iDir)
        
        #フォルダ選択がキャンセルされた場合は以後の処理を飛ばす
        if iDirPath == "":
            return
        
        #テキストボックスに反映
        self.input_folder_entry.set(iDirPath)
        
        #tab_makerクラスに入力フォルダのディレクトリを与える
        self.tm.set_inputdir(iDirPath)
        
        #見つかった写真の数を表示する
        self.finded_imgnum_label["text"] = "画像　：　"+str(len(self.tm.input_list)) + "枚"
        
    # 出力フォルダ指定の関数
    def Odirdialog_clicked(self):
        oDir = os.path.abspath(os.path.dirname(__file__))
        oDirPath = filedialog.askdirectory(initialdir = oDir)
        
        #フォルダ選択がキャンセルされた場合は以後の処理を飛ばす
        if oDirPath == "":
            return
        
        #テキストボックスに反映
        self.output_folder_entry.set(oDirPath)
        
        #tab_makerクラスに出力ディレクトリを与える
        self.tm.set_outputdir(oDirPath)
        
    # 開始ボタン押下時の実行関数
    def conductMain(self):
        #画像読込先ディレクトリが存在するかの確認
        if not os.path.isdir(self.input_folder_entry.get()) :   
            messagebox.showwarning("エラー",
                                   "画像読み込み先のフォルダが見つかりません")
            return
        
        #結果出力先ディレクトリが存在するかの確認
        if not os.path.isdir(self.output_folder_entry.get()) :   
            messagebox.showwarning("エラー",
                                   "結果出力先のフォルダが見つかりません")
            return
        
        #画像の枚数を確認
        if len(self.tm.input_list) == 0:
            messagebox.showerror("エラー",
                                 "指定フォルダに画像がありません")

        #実行
        self.tm.set_outputvariables(vseparate=self.vseparate.get(),vspacing=self.vspacing.get())
        result = self.tm.main()
        
        if result == True:
            messagebox.showinfo("完了",
                                "実行完了")
        else:
            messagebox.showerror("失敗",
                                 "実行失敗")
    
if __name__ == "__main__":
    App = Application()
