import re
import hashlib
import os
from cryptography.fernet import Fernet
import tkinter as tk
import smtplib
import random
import string
from tkinter import *
from PIL import Image, ImageTk
import openai
import subprocess
# Generate a new encryption key
key =b'_0OA1eOQ0gI8bHs-JB3YNrW3im8x90MQAmKVa_09aSw='
openai.api_key = "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" 
# Create a Fernet object with the encryption key
fernet = Fernet(key)
# Create an empty dictionary to hold user credentials
users = {}
canvas = None
current_canvas = None

button_clicked = False

def play_gif(gif_path, window):
    global current_canvas
    
    # Destroy the previous canvas if it exists
    if current_canvas is not None:
        current_canvas.destroy()
        
    # Load the GIF file and get the dimensions of the GIF frames
    gif = Image.open(gif_path)
    width, height = gif.size
    
    # Create a canvas to display the GIF frames
    canvas = tk.Canvas(window, width=width, height=height)
    canvas.pack()
    
    # Convert each GIF frame to a Tkinter-compatible format
    gif_frames = []
    for frame in range(gif.n_frames):
        gif.seek(frame)
        gif_frames.append(ImageTk.PhotoImage(gif.copy()))

    # Define a function to update the canvas with the next GIF frame
    def update_canvas(frame=0):
        if canvas.winfo_exists():
            canvas.delete("all")
            canvas.create_rectangle(0, 0, width, height, fill="white")  # Fill the canvas with a solid color
            canvas.create_image(0, 0, image=gif_frames[frame], anchor=tk.NW)
            frame += 1
            if frame >= len(gif_frames):
                frame = 0
            delay = gif.info.get("duration", 20)  # Get the delay between frames specified in the GIF file
            window.after(delay, update_canvas, frame)

    # Start the frame update loop
    update_canvas()

    # Update the current canvas
    current_canvas = canvas

    return canvas

def generate_verification_code():
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return code

def email():

    smtp_server_str =('smtp.gmail.com',587)
    s = smtplib.SMTP(*smtp_server_str)
    s.starttls()
    s.login("anson1314qq@gmail.com","elcdhzdykqskodom")
    email_title = "Verification Code of AI LAB Account"
    name = username_entry.get()
    receiver = email_entry.get()
    # Check if the email address is valid
    if not re.match(r"[^@]+@[^@]+\.[^@]+", receiver):
        error_label.config(text="Invalid email address. Try again.", fg="red")
        return
    email_content = "Hi " +  name + ",here is your verification code:" + verification_code
    send_data =f"Subject:{email_title}\n\n{email_content}"
    s.sendmail("anson1314qq@gmail.com",receiver,send_data)
                
def sign_up():
    # Remove the sign up and login buttons from the window
    if signup_button.winfo_exists():
        signup_button.place_forget()
    if signup_button.winfo_exists():
        login_button.place_forget()

    # Add the labels and entry widgets for the username, email, and password
    username_label.place(x=650, y=280)
    username_entry.place(x=880, y=290)

    email_label.place(x=650, y=380)
    email_entry.place(x=880, y=390)

    password_label.place(x=650, y=480)
    password_entry.place(x=880, y=490)

    verif_label.place(x=650, y=580)
    verif_entry.place(x=880, y=590)

    # Add the  buttons to the window
    verif_button.place(x=650,y =670)             
    signupfinish_button.place(x=1000,y=670)
    
def login():
    global hashed_password, users
    if signup_button.winfo_exists():
        signup_button.place_forget()
    if signup_button.winfo_exists():
        login_button.place_forget()
    # Add the labels and entry widgets for the username and password
    username_label.place(x=650, y=380)
    username_entry.place(x=880, y=390)
    password_label.place(x=650, y=530)
    password_entry.place(x=880, y=540)
    # Add the finish button to the window
    loginfinish_button.place(x=830,y=670)

