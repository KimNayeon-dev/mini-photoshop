from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter.simpledialog import *
from tkinter.colorchooser import *
from tkinter import filedialog
from wand.image import *

# 모든 함수들이 공통적으로 사용할 전역 변수 선언부
window, canvas, paper = None, None, None
# photo는 원본 이미지, photo2는 처리 결과를 저장할 변수, photo3는 원본을 백업
photo, photo2 = None, None
oriX, oriY, newX, newY = 0, 0, 0, 0 # 원본 이미지의 폭과 높이를 저장하는 변수
x1, y1, x2, y2 = None, None, None, None
openNum, newNum = 0, 0
penColor = 'black'
penWidth = 3


# 함수 정의부
# 함수 정의 부분

def displayImage(img, width, height) :
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY
    
    # 이미지를 불러오면 캔버스 크기를 이미지에 맞춤
    # window.geometry(str(width)+"x"+str(height))
    if canvas != None :  # 캔버스가 None이 아니면
        canvas.destroy() # 캔버스를 삭제

    canvas = Canvas(window, width=width, height=height) # 새 캔버스
    paper = PhotoImage(width=width, height=height) # 새 이미지
    canvas.create_image((width/2, height/2), image=paper, state="normal")

    '''
    # blob = Binary Large Object
    # 이미지, 사운드, 비디오 등 멀티 미디어를 다룰 때 사용하는 객체
    blob = img.make_blob(format='RGB')
    for i in range(0, width) :
        for k in range(0, height) :
            r = blob[(i*3*width)+(k*3) + 0]
            g = blob[(i*3*width)+(k*3) + 1]
            b = blob[(i*3*width)+(k*3) + 2]
            paper.put("#%02x%02x%02x"%(r,g,b), (k, i))
    '''
    # format='png'는 픽셀을 한칸한칸 처리하는 format='RGB'에 비해 처리 속도가 빠름
    blob = img.make_blob(format='png')
    paper.put(blob)

    canvas.place(x=(1050-width)/2, y=(940-height)/2)

def mouseClick(event) :
    global x1, y1, x2, y2, penColor, penWidth
    x1, y1 = (event.x), (event.y)

def mouseDrop(event) :
    global x1, y1, x2, y2, penColor, penWidth
    x2, y2 = (event.x), (event.y)
    canvas.create_line(x1, y1, x2, y2, width=penWidth, fill=penColor)

def circleClick(event) :
    global x1, y1, x2, y2, penColor, penWidth
    x1, y1 = (event.x-1), (event.y-1)

def circleDrop(event) :
    global x1, y1, x2, y2, penColor, penWidth
    x2, y2 = (event.x+1), (event.y+1)
    canvas.create_oval(x1, y1, x2, y2, width=penWidth, fill=None, outline=penColor)

def recDrop(event) :
    global x1, y1, x2, y2, penColor, penWidth
    x2, y2 = (event.x+1), (event.y+1)
    canvas.create_rectangle(x1, y1, x2, y2, width=penWidth, fill=None, outline=penColor)

def paint(event) :
    global x1, y1, x2, y2, penColor, penWidth
    x1, y1 = (event.x-1), (event.y-1)
    x2, y2 = (event.x+1), (event.y+1)
    canvas.create_oval(x1, y1, x2, y2, width=penWidth, fill=penColor, outline=penColor)

def getColor() :
    global x1, y1, x2, y2, penColor, penWidth
    color = askcolor()
    penColor = color[1]

def getWidth() :
    global x1, y1, x2, y2, penColor, penWidth
    penWidth = askinteger("펜 두께", "펜 두께(1~10)를 입력하세요.", minvalue=1, maxvalue=10)

def func_pen() :
    global x1, y1, x2, y2, penColor, penWidth
    canvas.bind("<B1-Motion>", paint)

def func_line() :
    global x1, y1, x2, y2, penColor, penWidth
    canvas.bind("<Button-1>", mouseClick) # canvas.bind(이벤트명, 실행할 함수)
    canvas.bind("<ButtonRelease-1>", mouseDrop) # 왼쪽 마우스(Button-1)를 뗄 때(Release)

