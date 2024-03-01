import pathlib
import cv2
import numpy as np
import os

class tab_maker():
    
    #画像保存先を受け取り起動。画像リストを生成
    def  __init__(self,input_dir="",output_dir="",vseparate=6,vspacing=5):
        
        #出力ディレクトリの設定
        self.output_dir = output_dir
        
        #入力ディレクトリの設定と画像の読み込み
        if input_dir != "":
            self.input_dir = input_dir
            
            #画像パスの読み込み(png>jpg)
            self.input_list = list(pathlib.Path(self.input_dir).glob('**/*.png'))
            if len(self.input_list) == 0:
                self.input_list = list(pathlib.Path(self.input_dir).glob('**/*.jpg'))
            
            print("Find " + str(len(self.input_list)) + " img files.")
            
        #出力時に何枚ずつで結果を生成するか
        self.vseparate = vseparate
        
        #出力時の画像の間の縦スペースの設定
        self.vspacing = vspacing
        
        #トリミング位置
        self.crop_pos_leftup = []
        self.crop_pos_rightdown = []
        
    #画像ファイルの再設定
    def set_inputdir(self,new_input_dir):
        self.input_dir = new_input_dir
        
        #画像パスの読み込み(png>jpg)
        self.input_list = list(pathlib.Path(self.input_dir).glob('**/*.png'))
        if len(self.input_list) == 0:
            self.input_list = list(pathlib.Path(self.input_dir).glob('**/*.jpg'))
        
        print("Find " + str(len(self.input_list)) + " img files.")
    
    #出力先ファイルの再設定
    def set_outputdir(self,new_output_dir):
        self.output_dir = new_output_dir 
    
    #画像リストから画像を全取得
    def get_images(self,printname=False):
        #リストの初期化
        self.img_list = []
        
        #画像を一枚ずつ読み込み
        for i in range(len(self.input_list)):
            img_file_name = str(self.input_list[i])
            img = self.imread(img_file_name,printname=printname)
            height,width = img.shape[:2]
            
            #画像サイズが同じかどうかをチェック
            if i==0:
                self.height = height
                self.width = width
                self.img_list.append(img)
            else:
                if(self.height == height and self.width == width):
                    self.img_list.append(img)
                else:
                    print("This image was excluded because it had a different size from the first image.")
                    print("異なるサイズの画像があったため除外しました")
    
    #余白や、つなげる枚数の設定を更新
    def set_outputvariables(self,vseparate,vspacing):
        self.vseparate = vseparate
        self.vspacing = vspacing
                    
    #画像を指定の二点をもとに切り取る
    def crop_img(self,img,left_up,right_down):
        return img[left_up[1]:right_down[1],left_up[0]:right_down[0]]
    
    #保持しているすべての画像を指定の二点をもとに切り取る
    def crop_img_all(self,left_up,right_down):
        new_img_list = []
        for img in self.img_list:
            crop_img = self.crop_img(img,left_up, right_down)
            new_img_list.append(crop_img)
        self.img_list = new_img_list
    
    #画像を読み込み（日本語対応）　ただし倍率を50%で読み込む（座標確認用）
    def imread(self,filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8,printname=False):
        try:
            n = np.fromfile(filename, dtype)
            img = cv2.imdecode(n, flags)
            height,width = img.shape[:2]
            
            #読み込み画像名を表示
            if printname == True:
                print(str(filename) + ":Image Size:(" + str(height)+","+str(width)+")")
                
            img = cv2.resize(img,(int(width / 2), int(height / 2)))
            return img
        except Exception as e:
            print(e)
            return None
    
    #ディレクトリが日本語を含む場合に備えたimwrite
    def imwrite(self,filename, img, params=None):
        try:
            ext = os.path.splitext(filename)[1]
            result, n = cv2.imencode(ext, img, params)
    
            if result:
                with open(filename, mode='w+b') as f:
                    n.tofile(f)
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False
        
    #切り取り範囲指定
    def get_crop_pos(self):
        
        #切り取り座標をリセット
        self.crop_pos_leftup = []
        self.crop_pos_rightdown = []
        
        #保持画像の一枚目をコピーして保存
        self.get_crop_pos_img = self.img_list[0].copy()
        
        #画像の表示
        cv2.imshow("set_crop_area",self.get_crop_pos_img)
        #sampleWindow内でクリックが発生したとき、click_pos関数を呼び出す
        cv2.setMouseCallback("set_crop_area",self.click_pos_crop)
        
        #ループフラグ
        self.flag = True
        while self.flag:
            #ウィンドウが閉じられていたらFalseを返す
            if not cv2.getWindowProperty("set_crop_area", cv2.WND_PROP_VISIBLE) >= 1:
                return False
            cv2.waitKey(10)
        
        return True
        
    #クリック時に動作する関数
    def click_pos_crop(self,event, x, y, flags, params):
        
        if event == cv2.EVENT_LBUTTONDOWN:              #左クリック時にその座標を保存
            self.crop_pos_leftup = (int(x),int(y))
        elif event == cv2.EVENT_MOUSEMOVE:
            if len(self.crop_pos_leftup) != 0:          #マウスを動かしている間はその座標に沿って四角を描画
                self.get_crop_pos_img = self.img_list[0].copy()
                cv2.rectangle(img = self.get_crop_pos_img,
                              pt1 = self.crop_pos_leftup,
                              pt2 = (int(x),int(y)),
                              color=(125,125,125),
                              thickness=3)
                #表示画像を更新
                cv2.imshow("set_crop_area",self.get_crop_pos_img)
        elif event == cv2.EVENT_LBUTTONUP:              #左ボタンを離したとき、座標を保存。ウィンドウを閉じるフラグをTrueに
            self.crop_pos_rightdown = (int(x),int(y))
            self.flag = False
            cv2.destroyAllWindows()
            
    #画像の結合を行う
    #vseparate:何枚づつで縦結合するか
    #vspacing:縦方向の余白
    def concat(self,vseparate=6,vspacing=5):
        img_list_copy = self.img_list.copy()

        #足りない枚数
        append_num = len(img_list_copy)%vseparate
        
        #足りない枚数分白紙画像を追加
        for i in range(vseparate - append_num):
            white_img=np.full((img_list_copy[0].shape[0],img_list_copy[0].shape[1],img_list_copy[0].shape[2]),255,np.uint8)
            img_list_copy.append(white_img)
    
        #余白の追加
        if vspacing > 0:
            for i,img in enumerate(img_list_copy):
                img_list_copy[i]=cv2.copyMakeBorder(img, vspacing, vspacing, 0, 0,cv2.BORDER_CONSTANT,value=[255,255,255])
        
        #画像の結合と保存
        number = 1
        while len(img_list_copy) >= vseparate:
            self.concat_img = cv2.vconcat(img_list_copy[:vseparate])
            del img_list_copy[:vseparate]
            print("出力:" + self.output_dir + "/result" + str(number) + ".png")
            print(self.imwrite(self.output_dir + "/result" + str(number) + ".png",
                        self.concat_img))
            number=number+1    
            
    #座標を切り取りに対応した形式に整頓する
    def crop_coodinate_cleanup(self,left_up,right_down):
        new_left_up = []
        new_right_down = []
        
        #同じ値の座標であれば切り取れないであるためFalse
        if(left_up[0] == right_down[0]) or (left_up[1] == right_down[1]):
            return False
        
        #x座標について
        if (left_up[0] < right_down[0]):
            new_left_up.append(left_up[0])
            new_right_down.append(right_down[0])
        else:
            new_left_up.append(right_down[0])
            new_right_down.append(left_up[0])
            
        #y座標について
        if (left_up[1] < right_down[1]):
            new_left_up.append(left_up[1])
            new_right_down.append(right_down[1])
        else:
            new_left_up.append(right_down[1])
            new_right_down.append(left_up[1])
        
        self.crop_pos_leftup = new_left_up
        self.crop_pos_rightdown = new_right_down
        
        return True
    
    #実行部
    def main(self):
        
        try:
            #画像が一つも見つからなければ終了
            if len(self.input_list) == 0:
                print("No image")
                return 0
            
            #画像を取得
            self.get_images()
            
            #トリミング範囲を読み込む
            check = self.get_crop_pos()
            if check is False:
                return False
            
            #トリミング範囲の整頓、検査
            check = self.crop_coodinate_cleanup(self.crop_pos_leftup, self.crop_pos_rightdown)
            if check is False:
                return False
            
            #トリミングの実行
            self.crop_img_all(self.crop_pos_leftup, 
                                  self.crop_pos_rightdown)
            
            #画像の結合
            self.concat(vseparate = self.vseparate,
                        vspacing = self.vspacing)
            
            return True
        
        except Exception as e:
            #エラー発生時はエラーをコンソールに表示、実行失敗のFalseを返す
            print(e)
            return False
