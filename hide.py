from tkinter import *
from tkinter import ttk
import tkinter.filedialog
from PIL import ImageTk
from PIL import Image
from tkinter import messagebox
from io import BytesIO
import os

class Hide:
    art = '''
    Data Hiding
     In Image
    '''
    art2 = ''
    output_image_size = 0

    def __init__(self, root):
        self.root = root

    def main(self):
        self.root.title('Image Steganography - Hide Data')
        self.root.geometry('500x600')
        self.root.resizable(False, False)
        f = Frame(self.root)
        title = Label(f, text='Image Steganography')
        title.config(font=('courier', 30))
        b_encode = Button(f, text='Encode', padx=14, command=lambda: self.frame1_encode(f))
        b_encode.config(font=('courier', 14))
        b_decode = Button(f, text='Decode', padx=14, command=lambda: self.frame1_decode(f))
        b_decode.config(font=('courier', 14))
        ascii_art = Label(f, text=self.art)
        ascii_art.config(font=('courier', 20))
        ascii_art2 = Label(f, text=self.art2)
        ascii_art2.config(font=('courier', 12, 'bold'))
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        f.grid()
        title.grid(row=1)
        b_encode.grid(row=2, pady=12)
        b_decode.grid(row=3, pady=12)
        ascii_art.grid(row=4, pady=10)
        ascii_art2.grid(row=5, pady=10)

    def home(self, frame):
        frame.destroy()
        self.main()

    def frame1_encode(self, f):
        f.destroy()
        f2 = Frame(self.root)
        label_art = Label(f2, text='ENCODE')
        label_art.config(font=('courier', 40))
        label_art.grid(row=1, pady=30)
        l1 = Label(f2, text='Select Image')
        l1.config(font=('courier', 20))
        l1.grid()
        bws_button = Button(f2, text='Select', font=('courier', 18), command=lambda: self.frame2_encode(f2))
        bws_button.grid()
        back_button = Button(f2, text='Back', command=lambda: self.home(f2))
        back_button.config(font=('courier', 18))
        back_button.grid(pady=15)
        f2.grid()

    def frame1_decode(self, f):
        f.destroy()
        d_f2 = Frame(self.root)
        label_art = Label(d_f2, text='DECODE')
        label_art.config(font=('courier', 40))
        label_art.grid(row=1, pady=30)
        l1 = Label(d_f2, text='Select Image')
        l1.config(font=('courier', 20))
        l1.grid()
        bws_button = Button(d_f2, text='Select', font=('courier', 18), command=lambda: self.frame2_decode(d_f2))
        bws_button.grid()
        back_button = Button(d_f2, text='Back', command=lambda: self.home(d_f2))
        back_button.config(font=('courier', 18))
        back_button.grid(pady=15)
        d_f2.grid()

    def frame2_decode(self, d_f2):
        d_f3 = Frame(self.root)
        myfile = tkinter.filedialog.askopenfilename(
            title="Select an image file",
            filetypes=[("Image files", ("*.png", "*.jpg", "*.jpeg", "*.bmp", "*.gif"))])
        if not myfile:
            messagebox.showerror("Error", "No file selected")
            d_f3.destroy()
            return
        myimg = Image.open(myfile, 'r')
        myimage = myimg.resize((300, 200))
        img = ImageTk.PhotoImage(myimage)
        l4 = Label(d_f3, text="Selected Image")
        l4.config(font=('courier', 20))
        l4.grid()
        panel = Label(d_f3, image=img)
        panel.image = img
        panel.grid()
        hidden_data = self.decode_image(myimg)
        l2 = Label(d_f3, text="Hidden Data")
        l2.config(font=('courier', 20))
        l2.grid(pady=10)
        text_area = Text(d_f3, height=10, width=50)
        text_area.insert(INSERT, hidden_data)
        text_area.grid()
        back_button = Button(d_f3, text='Cancel', command=lambda: self.home(d_f3))
        back_button.config(font=('courier', 18))
        back_button.grid(pady=15)
        show_info = Button(d_f3, text="More Info", command=self.info)
        show_info.config(font=('courier', 11))
        show_info.grid()
        d_f3.grid(row=1)
        d_f2.destroy()

    def decode_image(self, img):
        data = ''
        imgdata = iter(img.getdata())
        while True:
            try:
                pixels = [value for value in next(imgdata)[:3] +
                          next(imgdata)[:3] +
                          next(imgdata)[:3]]
            except StopIteration:
                break
            binstr = ''
            for i in pixels[:8]:
                if i % 2 == 0:
                    binstr += '0'
                else:
                    binstr += '1'
            data += chr(int(binstr, 2))
            if pixels[-1] % 2 != 0:
                break
        return data

    def info(self):
        try:
            info_str = f"Output Image Size: {self.output_image_size.st_size} bytes\n"
            info_str += f"Original Image Width: {self.o_image_w} pixels\n"
            info_str += f"Original Image Height: {self.o_image_h} pixels\n"
            messagebox.showinfo("Image Info", info_str)
        except AttributeError:
            messagebox.showerror("Error", "No image data available. Please encode an image first.")

    def genData(self, data):
        newd = []
        for i in data:
            newd.append(format(ord(i), '08b'))
        return newd

    def modPix(self, pix, data):
        datalist = self.genData(data)
        lendata = len(datalist)
        imdata = iter(pix)
        for i in range(lendata):
            pixels = [value for value in next(imdata)[:3] +
                      next(imdata)[:3] +
                      next(imdata)[:3]]
            for j in range(8):
                if datalist[i][j] == '0':
                    if pixels[j] % 2 != 0:
                        pixels[j] -= 1
                else:
                    if pixels[j] % 2 == 0:
                        pixels[j] -= 1
            if i == lendata - 1:
                if pixels[-1] % 2 == 0:
                    pixels[-1] -= 1
            else:
                if pixels[-1] % 2 != 0:
                    pixels[-1] -= 1
            pixels = tuple(pixels)
            yield pixels[0:3]
            yield pixels[3:6]
            yield pixels[6:9]

    def encode_enc(self, newim, data):
        w = newim.size[0]
        (x, y) = (0, 0)
        for pixel in self.modPix(newim.getdata(), data):
            newim.putpixel((x, y), pixel)
            if x == (w - 1):
                x = 0
                y += 1
            else:
                x += 1

    def enc_fun(self, text_area, myimg):
        data = text_area.get("1.0", "end-1c")
        if len(data) == 0:
            messagebox.showerror("Error", "No data to encode")
        else:
            newimg = myimg.copy()
            self.encode_enc(newimg, data)
            temp = os.path.splitext(os.path.basename(myimg.filename))[0]
            save_path = tkinter.filedialog.asksaveasfilename(initialfile=temp + "_encoded.png",
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"), ("BMP files", "*.bmp"), ("GIF files", "*.gif")])
            if save_path:
                newimg.save(save_path, format="PNG")
                messagebox.showinfo("Success", "Data encoded successfully")

    def frame2_encode(self, f2):
        ep = Frame(self.root)
        myfile = tkinter.filedialog.askopenfilename(
            title="Select an image file",
            filetypes=[("Image files", ("*.png", "*.jpg", "*.jpeg", "*.bmp", "*.gif"))])
        if not myfile:
            messagebox.showerror("Error", "No file selected")
            ep.destroy()
            return
        myimg = Image.open(myfile)
        myimage = myimg.resize((300, 200))
        img = ImageTk.PhotoImage(myimage)
        l3 = Label(ep, text="Selected Image")
        l3.config(font=('courier', 20))
        l3.grid()
        panel = Label(ep, image=img)
        panel.image = img
        panel.grid()
        self.output_image_size = os.stat(myfile)
        self.o_image_w, self.o_image_h = myimg.size
        l2 = Label(ep, text='Enter the message')
        l2.config(font=('courier', 20))
        l2.grid(pady=10)
        text_area = Text(ep, height=10, width=50)
        text_area.grid()
        encode_button = Button(ep, text='Cancel', command=lambda: self.home(ep))
        encode_button.config(font=('courier', 11))
        encode_button.grid()
        back_button = Button(ep, text='Encode', command=lambda: [self.enc_fun(text_area, myimg), self.home(ep)])
        back_button.config(font=('courier', 11))
        back_button.grid(pady=15)
        ep.grid(row=1)
        f2.destroy()

if __name__ == "__main__":
    root = Tk()
    app = Hide(root)
    app.main()
    root.mainloop()