def func_circle() :
    global x1, y1, x2, y2, penColor, penWidth
    canvas.bind("<Button-1>", circleClick)
    canvas.bind("<ButtonRelease-1>", circleDrop)

def func_rectangle() :
    global x1, y1, x2, y2, penColor, penWidth
    canvas.bind("<Button-1>", circleClick)
    canvas.bind("<ButtonRelease-1>", recDrop)
    
def func_new() :
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY, openNum, newNum, fileName, frameDraw, penColor, penWidth
    ask_save()
    
    if canvas != None :  # 캔버스가 None이 아니면
        canvas.destroy() # 캔버스를 삭제
        
    width = askinteger("가로 사이즈", "캔버스의 <가로> 사이즈(1~800)", minvalue=1, maxvalue=800)
    height = askinteger("세로 사이즈", "캔버스의 <세로> 사이즈(1~750)", minvalue=1, maxvalue=750)
    canvas = Canvas(window, width=width, height=height, bg="white") # 새 캔버스
    canvas.place(x=(1080-width)/2, y=(920-height)/2)

    openNum += 1 # 파일이 열린 횟수를 카운트
    newNum += 1
    
    # 그리기툴을 넣을 프레임
    if newNum > 1 :
        frameDraw.destroy()
    frameDraw = Frame()
    frameDraw.configure(width=40, height=850, bg='Gray36', bd=1, relief='solid')
    frameDraw.pack(side='left', anchor='n')
    frameDraw.propagate(0)

    # 그리기 - 펜툴
    buttonPen0 = Button(frameDraw, text="Draw", state='disabled')
    buttonPen0.configure(font=('Arial', 9), disabledforeground='white',
                         bg='Gray26', width=5)
    buttonPen1 = Button(frameDraw, text="Color", command=getColor)
    buttonPen1.configure(font=('Arial', 9), fg='white', bg='Gray30', cursor='hand2',
                         bd=1, relief='ridge', overrelief='sunken',
                         activebackground='Gray28', activeforeground='white')
    buttonPen2 = Button(frameDraw, text="Width", command=getWidth)
    buttonPen2.configure(font=('Arial', 9), fg='white', bg='Gray30', cursor='hand2',
                         bd=1, relief='ridge', overrelief='sunken',
                         activebackground='Gray28', activeforeground='white')
    buttonPen3 = Button(frameDraw, text="Pen", command=func_pen)
    buttonPen3.configure(font=('Arial', 9), fg='white', bg='Gray30', cursor='hand2',
                         bd=1, relief='ridge', overrelief='sunken',
                         activebackground='Gray28', activeforeground='white')

    buttonPen0.pack()
    buttonPen1.pack()
    buttonPen2.pack()
    buttonPen3.pack()
    
    # 그리기 - 도형툴
    buttonShape0 = Button(frameDraw, text="Shape", state='disabled')
    buttonShape0.configure(font=('Arial', 9), disabledforeground='white',
                           bg='Gray26', width=5)
    buttonShape1 = Button(frameDraw, text="Line", command=func_line)
    buttonShape1.configure(font=('Arial', 9), fg='white', bg='Gray30', cursor='hand2',
                           bd=1, relief='ridge', overrelief='sunken',
                           activebackground='Gray28', activeforeground='white')
    buttonShape2 = Button(frameDraw, text="Circle", command=func_circle)
    buttonShape2.configure(font=('Arial', 9), fg='white', bg='Gray30', cursor='hand2',
                           bd=1, relief='ridge', overrelief='sunken',
                           activebackground='Gray28', activeforeground='white')
    buttonShape3 = Button(frameDraw, text="Rentangle", command=func_rectangle)
    buttonShape3.configure(font=('Arial', 9), fg='white', bg='Gray30', cursor='hand2',
                           bd=1, relief='ridge', overrelief='sunken',
                           activebackground='Gray28', activeforeground='white')

    buttonShape0.pack()
    buttonShape1.pack()
    buttonShape2.pack()
    buttonShape3.pack()

    # 파일 정보 표시 라인
    if openNum > 1 : # 파일이 2번 이상 열렸다면
        fileName.destroy() # 앞에 있던 label을 파괴하고 새로 생성
    fileName = Label(window, text="/New file.png")
    fileName.configure(font=('Arial', 10), anchor='nw', fg='white',
                       width=1350, height=1, padx=10,
                       bd=1, bg='Gray32', relief='solid')
    fileName.pack()

