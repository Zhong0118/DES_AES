import os
import tkinter as tk
from tkinter import font, scrolledtext, messagebox, filedialog
from DES_AES_lib import des_encrypt, des_decrypt, aes_encrypt, aes_decrypt
import DES
import AES
from time_compare import *

# create main window
window = tk.Tk()
window.title("Time Comparison")

window_width = 1200
window_height = 800
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2)
window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

# set background
window.configure(bg="#f0f0f0")
title_font1 = font.Font(family="STENCIL", size=20, weight="bold")
title_font2 = font.Font(family="Consolas", size=16, weight="bold")
text_font = font.Font(family="Helvetica", size=12)
input_font = font.Font(family="Consolas", size=12)

# the title description
title_label1 = tk.Label(
    window, text="Welcome to compare performance", font=title_font1, bg="#f0f0f0", fg="#111"
)
title_label2 = tk.Label(
    window,
    text="You can choose custom DES or AES and library DES or AES",
    font=title_font2,
    bg="#f0f0f0",
    fg="#444",
)
title_label1.pack(pady=1)
title_label2.pack(pady=1)


mode_frame = tk.Frame(window, bg="#f0f0f0")
mode_frame.pack(pady=5)

file_mode_var = tk.BooleanVar()

def toggle_input_mode():
    if file_mode_var.get():
        plaintext_text.config(state=tk.DISABLED)
        file_button.config(state=tk.NORMAL)
    else:
        plaintext_text.config(state=tk.NORMAL)
        file_button.config(state=tk.DISABLED)
        file_label.config(text="No file selected")

tk.Checkbutton(
    mode_frame, 
    text="File Mode", 
    variable=file_mode_var, 
    command=toggle_input_mode,
    bg="#f0f0f0", 
    font=text_font
).pack(side=tk.LEFT, padx=10)

file_button = tk.Button(
    mode_frame,
    text="Choose File",
    command=lambda: select_file(),
    font=text_font,
    state=tk.DISABLED
)
file_button.pack(side=tk.LEFT, padx=10)

file_label = tk.Label(
    mode_frame,
    text="No file selected",
    font=text_font,
    bg="#f0f0f0"
)
file_label.pack(side=tk.LEFT, padx=10)

current_file = None

def select_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        global current_file
        current_file = file_path
        file_label.config(text=f"Selected file: {file_path}")




# 添加输入框
plaintext_label = tk.Label(window, text="Plaintext", font=title_font2, bg="#f0f0f0")
plaintext_label.pack(pady=5)
plaintext_text = scrolledtext.ScrolledText(window, width=120, height=10, font=input_font)
plaintext_text.pack(pady=5)

key_label = tk.Label(window, text="Key", font=title_font2, bg="#f0f0f0")
key_label.pack(pady=5)
key_entry = scrolledtext.ScrolledText(window, width=50, height=1, font=input_font)
key_entry.pack(pady=5)

# 添加复选框
checkboxes_frame = tk.Frame(window, bg="#f0f0f0")
checkboxes_frame.pack(pady=10)

des_custom_var = tk.BooleanVar()
aes_custom_var = tk.BooleanVar()
des_lib_var = tk.BooleanVar()
aes_lib_var = tk.BooleanVar()

tk.Checkbutton(checkboxes_frame, text="DES Custom", variable=des_custom_var, bg="#f0f0f0", font=text_font).pack(side=tk.LEFT, padx=20)
tk.Checkbutton(checkboxes_frame, text="AES Custom", variable=aes_custom_var, bg="#f0f0f0", font=text_font).pack(side=tk.LEFT, padx=20)
tk.Checkbutton(checkboxes_frame, text="DES Lib", variable=des_lib_var, bg="#f0f0f0", font=text_font).pack(side=tk.LEFT, padx=20)
tk.Checkbutton(checkboxes_frame, text="AES Lib", variable=aes_lib_var, bg="#f0f0f0", font=text_font).pack(side=tk.LEFT, padx=20)

# 添加结果表格
result_frame = tk.Frame(window)
result_frame.pack(pady=20)

headers = ["", "DES Custom", "AES Custom", "DES Lib", "AES Lib"]
results = {}

for j, header in enumerate(headers):
    tk.Label(result_frame, text=header, font=text_font, relief="groove", width=15).grid(row=0, column=j)
    results[""] = tk.Label(result_frame, text="Time(s)", font=text_font, relief="groove", width=15)
    results[""].grid(row=1, column=j)
    if j > 0:
        results[header] = tk.Label(result_frame, text="", font=text_font, relief="groove", width=15)
        results[header].grid(row=1, column=j)

# 加密按钮处理函数
def encrypt():
    print("===============================================")
    key = key_entry.get("1.0", tk.END).strip()
    if file_mode_var.get():
        if not current_file:
            messagebox.showerror("Error", "Please select a file")
            return
        # 尝试不同的编码方式读取文件
        encodings = ['utf-8', 'gbk', 'gb2312', 'iso-8859-1', 'ascii']
        plaintext = None
        for encoding in encodings:
            try:
                with open(current_file, 'r', encoding=encoding) as f:
                    plaintext = f.read()
                break  # 如果成功读取，跳出循环
            except UnicodeDecodeError:
                continue
        if plaintext is None:
            messagebox.showerror("Error", "Failed to read file with any supported encoding")
            return
    else:
        plaintext = plaintext_text.get("1.0", tk.END).strip()
    if not plaintext or not key:
        messagebox.showerror("Error", "Please input plaintext/file and key")
        return
    # 清空之前的结果
    for label in results.values():
        label.config(text="")
    
    # 根据选择执行相应的加密并计时
    if des_custom_var.get():
        _, time_result = get_time_cost(DES.encrypt, plaintext, key)
        print("DES Custom: " + str(time_result))
        results["DES Custom"].config(text=f"{time_result:.6f}")
        
    if aes_custom_var.get():
        _, time_result = get_time_cost(AES.AES_encrypt, plaintext, key)
        print("AES Custom: " + str(time_result))
        results["AES Custom"].config(text=f"{time_result:.6f}")
        
    if des_lib_var.get():
        _, time_result = get_time_cost(des_encrypt, plaintext, key)
        print("DES Lib: " + str(time_result))
        results["DES Lib"].config(text=f"{time_result:.6f}")
        
    if aes_lib_var.get():
        _, time_result = get_time_cost(aes_encrypt, plaintext, key)
        print("AES Lib: " + str(time_result))
        results["AES Lib"].config(text=f"{time_result:.6f}")

# 添加加密按钮
encrypt_button = tk.Button(window, text="Encrypt→", command=encrypt, font=text_font, width=20, bg="#4CAF50", fg="white", activebackground="#45a049")
encrypt_button.pack(pady=10)

window.mainloop()