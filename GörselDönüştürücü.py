from tkinter import Tk, Label, Button, filedialog, StringVar, OptionMenu, messagebox, Frame
from PIL import Image
import os
import cairosvg

def convert_image(input_path, output_format):
    base, ext = os.path.splitext(input_path)
    output_path = base + '.' + output_format

    if output_format in ['jpg', 'jpeg', 'png', 'bmp', 'gif']:
        if ext.lower() == '.svg':
            # Convert SVG to PNG first
            temp_png_path = base + '.png'
            cairosvg.svg2png(url=input_path, write_to=temp_png_path)
            input_path = temp_png_path
        
        image = Image.open(input_path)
        image = image.convert("RGB")  # JPG ve BMP gibi formatlar için gerekli
        image.save(output_path)
        print(f"Görüntü olarak kaydedildi {output_path}")

    elif output_format == 'ico':
        if ext.lower() == '.svg':
            # Convert SVG to PNG first
            temp_png_path = base + '.png'
            cairosvg.svg2png(url=input_path, write_to=temp_png_path)
            input_path = temp_png_path
        
        image = Image.open(input_path)
        image.save(output_path, format='ICO')
        print(f"İkon olarak kaydedildi {output_path}")

    elif output_format == 'svg':
        if ext.lower() == '.svg':
            os.rename(input_path, output_path)
            print(f"SVG dosyası olarak kaydedildi {output_path}")
        else:
            cairosvg.svg2svg(url=input_path, write_to=output_path)
            print(f"Görüntü olarak kaydedildi {output_path}")

    else:
        print("Desteklenmeyen çıktı formatı!")

    return output_path

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.svg")])
    file_label.config(text=file_path)
    return file_path

def convert_and_save():
    input_path = file_label.cget("text")
    output_format = format_var.get()
    if input_path and output_format:
        output_path = convert_image(input_path, output_format)
        result_label.config(text=f"Görüntü olarak kaydedildi {output_path}")

        # Show message box
        if messagebox.askyesno("Dizini Aç", "Kaydedilen dizini açmak istiyor musunuz?"):
            open_directory(os.path.dirname(output_path))

def open_directory(directory):
    os.startfile(directory)

# Create the main window
root = Tk()
root.title("Resim Dönüştürücü")
root.geometry("400x200")
root.resizable(False, False)

# Create a frame for better layout management
frame = Frame(root, padx=10, pady=10)
frame.pack(fill="both", expand=True)

# Add a label to show the selected file path
file_label = Label(frame, text="Dosya seçilmedi", wraplength=300, anchor="w", justify="left")
file_label.grid(row=0, column=0, columnspan=3, pady=5)

# Add a button to select a file
select_button = Button(frame, text="Görsel Dosyasını Seçiniz", command=select_file)
select_button.grid(row=1, column=0, pady=5)

# Add a dropdown to select the output format
format_var = StringVar(frame)
format_var.set("jpg")  # default value
format_options = ["jpg", "png", "svg", "ico"]
format_menu = OptionMenu(frame, format_var, *format_options)
format_menu.grid(row=1, column=1, pady=5, padx=5)

# Add a button to convert and save the image
convert_button = Button(frame, text="Dönüştür ve Kaydet", command=convert_and_save)
convert_button.grid(row=1, column=2, pady=5)

# Add a label to show the result of the conversion
result_label = Label(frame, text="", wraplength=300, anchor="w", justify="left")
result_label.grid(row=2, column=0, columnspan=3, pady=5)

# Run the GUI event loop
root.mainloop()