def func_open() :
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY, openNum, fileName
    ask_save()
    
    myFile = askopenfilename(parent=window, filetype=(("JPEG", "*.JPG;*.JPEG;*.JPE"), ("PNG", "*.PNG;*.PNG"), ("CompuServe GIF", "*.GIF"), ("모든 파일", "*.*")))
    # 이미지는 GIF, JPG, PNG를 불러와 모두 처리하기 위해 PhotoImage()가 아닌
    # Wand 라이브러리에서 제공하는 Image()를 사용

    openNum += 1 # 파일이 열린 횟수를 카운트
    # 파일 정보 표시 라인
    if openNum > 1 : # 파일이 2번 이상 열렸다면
        fileName.destroy() # 앞에 있던 label을 파괴하고 새로 생성
    fileName = Label(window, text=myFile)
    fileName.configure(font=('Arial', 10), anchor='nw', fg='white',
                       width=1350, height=1, padx=10,
                       bd=1, bg='Gray32', relief='solid')
    fileName.pack()
    
    photo = Image(filename=myFile) # Image 메소드에 photo(원본 이미지) 저장
    oriX = photo.width  # 원본 이미지의 가로 사이즈를 oriX에 저장
    oriY = photo.height # 원본 이미지의 가로 사이즈를 oriY에 저장

    # photo2는 처리 결과를 저장할 변수
    photo2 = photo.clone() # photo를 복사하여 photo2에 저장
    newX = photo2.width
    newY = photo2.height
    displayImage(photo, oriX, oriY)

def func_save() :
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY

    # func_open() 함수로 생성되는 photo2가 없으면
    # 아래의 코드를 실행하지 않고 빠져나감
    if photo2 == None : # photo2가 없다면 return
        messagebox.showinfo("오류", "이미지가 없습니다.")
        return

    # 대화 상자로부터 넘겨받은 파일 정보를 saveFile에 저장
    saveFile = asksaveasfile(parent=window, mode="w", defaultextension=".png", filetypes=(("JPEG", "*.JPG;*.JPEG;*.JPE"), ("PNG", "*.PNG;*.PNG"), ("CompuServe GIF", "*.GIF"), ("모든 파일", "*.*")))
    savePhoto = photo2.convert("png") # 결과 이미지(photo2) 확장자 변환
    savePhoto.save(filename=saveFile.name) # 파일 저장창에서 입력이름으로 저장

def exit() :
        window.quit()
        window.destroy()

def func_exit() :
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY
    if canvas != None : # 만약 캔버스가 비어있지 않다면
        # 안내 메세지 출력를 출력하고 사용자가 누른 버튼 값을 response에 저장 
        response= messagebox.askyesnocancel(title="안내", message="파일을 저장하시겠습니까?")
        
        if response == 1 : # 예
            func_save()
            exit()
        elif response == 0 : # 아니오
            exit()
        else : # 취소
            return
        
    else : # 캔버스가 비어있다면 프로그램 종료
        exit()

# 편집 시 수정할 이미지(photo2)가 없으면 오류 메세지와 함께 파일 열기창이 뜸
def error_message() :
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY
    if photo2 == None :
        messagebox.showinfo("오류", "이미지가 없습니다.")
        func_open()

def ask_save() :
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY
    if canvas != None :
        response= messagebox.askyesnocancel(title="안내", message="아직 저장하지 않은 파일이 존재합니다.\n저장하시겠습니까?")
        
        if response == 1 : # 예
            func_save()
            return
        elif response == 0 : # 아니오
            return
        else : # 취소
            return
        
    else : # 캔버스가 비어있다면 넘어가기
        return

