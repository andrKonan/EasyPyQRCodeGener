import qrcode
import tkinter as tk
from PIL import ImageTk, Image

window = tk.Tk()
window.title("QR code generator") 
window.minsize(200, 200)

txtAndInputFrame = tk.Frame(master = window, height = 10)
txtAndInputFrame.pack(fill = tk.X)

explainingText = tk.Label(master = txtAndInputFrame, text="Text for converting to QR:")
textEntryToQR = tk.Entry(master = txtAndInputFrame, width = 50)
qrImg = tk.Canvas(width = 350, height = 350)  

explainingText.pack(side = tk.LEFT, anchor = tk.NW)
textEntryToQR.pack(side = tk.RIGHT, anchor = tk.NE, fill = tk.X)
qrImg.pack(side = tk.BOTTOM, anchor = tk.S)

prevText = textEntryToQR.get()

def makeQR(text:str):
	qrcode.make(text).save('qr.png')
	img = Image.open('qr.png')
	size = img.size
	img = ImageTk.PhotoImage(img)
	return (img, size)

img, size = makeQR(textEntryToQR.get())
qrImg.config(width = size[0], height = size[1])
qrImg.create_image(0, 0, anchor = tk.NW, image = img)  
prevText = textEntryToQR.get()

window.update_idletasks()
window.update()

run = True
while run:
	try:
		nowText = textEntryToQR.get()
	except:
		run = False
		break
		
	if prevText != textEntryToQR.get() and len(textEntryToQR.get()) <= 2048:
		img, size = makeQR(textEntryToQR.get())
		qrImg.config(width = size[0], height = size[1])
		qrImg.create_image(0, 0, anchor = tk.NW, image = img)
		window.iconphoto(False, img)
		window.minsize(size[0], window.winfo_height())
		prevText = textEntryToQR.get()
	
	elif prevText != textEntryToQR.get() and len(textEntryToQR.get()) > 2048:
		tmp = textEntryToQR.get()[-1]
		textEntryToQR.delete(0)
		textEntryToQR.insert(0, tmp)
	
	window.update_idletasks()
	window.update()