def signupfinish():
    global hashed_password, users,ver_code
    fernet = Fernet(key)
    error_label.place(x=750, y=630)
    # Get the values of the username, email, password, and verification code entry widgets
    with open("info.txt", "r") as f:
        lines = f.readlines()
    # Create an empty dictionary to hold user credentials
    users = {}
    username = username_entry.get()
    useremail = email_entry.get()
    userpassword = password_entry.get()
    verif_code = verif_entry.get()
    email = ""
    for line in lines:
        name, email, password = line.strip().split(",")
        users[name] = {"email": email, "password": password}
    # Check if the username is already take
    if username in users:
        error_label.config(text="Username already taken. Try another one.", fg="red")
        return

    # Check if the email address is valid
    if not re.match(r"[^@]+@[^@]+\.[^@]+", useremail):
        error_label.config(text="Invalid email address. Try again.", fg="red")
        return

    # Check if the password meets the requirements
    if len(userpassword) < 8 or not re.search("[a-z]", userpassword) or not re.search("[A-Z]", userpassword) or not re.search("[0-9]", userpassword):
        error_label.place(x=250, y=630)
        error_label.config(text="Password must be at least 8 characters longwith at least one lowercase letter, one uppercase letter, and one number.", fg="red")
        return
    # Check if verification code is valid
    if verif_code != ver_code:
        error_label.config(text="Invalid verification code. Try again.", fg="red")
        return
    # Encrypt the hashed password using Fernet
    userpassword = userpassword.encode()
    encrypted_password = fernet.encrypt(userpassword)
    print(encrypted_password.decode())
    
    # Add the username, email, and encrypted password to the users dictionary
    users[username] = {"email": email, "password": encrypted_password.decode()}
    
    # Save the user information in a file
    with open("info.txt", "a") as file:
        file.write(f"{username},{useremail},{encrypted_password.decode()}\n")

    error_label.config(text="Sign up successful!", fg="green")
    
    verification_code = generate_verification_code()
    # Clear the input fields after sign up
    username_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    verif_entry.delete(0, tk.END)

    # Remove the username, email, password, and verification code fields from the window
    username_label.place_forget()
    username_entry.place_forget()
    email_label.place_forget()
    email_entry.place_forget()
    password_label.place_forget()
    password_entry.place_forget()
    verif_label.place_forget()
    verif_entry.place_forget()
    signupfinish_button.place_forget()
    verif_button.place_forget()
    ver_code = verification_code
    signup_button.place(x=650,y =670)
    login_button.place(x=1000, y=670)