def func_zoomIn() :
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY
    error_message()

    # askinteger() 함수로 정수형 데이터로 입력받고 scale에 저장(2배~4배)
    scale = askinteger("확대", "확대할 배수를 입력하세요(2~4)", minvalue=2, maxvalue=4)
    # resize()함수로 photo2의 newX, newY에 scale 값을 곱한 뒤 저장(int형)
    photo2.resize(int(newX*scale), int(newY*scale))
    newX = photo2.width  # newX에 변경된 width값 저장
    newY = photo2.height # newY에 변경된 height값 저장
    displayImage(photo2, newX, newY) # 수정된 photo2 이미지를 보여줌

def func_zoomOut() :
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY
    error_message()

    # askinteger() 함수로 정수형 데이터로 입력받고 scale에 저장(-2배~-4배)
    scale = askinteger("축소", "축소할 배수를 입력하세요(2~4)", minvalue=2, maxvalue=4)
    # resize()함수로 photo2의 newX, newY에 scale 값을 나눈 뒤 저장(int형)
    photo2.resize(int(newX/scale), int(newY/scale))
    newX = photo2.width  # newX에 변경된 width값 저장
    newY = photo2.height # newY에 변경된 height값 저장
    displayImage(photo2, newX, newY) # 수정된 photo2 이미지를 보여줌

def func_mirrorW() :
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY
    error_message()
    
    photo2.flip() # FLIP() 함수로 상하 반전
    newX = photo2.width  # newX에 변경된 width값 저장
    newY = photo2.height # newY에 변경된 height값 저장
    displayImage(photo2, newX, newY) # 수정된 photo2 이미지를 보여줌

def func_mirrorH() :
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY
    error_message()
    
    photo2.flop() # FLOP() 함수로 좌우 반전
    newX = photo2.width  # newX에 변경된 width값 저장
    newY = photo2.height # newY에 변경된 height값 저장
    displayImage(photo2, newX, newY) # 수정된 photo2 이미지를 보여줌

def func_rotate() :
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY
    error_message()

    # askinteger() 함수로 정수형 데이터로 입력받고 degree에 저장(0도~360도)
    degree = askinteger("회전", "회전할 각도를 입력하세요", minvalue=0, maxvalue=360)
    photo2.rotate(degree) # rotate() 함수로 입력받은 degree 값 만큼 회전
    newX = photo2.width  # newX에 변경된 width값 저장
    newY = photo2.height # newY에 변경된 height값 저장
    displayImage(photo2, newX, newY) # 수정된 photo2 이미지를 보여줌

def func_bright() :
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY
    error_message()

    # askinteger() 함수로 정수형 데이터로 입력받고 value에 저장(0~100)
    value = askinteger("밝게", "값을 입력하세요(0~100)", minvalue=0, maxvalue=100)
    # modulate(명도, 채도, 색상) 함수로 value값 만큼 밝기 수정
    # 100(~200)을 기준으로 밝아지기 때문에 +100하여 value를 상대값으로 인식
    photo2.modulate((value+100), 100, 100)
    newX = photo2.width  # newX에 변경된 width값 저장
    newY = photo2.height # newY에 변경된 height값 저장
    displayImage(photo2, newX, newY) # 수정된 photo2 이미지를 보여줌

def func_dark() :
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY
    error_message()

    # askinteger() 함수로 정수형 데이터로 입력받고 value에 저장(0~100)
    value = askinteger("어둡게", "값을 입력하세요(0~100)", minvalue=0, maxvalue=100)
    # modulate(명도, 채도, 색상) 함수로 value값 만큼 조절
    # (0~)100을 기준으로 어두워지기 때문에 100에서 -value하여 상대값으로 인식
    photo2.modulate((100-value), 100, 100)
    newX = photo2.width  # newX에 변경된 width값 저장
    newY = photo2.height # newY에 변경된 height값 저장
    displayImage(photo2, newX, newY) # 수정된 photo2 이미지를 보여줌

def func_saturationH() :
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY
    error_message()

    # askinteger() 함수로 정수형 데이터로 입력받고 value에 저장(0~100)
    value = askinteger("채도", "값을 입력하세요(0~100)", minvalue=0, maxvalue=100)
    # modulate(명도, 채도, 색상) 함수로 value값 만큼 밝기 수정
    # 100(~200)을 기준으로 쨍해지기 때문에 +100하여 value를 상대값으로 인식
    photo2.modulate(100, (value+100), 100)
    newX = photo2.width  # newX에 변경된 width값 저장
    newY = photo2.height # newY에 변경된 height값 저장
    displayImage(photo2, newX, newY) # 수정된 photo2 이미지를 보여줌

