import tkinter as tk
from tkinter import filedialog
from tkinter import *
from readShp import *
import tkinter.messagebox as mBox
import os

pointsSave = []

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Mini Gis SoftWare")
        w, h = self.maxsize()
        self.geometry("{}x{}".format(w, h))

        self.menubar = tk.Menu(self, bg="lightgrey", fg="black")
        self.filemenu = tk.Menu(self.menubar, tearoff=0,bg="lightgrey"\
        , fg="black")
        self.edit = tk.Menu(self.menubar,tearoff=0,bg="lightgrey"\
        , fg="black")

        self.menubar.add_cascade(label='buffer', menu=self.filemenu)
        self.filemenu.add_command(label='startEdit', command=self.startEdit)
        self.filemenu.add_command(label='endEdit', command=self.endEdit)
        self.filemenu.add_command(label='buffer', command=self.buffer)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Exit', command=self.quit)

        #self.menubar.add_cascade(label='Edit', command=self.edit)
        #self.edit.add_command(label='startEdit', command=self.startEdit)
        #self.edit.add_command(label='startEdit1', command=self.startEdit)

        self.config(menu=self.menubar)
        self.canvas = Canvas(self,background = 'white')
        self.canvas.pack(fill = BOTH,expand = True)
        # with Linux OS
        # This is what enables using the mouse:
        self.canvas.bind("<ButtonPress-1>", self.move_start)
        #self.canvas.bind("<B1-Motion>", self.move_move)
        #linux scroll
        self.canvas.bind("<Button-4>", self.zoomin)
        self.canvas.bind("<Button-5>", self.zoomout)
        self.canvas.bind("<ButtonRelease-1>",self.randomDraw)
        self.canvas.update()

        # --------------------------和后端接轨------------------------
        self.layers = []
        self.nowLayer = -1
        self.click = True
        self.viewList = []
        self.nowPointer = len(self.viewList)-1
        
        #self.draw = False
        frameGeometry = self.geometry()

        '''
        下面是一些开关
        '''
        self.boolEdit = False
        
        #self.test()
        #self.buffer()
    
    def startEdit(self):
        self.boolEdit = True
        mBox.showinfo('提示', '开始编辑。')

    def endEdit(self):
        global pointsSave
        lines = SoloLine(pointsSave)
        self.boolEdit = False
        layer = Layer(3,[lines])
        self.layers.append(layer)
        view = View(layer.extent,self.canvas)
        self.viewList.append(view)
        self.canvas.delete('all')
        layer.draw(self.canvas,view)
        mBox.showinfo('提示', '编辑结束。')
    
    def randomDraw(self,event):
        if not self.boolEdit:
            return 
        global pointsSave
        r = 2
        x = event.x
        y = event.y
        self.canvas.create_oval(x-r,y-r,x+r,y+r)
        defaultView = View(Extent(),self.canvas)
        mapPoint = defaultView.toMapPoint(SoloPoint(x,y))
        pointsSave.append(mapPoint)
    
    def buffer(self):
        Buffer().buffer(self.layers[-1],self.canvas,self.viewList[-1])

    def openShp(self):
        fileName = filedialog.askopenfilename(\
         filetypes=[("shapefile", "*.shp")])
        if fileName:
            sf = ReadSHP()
            path = os.path.abspath(fileName)
            layer = sf.readshp(path)
            layer.bool_drawAttributeOrNot = False
            self.layers.append(layer)
            self.showAll()
        
        return

    def showAll(self):
        view = View(self.layers[-1].extent,self)
        self.viewList.append(view)
        self.layers[-1].draw(self.canvas,view)

    def test(self):
        fileName = "/home/benfen/Personal Project/mini gis/testData/ne_110m_rivers_lake_centerlines/ne_110m_rivers_lake_centerlines.shp"
        sf = ReadSHP()
        path = os.path.abspath(fileName)
        layer = sf.readshp(path)
        layer.bool_drawAttributeOrNot = False
        self.layers.append(layer)
        self.showAll()

    def move_start(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def move_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)
        
    def zoomin(self,event):
        view = self.viewList[-1]
        self.viewList.append(view)
        
        view.changeView('Zoomin')
        self.reDraw()
        return

    def zoomout(self,event):
        view = self.viewList[-1]
        self.viewList.append(view)
        
        view.changeView('Zoomout')
        self.reDraw()
        return
    
    def reDraw(self):
        self.canvas.delete('all')
        self.layers[-1].draw(self.canvas,self.viewList[-1])
        return

    def toCanvas(self,x,y):
        return  self.canvas.canvasx(x), self.canvas.canvasy(y)

if __name__ == "__main__":
    translatebook = MainWindow()
    translatebook.mainloop()