def loginfinish(chatstate,idname,idemail,maskstate,idpassword):
    # Get the values of the username and password entry widgets
    username = username_entry.get()
    userpassword = password_entry.get()
    fernet = Fernet(key)
    with open("suspend.txt", "r") as f:
        lines = f.readlines()
    users = {}
    for line in lines:
        name, email, password = line.strip().split(",")
        users[name] = {"email": email, "password": password}
    # Check if the username is already take
    if username in users:
        error_label.config(text="Account is suspended.Please contact teacher.", fg="red")
        return
    username = username_entry.get()
    userpassword = password_entry.get()
    fernet = Fernet(key)
    # Get the values of the username, email, password, and verification code entry widgets
    with open("info.txt", "r") as f:
        lines = f.readlines()
    # Create an empty dictionary to hold user credentials
    users = {}
    for line in lines:
        name, email, password = line.strip().split(",")
        users[name] = {"email": email, "password": password}

    # Check if the username is already take
    if not (username in users):
        error_label.config(text="Invaild Username. Try again.", fg="red")
        return
    decrypted_data = fernet.decrypt(password)
    if userpassword != decrypted_data.decode():
        error_label.config(text="Invaild Password. Try again.", fg="red")
        return
    idname = username
    idemail = email
    idpassword = userpassword
    # Clear the input fields after login
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

    # Remove the username and password fields from the window
    username_label.place_forget()
    username_entry.place_forget()
    password_label.place_forget()
    password_entry.place_forget()
    
    loginfinish_button.place_forget()
    play_gif("menubg.gif", window)
    chat_button = tk.Button(window, image=cpng_photo,command =lambda:chat(chatstate,idname,idemail,maskstate,idpassword), highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    mask_button = tk.Button(window, image=mpng_photo,command =mask,highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    back_button = tk.Button(window, image=bpng_photo,command=lambda: inbackend(chatstate,idname,idemail,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    idcard_button = tk.Button(window, image=upng_photo, command=lambda:idcard(chatstate,idname,idemail,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    idname_label = tk.Label(window, font=("Times New Roman", 45),bg="#CDFFF5")
    chat_button.place(x=550,y=320)
    mask_button.place(x=550,y=460)
    back_button.place(x=550,y=620)
    idcard_button.place(x=1,y=1)
    idname_label.place(x=200,y=77)
    idname_label.config(text=idname)
def inbackend(chatstate,idname,idemail,maskstate,idpassword):
    global teacher_label,teacher_entry,backloginfinish_button,backpassword_label,backpassword_entry,teacher,backpassword,exit_button
    chat_button.place_forget()
    mask_button.place_forget()
    back_button.place_forget()
    play_gif("backendbg.gif", window)
    teacher_label = tk.Label(window, image=tpng_photo, highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    teacher_entry = tk.Entry(window, font=("Century Gothic", 20))
    backpassword_label = tk.Label(window,image=ppng_photo, highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    backpassword_entry = tk.Entry(window, show="*", font=("Century Gothic", 20))
    backloginfinish_button = tk.Button(window, image=fpng_photo,command=lambda: backloginfinish(chatstate,idname,idemail,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    exit_button = tk.Button(window, image=expng_photo, command=lambda:ex(chatstate,idname,idemail,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    exit_button.place(x=1650,y=900)
    teacher_label.place(x=650, y=380)
    teacher_entry.place(x=880, y=390)
    backpassword_label.place(x=650, y=530)
    backpassword_entry.place(x=880, y=540)
    backloginfinish_button.place(x=830,y=670)
    teacher = teacher_entry.get()
    backpassword = backpassword_entry.get()
    window.title("Backend")
def backloginfinish(chatstate,idname,idemail,maskstate,idpassword):
    global teacher_label,teacher_entry,backloginfinish_button,backpassword_label,backpassword_entry,teacher,backpassword,error_label,chan_pw_button,suspend_button ,remove_button,endismask_button,endischat_button,exit_button
    error_label = tk.Label(window, font=("Helvetica", 20),bg="black", fg="white")
    teacher = teacher_entry.get()
    backpassword = backpassword_entry.get()
    error_label.place(x=750, y=630)
    if teacher != "kwoksir":
        error_label.config(text="Teacher not found. Try again.", fg="red")
        return
    if backpassword != "123456Hk":
        error_label.config(text="Invalid password. Try again.", fg="red")
        return
    
    teacher_entry.delete(0, tk.END)
    backpassword_entry.delete(0, tk.END)
    teacher_label.place_forget()
    teacher_entry.place_forget()
    backpassword_label.place_forget()
    backpassword_entry.place_forget()
    backloginfinish_button.place_forget()
    error_label.place_forget()
    play_gif("backinbg.gif", window)
    suspend_button = tk.Button(window, image=bbpng_photo, command=lambda:suspend(chatstate,idname,idemail,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    remove_button = tk.Button(window, image=bbpng_photo, command=lambda:remove(chatstate,idname,idemail,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    endismaskon_button = tk.Button(window, image=onpng_photo, command=lambda: endisable_mask(chatstate,idname,idemail,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    endismaskoff_button = tk.Button(window, image=offpng_photo, command=lambda: endisable_mask(chatstate,idname,idemail,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    endischaton_button = tk.Button(window, image=onpng_photo, command=lambda: endisable_chat(chatstate,idname,idemail,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    endischatoff_button = tk.Button(window, image=offpng_photo, command=lambda: endisable_chat(chatstate,idname,idemail,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    exit_button = tk.Button(window, image=expng_photo, command=lambda:ex(chatstate,idname,idemail,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    suspend_button.place(x=1000,y=430)
    remove_button.place(x=1000,y=570)
    exit_button.place(x=1650,y=900)
    if chatstate == 0:
        endischaton_button.place(x=542,y=425)
    if  chatstate == 1:
        endischatoff_button.place(x=542,y=430)
    if maskstate == 0:
        endismaskon_button.place(x=542,y=570)
    if  maskstate == 1:
        endismaskoff_button.place(x=542,y=570)
def backbutton(chatstate,idname,idemail,maskstate,idpassword):
    suspend_button = tk.Button(window, image=bbpng_photo, command=lambda:suspend(chatstate,idname,idemail,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    remove_button = tk.Button(window, image=bbpng_photo, command=lambda:remove(chatstate,idname,idemail,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    endischaton_button = tk.Button(window, image=onpng_photo, command=lambda: endisable_chat(chatstate,idname,idemail,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    endischatoff_button = tk.Button(window, image=offpng_photo, command=lambda: endisable_chat(chatstate,idname,idemail,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    endismaskon_button = tk.Button(window, image=onpng_photo, command=lambda: endisable_mask(chatstate,idname,idemail,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    endismaskoff_button = tk.Button(window, image=offpng_photo, command=lambda: endisable_mask(chatstate,idname,idemail,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    exit_button = tk.Button(window, image=expng_photo, command=lambda:ex(chatstate,idname,idemail,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    suspend_button.place(x=1000,y=425)
    remove_button.place(x=1000,y=570)
    exit_button.place(x=1650,y=900)

def chat(chatstate,idname,idemail,maskstate,idpassword):
    global chat_entry,chat_label
    widgets = window.winfo_children()
    # Loop through all the widgets and destroy them if they are not the background video
    for widget in widgets:
        if not isinstance(widget, tk.Canvas):
            widget.destroy()
    play_gif("chatbg.gif", window)
    exit_button = tk.Button(window, image=expng_photo, command=lambda:ex(chatstate,idname,idemail,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    exit_button.place(x=1650,y=900)
    chat_entry = tk.Text(window, font=("Century Gothic", 20), width=25, height=4)
    chat_entry.place(x=953, y=605)
    chat_label = tk.Label(window, font=("Arial", 20),bg="white", fg="black",width=24)
    chat_label.place(x=535, y=305)
    chat_label.config(text="Hi, I'm Pepper. I'm a helpful assistant.What can I help you today?",wraplength=400)
    inchat_button = tk.Button(window, image=ccpng_photo, command=lambda:inchat(chatstate,idname,idemail,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    inchat_button.place(x=830,y=836)
    window.title("Chatbot")
def inchat(chatstate,idname,idemail,maskstate,idpassword):
    global chat_entry,chat_label,message
    chat_label.place_forget()
    nchat_label = tk.Label(window, font=("Arial", 17),bg="white", fg="black",width=30)
    messages = [
        # system message to set the behavior of the assistant
        {"role": "system", "content": "You are a helpful assistant called Pepper! Please reply within 1 sentence"},
    ]

    try:
        chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        reply = chat_completion["choices"][0]["message"]["content"]
        messages.append({"role": "assistant", "content": reply})
    except:
        print("Check if you have set the API key correctly")
        return
    a = chat_entry.get("1.0", tk.END)
    message = a
    if message == "clear":
        print("\033[H\033[J")
        print("ChatGPT: Hi, I'm ChatGPT. I'm a helpful assistant")
        messages = [
            {"role": "system", "content": "Hi ChatGPT, You are a helpful assistant!"},
        ]
        chat_completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
        reply = chat_completion["choices"][0]["message"]["content"]
        messages.append({"role": "assistant", "content": reply})
    if message:
        messages.append(
            {"role": "user", "content": message},
        )
        chat_completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )

    reply = chat_completion["choices"][0]["message"]["content"]
    nchat_label.place(x=535, y=306)
    nchat_label.config(text=(f"{reply}"),wraplength=400)
    messages.append({"role": "assistant", "content": reply})
    chat_entry.delete(0, tk.END)
def ex(chatstate,idname,idemail,maskstate,idpassword):
    global chat_button,mask_button,back_button
    # Get a list of all widgets in the window
    widgets = window.winfo_children()
    # Loop through all the widgets and destroy them if they are not the background video
    for widget in widgets:
        if not isinstance(widget, tk.Canvas):
            widget.destroy()
    play_gif("menubg.gif", window)
    mask_button = tk.Button(window, image=mpng_photo,command =mask,highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    back_button = tk.Button(window, image=bpng_photo,command=lambda: inbackend(chatstate,idname,idemail,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    chat_button = tk.Button(window, image=cpng_photo, command =lambda: chat(chatstate,idname,idemail,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    idcard_button = tk.Button(window, image=upng_photo, command=lambda:idcard(chatstate,idname,idemail,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    idname_label = tk.Label(window, font=("Times New Roman", 45),bg="#CDFFF5")
    chat_button.place(x=550,y=320)
    mask_button.place(x=550,y=460)
    back_button.place(x=550,y=620)
    idcard_button.place(x=1,y=1)
    idname_label.place(x=200,y=77)
    idname_label.config(text=idname)
    if chatstate == 0:
        chat_button.config(state="normal")
    elif  chatstate == 1:
        chat_button.config(state="disabled")
    if maskstate == 0:
        mask_button.config(state="normal")
    elif  maskstate == 1:
        mask_button.config(state="disabled")
def endisable_chat(chatstate,idname,idemail,maskstate,idpassword):
    # Get a list of all widgets in the window
    widgets = window.winfo_children()
    # Loop through all the widgets and destroy them if they are not the background video
    for widget in widgets:
        if not isinstance(widget, tk.Canvas):
            widget.destroy()
    endischaton_button = tk.Button(window, image=onpng_photo, command=lambda: endisable_chat(chatstate,idname,idemail,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    endischatoff_button = tk.Button(window, image=offpng_photo, command=lambda: endisable_chat(chatstate,idname,idemail,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    endismaskon_button = tk.Button(window, image=onpng_photo, command=lambda: endisable_mask(chatstate,idname,idemail,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    endismaskoff_button = tk.Button(window, image=offpng_photo, command=lambda: endisable_mask(chatstate,idname,idemail,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    if chatstate == 0:
        chatstate = 1
        endischatoff_button.place(x=542,y=430)
    elif  chatstate == 1:
        chatstate = 0
        endischaton_button.place(x=542,y=430)
    if maskstate == 0:
        endismaskon_button.place(x=542,y=570)
    if  maskstate == 1:
        endismaskoff_button.place(x=542,y=570)
    backbutton(chatstate,idname,idemail,maskstate,idpassword)

def endisable_mask(chatstate,idname,idemail,maskstate,idpassword):
    # Get a list of all widgets in the window
    widgets = window.winfo_children()
    # Loop through all the widgets and destroy them if they are not the background video
    for widget in widgets:
        if not isinstance(widget, tk.Canvas):
            widget.destroy()
    endischaton_button = tk.Button(window, image=onpng_photo, command=lambda: endisable_chat(chatstate,idname,idemail,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    endischatoff_button = tk.Button(window, image=offpng_photo, command=lambda: endisable_chat(chatstate,idname,idemail,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    endismaskon_button = tk.Button(window, image=onpng_photo, command=lambda: endisable_mask(chatstate,idname,idemail,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    endismaskoff_button = tk.Button(window, image=offpng_photo, command=lambda: endisable_mask(chatstate,idname,idemail,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    if maskstate == 0:
        maskstate = 1
        endismaskoff_button.place(x=542,y=570)
    elif  maskstate == 1:
        maskstate = 0
        endismaskon_button.place(x=542,y=570)
    if chatstate == 0:
        endischaton_button.place(x=542,y=430)
    if  chatstate == 1:
        endischatoff_button.place(x=542,y=430)
    backbutton(chatstate,idname,idemail,maskstate,idpassword)
def suspend(chatstate,idname,idemail,maskstate,idpassword):
    # Get a list of all widgets in the window
    widgets = window.winfo_children()
    # Loop through all the widgets and destroy them if they are not the background video
    for widget in widgets:
        if not isinstance(widget, tk.Canvas):
            widget.destroy()
    play_gif("acbg.gif", window)
    exit_button = tk.Button(window, image=expng_photo, command=lambda:ex(chatstate,idname,idemail,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    username_label = tk.Label(window, image=npng_photo, highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    username_entry = tk.Entry(window, font=("Century Gothic", 20))
    sus_button = tk.Button(window, image=supng_photo, command=lambda:sus(chatstate,idname,idemail,username_entry,error_label,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    sus_button.place(x=640,y=670)
    gobackend_button = tk.Button(window, image=gopng_photo, command=lambda:gobackend(chatstate,idname,idemail,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    gobackend_button.place(x=830,y=845)
    resus_button = tk.Button(window, image=rspng_photo, command=lambda:resus(chatstate,idname,idemail,username_entry,error_label,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    resus_button.place(x=1030,y=670)
    username_label.place(x=650, y=530)
    username_entry.place(x=880, y=540)
    exit_button.place(x=1650,y=900)
    error_label = tk.Label(window, font=("Helvetica", 20),bg="black", fg="white")
    error_label.place(x=750, y=630)
def sus(chatstate,idname,idemail,username_entry,error_label,maskstate,idpassword):
    fernet = Fernet(key)
    with open("info.txt", "r") as f:
        lines = f.readlines()
    # Create an empty dictionary to hold user credentials
    users = {}
    username = username_entry.get()
    email = ""
    if username == idname :
        error_label.config(text="Can't suspend current account.Try again.", fg="red")
        return           
    for line in lines:
        name, email, password = line.strip().split(",")
        users[name] = {"email": email, "password": password}
    # Check if the username is already take
    if not (username in users):
        error_label.config(text="Invaild username.Try again.", fg="red")
        return   
    with open("suspend.txt", "r") as f:
        lines = f.readlines()
    users = {}
    email = ""
    for line in lines:
        name, email, password = line.strip().split(",")
        users[name] = {"email": email, "password": password}
    if  username in users:
        error_label.config(text="Username is suspended.Try again.", fg="red")
        return 
    else:    
        with open("suspend.txt", "a") as file:
            file.write(f"{username},{email},{password}\n")
            error_label.config(text="The suspension is successful", fg="green")
    username_entry.delete(0, tk.END)


    
def resus(chatstate,idname,idemail,username_entry,error_label,maskstate,idpassword):
    fernet = Fernet(key)
    with open("suspend.txt", "r") as f:
        lines = f.readlines()
    users = {}
    username = username_entry.get()
    email = idemail
    for line in lines:
        name, email, password = line.strip().split(",")
        users[name] = {"email": email, "password": password}
    
    if not (username in users):
        error_label.config(text="Invaild username.Try again.", fg="red")
        return   
    else:
        updated_lines = [line for line in lines if not line.startswith(username + ",")]
        with open("suspend.txt", "w") as file:
            file.writelines(updated_lines)
            error_label.config(text="The resuspension is successful", fg="green")
    username_entry.delete(0, tk.END)                 

def remove(chatstate,idname,idemail,maskstate,idpassword):
    # Get a list of all widgets in the window
    widgets = window.winfo_children()
    # Loop through all the widgets and destroy them if they are not the background video
    for widget in widgets:
        if not isinstance(widget, tk.Canvas):
            widget.destroy()
    play_gif("acbg.gif", window)
    gobackend_button = tk.Button(window, image=gopng_photo, command=lambda:gobackend(chatstate,idname,idemail,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    gobackend_button.place(x=830,y=845)
    exit_button = tk.Button(window, image=expng_photo, command=lambda:ex(chatstate,idname,idemail,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    username_label = tk.Label(window, image=npng_photo, highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    username_entry = tk.Entry(window, font=("Century Gothic", 20))
    remo_button = tk.Button(window, image=repng_photo, command=lambda:remo(chatstate,idname,idemail,username_entry,error_label,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    remo_button.place(x=830,y=670)
    username_label.place(x=650, y=530)
    username_entry.place(x=880, y=540)
    exit_button.place(x=1650,y=900)
    error_label = tk.Label(window, font=("Helvetica", 20),bg="black", fg="white")
    error_label.place(x=750, y=630)
            
def remo(chatstate,idname,idemail,username_entry,error_label,maskstate,idpassword):
    fernet = Fernet(key)
    username = username_entry.get()
    if username == idname :
        error_label.config(text="Can't suspend current account.Try again.", fg="red")
        return       
    with open("info.txt", "r") as f:
        lines = f.readlines()
    users = {}
    username = username_entry.get()
    email = ""
    for line in lines:
        name, email, password = line.strip().split(",")
        users[name] = {"email": email, "password": password}
    
    if not (username in users):
        error_label.config(text="Invaild Username.Try again.", fg="red")
        return   
    else:
        updated_lines = [line for line in lines if not line.startswith(username + ",")]
        with open("info.txt", "w") as file:
            file.writelines(updated_lines)
            error_label.config(text="The removal is successful", fg="green")
    with open("suspend.txt", "r") as f:
        lines = f.readlines()
    users = {}
    username = username_entry.get()
    email = ""
    for line in lines:
        name, email, password = line.strip().split(",")
        users[name] = {"email": email, "password": password}
    
    if username in users:
        updated_lines = [line for line in lines if not line.startswith(username + ",")]
        with open("suspend.txt", "w") as file:
            file.writelines(updated_lines)
    username_entry.delete(0, tk.END)                 
    
def gobackend(chatstate,idname,idemail,maskstate,idpassword):
    # Get a list of all widgets in the window
    widgets = window.winfo_children()
    # Loop through all the widgets and destroy them if they are not the background video
    for widget in widgets:
        if not isinstance(widget, tk.Canvas):
            widget.destroy()
    play_gif("backinbg.gif", window)
    suspend_button = tk.Button(window, image=bbpng_photo, command=lambda:suspend(chatstate,idname,idemail,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    remove_button = tk.Button(window, image=bbpng_photo, command=lambda:remove(chatstate,idname,idemail,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    endismaskon_button = tk.Button(window, image=onpng_photo, command=lambda: endisable_mask(chatstate,idname,idemail,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    endismaskoff_button = tk.Button(window, image=offpng_photo, command=lambda: endisable_mask(chatstate,idname,idemail,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    endischaton_button = tk.Button(window, image=onpng_photo, command=lambda: endisable_chat(chatstate,idname,idemail,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    endischatoff_button = tk.Button(window, image=offpng_photo, command=lambda: endisable_chat(chatstate,idname,idemail,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    exit_button = tk.Button(window, image=expng_photo, command=lambda:ex(chatstate,idname,idemail,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    suspend_button.place(x=1000,y=430)
    remove_button.place(x=1000,y=570)
    exit_button.place(x=1650,y=900)
    if chatstate == 0:
        endischaton_button.place(x=542,y=430)
    if  chatstate == 1:
        endischatoff_button.place(x=542,y=430)
    if maskstate == 0:
        endismaskon_button.place(x=542,y=570)
    if  maskstate == 1:
        endismaskoff_button.place(x=542,y=570)
def mask():
    chat_button.place_forget()
    mask_button.place_forget()
    back_button.place_forget()
    idcard_button.place_forget()
    play_gif("maskbg.gif", window)
    exit_button = tk.Button(window, image=expng_photo, command=lambda:ex(chatstate,idname,idemail,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    exit_button.place(x=1650,y=900)

def open_program(program_path):
    try:
        subprocess.Popen(program_path)
    except FileNotFoundError:
        print("Program not found.")

def close_program(program_name):
    try:
        subprocess.Popen(["taskkill", "/F", "/IM", program_name])
    except subprocess.CalledProcessError:
        print("Failed to close the program.")


def idcard(chatstate,idname,idemail,maskstate,idpassword):
    # Get a list of all widgets in the window
    widgets = window.winfo_children()
    # Loop through all the widgets and destroy them if they are not the background video
    for widget in widgets:
        if not isinstance(widget, tk.Canvas):
            widget.destroy()
    play_gif("idcard.gif", window)
    exit_button = tk.Button(window, image=expng_photo, command=lambda: ex(chatstate,idname,idemail,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    exit_button.place(x=1650,y=900)
    username_label = tk.Label(window, image=npng_photo, highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)    
    password_label = tk.Label(window,image=ppng_photo, highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    email_label = tk.Label(window, image=epng_photo, highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    password_entry = tk.Entry(window, font=("Century Gothic", 30) ,width=10)
    idname_label = tk.Label(window, font=("Century Gothic", 30),bg="white")
    idmail_label = tk.Label(window, font=("Helvetica", 15),bg="white")
    username_label.place(x=550, y=450)
    idname_label.place(x=800, y=445)
    email_label.place(x=550, y=550)
    idmail_label.place(x=790, y=560)
    password_label.place(x=550, y=650)
    password_entry.insert(0, idpassword)
    password_entry.place(x=800, y=650)
    idname_label.config(text=idname)
    idmail_label.config(text=idemail)
    error_label = tk.Label(window, font=("Helvetica", 20),bg="white")
    chpw_button = tk.Button(window, image=chpwpng_photo, command=lambda: chpw(chatstate,idname,idemail,maskstate,idpassword,password_entry,error_label),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
    chpw_button.place(x=830,y=845)
    error_label.place(x=550, y=730)
def chpw(chatstate,idname,idemail,maskstate,idpassword,password_entry,error_label):
    fernet = Fernet(key)
    error_label.place_forget()
    userpassword = password_entry.get()
    if len(userpassword) < 8 or not re.search("[a-z]", userpassword) or not re.search("[A-Z]", userpassword) or not re.search("[0-9]", userpassword):
        error_label.place(x=550, y=730)
        error_label.config(text="Password must be at least 8 characters longwith\nat least one lowercase letter, one uppercase letter, and one number.", fg="red")
        return
    with open("info.txt", "r") as f:
        lines = f.readlines()
    # Create an empty dictionary to hold user credentials
    users = {}
    username = idname
    email = ""
    useremail = idemail
    for line in lines:
        name, email, password = line.strip().split(",")
        users[name] = {"email": email, "password": password}
    userpassword = userpassword.encode()
    encrypted_password = fernet.encrypt(userpassword)    
    users[username] = {"email": email, "password": encrypted_password.decode()}
    if username in users:
        updated_lines = [line for line in lines if not line.startswith(username + ",")]
        with open("info.txt", "w") as file:
            file.writelines(updated_lines)
    with open("info.txt", "a") as file:
        file.write(f"{username},{useremail},{encrypted_password.decode()}\n")
    error_label = tk.Label(window, font=("Helvetica", 35),bg="white")
    error_label.place(x=720, y=742)
    error_label.config(text="Changed successful!", fg="green")
        
    
def run_python_file(file_path):
    try:
        subprocess.run(["python", file_path], check=True, encoding='utf-8')
    except subprocess.CalledProcessError as e:
        print(f"Error running {file_path}: {e}")
    
    
# Create a Tkinter window
window = tk.Tk()



# Set the size of the window
window.geometry("1980x1080")

# Set the title of the window
window.title("Login System")

# Play a video in the background of the window
play_gif("loginbg.gif", window)

# Load the PNG image
spng = Image.open("signbut.png")
# Convert the PNG image to a Tkinter-compatible format
spng_photo = ImageTk.PhotoImage(spng)
# Load the PNG image
lpng = Image.open("logbut.png")
lpng_photo = ImageTk.PhotoImage(lpng)
fpng = Image.open("finbut.png")
fpng_photo = ImageTk.PhotoImage(fpng)
gbpng = Image.open("getbut.png")
gbpng_photo = ImageTk.PhotoImage(gbpng)
npng = Image.open("1.png")
npng_photo = ImageTk.PhotoImage(npng)
epng = Image.open("2.png")
epng_photo = ImageTk.PhotoImage(epng)
ppng = Image.open("3.png")
ppng_photo = ImageTk.PhotoImage(ppng)
vpng = Image.open("4.png")
vpng_photo = ImageTk.PhotoImage(vpng)
cpng = Image.open("C.png")
cpng_photo = ImageTk.PhotoImage(cpng)
mpng = Image.open("M.png")
mpng_photo = ImageTk.PhotoImage(mpng)
bpng = Image.open("B.png")
bpng_photo = ImageTk.PhotoImage(bpng)
lopng = Image.open("logoutbut.png")
lopng_photo = ImageTk.PhotoImage(lopng)
tpng = Image.open("teacher.png")
tpng_photo = ImageTk.PhotoImage(tpng)
ccpng = Image.open("chatbut.png")
ccpng_photo = ImageTk.PhotoImage(ccpng)
expng = Image.open("exitbut.png")
expng_photo = ImageTk.PhotoImage(expng)
bbpng = Image.open("backbut.png")
bbpng_photo = ImageTk.PhotoImage(bbpng)
onpng = Image.open("on.png")
onpng_photo = ImageTk.PhotoImage(onpng)
offpng = Image.open("off.png")
offpng_photo = ImageTk.PhotoImage(offpng)
upng = Image.open("userbut.png")
upng_photo = ImageTk.PhotoImage(upng)
gopng = Image.open("gobackbut.png")
gopng_photo = ImageTk.PhotoImage(gopng)
supng = Image.open("susbut.png")
supng_photo = ImageTk.PhotoImage(supng)
repng = Image.open("rebut.png")
repng_photo = ImageTk.PhotoImage(repng)
rspng = Image.open("rsbut.png")
rspng_photo = ImageTk.PhotoImage(rspng)
chpwpng = Image.open("chpwbut.png")
chpwpng_photo = ImageTk.PhotoImage(chpwpng)



suspend_button = tk.Button(window, image=bbpng_photo, command=suspend,highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
remove_button = tk.Button(window, image=bbpng_photo, command=remove,highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
endismask_button = tk.Button(window, image=bbpng_photo, command=endisable_mask,highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
endischaton_button = tk.Button(window, image=onpng_photo, command=endisable_chat,highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
endischatoff_button = tk.Button(window, image=offpng_photo, command=endisable_chat,highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
idname = ""
idemail = ""
idpassword = ""
# Create the sign up and login buttons
signup_button = tk.Button(window, image=spng_photo,command=sign_up,highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
login_button = tk.Button(window, image=lpng_photo, command=login,highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
inchat_button = tk.Button(window, image=ccpng_photo, command=inchat,highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
exit_button = tk.Button(window, image=expng_photo, command=lambda: ex(chatstate,idname,idemail,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
idcard_button = tk.Button(window, image=upng_photo, command=idcard,highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)

# Create the labels and entry widgets for the username, email, password, and verification code
error_label = tk.Label(window, font=("Helvetica", 20),bg="black", fg="white")
idname_label = tk.Label(window, font=("Century Gothic", 40),bg="black", fg="#CDFFF5")
idmail_label = tk.Label(window, font=("Century Gothic", 30),bg="white")


username_label = tk.Label(window, image=npng_photo, highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
username_entry = tk.Entry(window, font=("Helvetica", 20))


email_label = tk.Label(window, image=epng_photo, highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
email_entry = tk.Entry(window, font=("Century Gothic", 20))

password_label = tk.Label(window,image=ppng_photo, highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
password_entry = tk.Entry(window, show="*", font=("Century Gothic", 20))
chat_entry = tk.Text(window, font=("Century Gothic", 20), width=25, height=4)
verif_label = tk.Label(window,image=vpng_photo, highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
verif_entry = tk.Entry(window, font=("Century Gothic", 20))

chat_entry = tk.Text(window, font=("Century Gothic", 20), width=25, height=4)
chat_label = tk.Label(window, font=("Century Gothic", 20),bg="white", fg="black",width=24)

# Create the finish buttons for sign up and login
signupfinish_button = tk.Button(window, image=fpng_photo, command=signupfinish,highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
verif_button = tk.Button(window, image=gbpng_photo, command=email,highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)

chat_button = tk.Button(window, image=cpng_photo, command =chat,highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
mask_button = tk.Button(window, image=mpng_photo,command =mask,highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
back_button = tk.Button(window, image=bpng_photo,command=lambda: inbackend(chatstate,idname,idemail,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)
loginfinish_button = tk.Button(window, image=fpng_photo,command=lambda:loginfinish(chatstate,idname,idemail,maskstate,idpassword),highlightthickness=0, bd=0, bg=window.cget('bg'), fg=window.cget('bg'), width=0, height=0)

message = chat_entry.get("1.0", tk.END)
messages = [
    # system message to set the behavior of the assistant
    {"role": "system", "content": "You are a helpful assistant called Pepper!Please reply within 1 sentense."},
]
chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
reply = chat_completion["choices"][0]["message"]["content"]
messages.append({"role": "assistant", "content": reply})

# Add the sign up and login buttons to the window
signup_button.place(x=650,y =670)
login_button.place(x=1000, y=670)

# Add the error label to the window
error_label.place(x=750, y=630)

verification_code = generate_verification_code()
ver_code = verification_code

chatstate = 0
maskstate = 0
window.mainloop()