def func_saturationL() :
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY
    error_message()

    # askinteger() 함수로 정수형 데이터로 입력받고 value에 저장(0~100)
    value = askinteger("채도", "값을 입력하세요(0~100)", minvalue=0, maxvalue=100)
    # modulate(명도, 채도, 색상) 함수로 value값 만큼 조절
    # (0~)100을 기준으로 탁해지기 때문에 100에서 -value하여 상대값으로 인식
    photo2.modulate(100, (100-value), 100)
    newX = photo2.width  # newX에 변경된 width값 저장
    newY = photo2.height # newY에 변경된 height값 저장
    displayImage(photo2, newX, newY) # 수정된 photo2 이미지를 보여줌

def func_bw() :
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY
    error_message()

    photo2.type="grayscale" # type() 함수로 이미지를 흑백으로 전환
    newX = photo2.width  # newX에 변경된 width값 저장
    newY = photo2.height # newY에 변경된 height값 저장
    displayImage(photo2, newX, newY) # 수정된 photo2 이미지를 보여줌

def func_autoZoomIn() :
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY
    error_message()

    # 데이터를 입력 받지 않고 자동으로 1.5배씩 확대
    photo2.resize(int(newX*1.5), int(newY*1.5))
    newX = photo2.width  # newX에 변경된 width값 저장
    newY = photo2.height # newY에 변경된 height값 저장
    displayImage(photo2, newX, newY) # 수정된 photo2 이미지를 보여줌

def func_autoZoomOut() :
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY
    error_message()

    # 데이터를 입력 받지 않고 자동으로 1.5배씩 축소
    photo2.resize(int(newX/1.5), int(newY/1.5))
    newX = photo2.width  # newX에 변경된 width값 저장
    newY = photo2.height # newY에 변경된 height값 저장
    displayImage(photo2, newX, newY) # 수정된 photo2 이미지를 보여줌

def func_autoRotate() :
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY
    error_message()
    
    photo2.rotate(90) #데이터를 입력 받지 않고 자동으로 90도 회전
    newX = photo2.width  # newX에 변경된 width값 저장
    newY = photo2.height # newY에 변경된 height값 저장
    displayImage(photo2, newX, newY) # 수정된 photo2 이미지를 보여줌

def func_resetImage() :
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY
    error_message()

    photo2 = photo.clone()
    newX = photo2.width  # newX에 변경된 width값 저장
    newY = photo2.height # newY에 변경된 height값 저장
    displayImage(photo2, newX, newY) # 수정된 photo2 이미지를 보여줌

def func_() :
    global x1, y1, x2, y2


# 메인 코드 부분
window = Tk()
window.geometry("1349x880")
window.resizable(False, False)
window.title("Mini Photoshop(Ver2.0)")

# 메뉴 구현
# 메뉴 자체 생성
mainMenu = Menu(window)
window.config(menu=mainMenu)
window.configure(bg='Gray38')


# 상단 라벨
topImage = PhotoImage(file='./image/bar.png')
topLabel = Label(window, image=topImage)
topLabel.configure(bd=0)
topLabel.pack(side='top', anchor='w')

# 우측 라벨
rightImage = PhotoImage(file='./image/box.png')
rightLabel = Label(window, image=rightImage)
rightLabel.configure(bd=0)
rightLabel.pack(side='right', anchor='n')


# 버튼을 배치해줄 좌측 프레임
frame = Frame(master=window)
frame.configure(width=40, height=850, bg='Gray36', bd=1, relief='solid')
frame.pack(side='left', anchor='n')
frame.propagate(0)


# 버튼 구현
icon1 = PhotoImage(file='./icon/zoomin.png')
icon2 = PhotoImage(file='./icon/zoomout.png')
icon3 = PhotoImage(file='./icon/rotate.png')

button0 = Button(frame, text="Tool", state='disabled')
button0.configure(font=('Arial', 9), disabledforeground='white', bg='Gray26',
                  width=5)

button1 = Button(frame, text="Zoom in", image=icon1, command=func_autoZoomIn)
button1.configure(font=('Arial', 9), fg='white', bg='Gray30', cursor='hand2',
                  bd=1, relief='ridge', overrelief='sunken', 
                  activebackground='Gray28', activeforeground='white')

button2 = Button(frame, text="Zoom out", image=icon2, command=func_autoZoomOut)
button2.configure(font=('Arial', 9), fg='white', bg='Gray30', cursor='hand2',
                  bd=1, relief='ridge', overrelief='sunken', 
                  activebackground='Gray28', activeforeground='white')

button3 = Button(frame, text="Rotate", image=icon3, command=func_autoRotate)
button3.configure(font=('Arial', 9), fg='white', bg='Gray30', cursor='hand2',
                  bd=1, relief='ridge', overrelief='sunken', 
                  activebackground='Gray28', activeforeground='white')

button4 = Button(frame, text="임시", command=func_)
button4.configure(font=('Arial', 9), fg='white', bg='Gray30', cursor='hand2',
                  bd=1, relief='ridge', overrelief='sunken', 
                  activebackground='Gray28', activeforeground='white')

button0.pack()
button1.pack(padx=2, pady=2)
button2.pack(padx=2, pady=2)
button3.pack(padx=2, pady=2)
button4.pack(padx=2, pady=2)


# 스크롤 구현
# scrollbar = Scrollbar()
# scrollbar.pack(side=RIGHT)


# File 상위메뉴 생성
fileMenu = Menu(mainMenu, tearoff=0, bg='Gray32', fg='white', font='Arial',
                activebackground='Gray42')
mainMenu.add_cascade(label="File", menu = fileMenu)
# File 하위메뉴 생성
fileMenu.add_separator() # 구분선 삽입
fileMenu.add_command(label="New file", command=func_new)
fileMenu.add_command(label="Open file", command=func_open)
fileMenu.add_command(label="Save file", command=func_save)
fileMenu.add_separator() # 구분선 삽입
fileMenu.add_command(label="Exit", command=func_exit)
fileMenu.add_separator() # 구분선 삽입


# Edit 상위메뉴 생성
image1Menu = Menu(mainMenu, tearoff=0, bg='Gray32', fg='white', font='Arial',
                  activebackground='Gray42')
mainMenu.add_cascade(label="Edit", menu = image1Menu)
    
# Edit 하위메뉴 생성
image1Menu.add_separator() # 구분선 삽입
image1Menu.add_command(label="Zoom in", command=func_zoomIn)
image1Menu.add_command(label="Zoom out", command=func_zoomOut)
image1Menu.add_separator() # 구분선 삽입
image1Menu.add_command(label="Mirror width", command=func_mirrorW)
image1Menu.add_command(label="Mirror height", command=func_mirrorH)
image1Menu.add_command(label="Rotate", command=func_rotate)
image1Menu.add_separator() # 구분선 삽입


# Image 상위메뉴 생성
image2Menu = Menu(mainMenu, tearoff=0, bg='Gray32', fg='white', font='Arial',
                  activebackground='Gray42')
mainMenu.add_cascade(label="Image", menu = image2Menu)

# Image 하위메뉴 생성
image2Menu.add_separator() # 구분선 삽입
image2Menu.add_command(label="Bright", command=func_bright)
image2Menu.add_command(label="Dark", command=func_dark)
image2Menu.add_separator() # 구분선 삽입
image2Menu.add_command(label="Saturation high", command=func_saturationH)
image2Menu.add_command(label="Saturation low", command=func_saturationL)
image2Menu.add_separator() # 구분선 삽입
image2Menu.add_command(label="BW", command=func_bw)
image2Menu.add_separator() # 구분선 삽입
image2Menu.add_command(label="Reset image", command=func_resetImage)
image2Menu.add_separator() # 구분선 삽입


'''
# 백그라운드 이미지
img = PhotoImage(file='./photoshop.png')
label = Label(window, image=img)
label.pack()
'''


window.mainloop()
