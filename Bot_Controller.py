#!/usr/bin/python3

#=========================================================== Import ===========================================================

from telethon import TelegramClient, sync
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.messages import AddChatUserRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors import SessionPasswordNeededError, FloodWaitError, PhoneNumberInvalidError
from telethon.tl.functions.messages import GetDialogsRequest
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import asyncio
import emoji
from time import sleep
import random
import sys
#=========================================================== Parameters of session ===========================================================

api_id = 1447598
api_hash = '8b5121ac8429ce37037b47ebd5f7cf23'
session_name = 'tipocheksss'

#=========================================================== Parameters of window ===========================================================

win_width = 600
win_height = 400

win = Tk()
win.title('Bot Controller')
icon_path1 = sys.argv[0]
icon_path2 = icon_path1.split('Bot_Controller.py')
icon_path2 = icon_path2[0] + 'icon.png'
image = PhotoImage(file = icon_path2)
win.iconphoto(False, image)
win.update_idletasks()
width = win.winfo_width()
height = win.winfo_height()
x = (win.winfo_screenwidth() // 2) - (win_width // 2)
y = (win.winfo_screenheight() // 2) - (win_height // 2)
win.geometry('{}x{}+{}+{}'.format(win_width, win_height, x, y))
widget_list = []

#=========================================================== Page functions ===========================================================

def login_pg1():
    #Create login page 1, ask phone number for login
    global widget_list
    global login_pg1_lbl1
    global login_pg1_phone_num_ent
    global login_pg1_Enter_btn
    clear(widget_list)


    login_pg1_lbl1 = Label(text = 'Enter phone number')
    login_pg1_lbl1.place(x = 225, y = 150, width = 150, height = 20)

    login_pg1_phone_num_ent = Entry()
    login_pg1_phone_num_ent.focus_set()
    login_pg1_phone_num_ent.bind("<Key>", login_pg1_phone_num_ent_bind)
    login_pg1_phone_num_ent.place(x = 225, y = 180, width = 150, height = 20)

    login_pg1_Enter_btn = Button(text = 'Next step', command = login_pg2)
    login_pg1_Enter_btn.bind("<Key>", login_pg1_Enter_btn_bind)
    login_pg1_Enter_btn.place(x = 250, y = 220, width = 100, height = 20)

    widget_list = [login_pg1_lbl1, login_pg1_phone_num_ent, login_pg1_Enter_btn]

def login_pg2():
    #Create login page 2 and send code request to telegram by phone number from login page 1, ask code for login
    global client
    global widget_list
    global phone_numbers
    global login_pg2_lbl1
    global login_pg2_code_num_ent
    global login_pg2_Enter_btn
    global login_pg1_phone_num_ent
    global login_pg2_back_btn
    global state
    if len(phone_numbers) < 1:
        phone_numbers = login_pg1_phone_num_ent.get()
    clear(widget_list)
    try:
        client.send_code_request(phone_numbers)
        login_pg2_lbl1 = Label(text = 'Code:')
        login_pg2_lbl1.place(x = 280, y = 160, width = 40, height = 20)

        login_pg2_code_num_ent = Entry()
        login_pg2_code_num_ent.focus_set()
        login_pg2_code_num_ent.bind("<Key>", login_pg2_code_num_ent_bind)
        login_pg2_code_num_ent.place(x = 225, y = 180, width = 150, height = 20)

        login_pg2_Enter_btn = Button(text = 'Next step', command = complete_auth)
        login_pg2_Enter_btn.bind("<Key>", login_pg2_Enter_btn_bind)
        login_pg2_Enter_btn.place(x = 250, y = 220, width = 100, height = 20)

        login_pg2_back_btn = Button(text = 'Back', command = main)
        login_pg2_back_btn.bind("<Key>", login_pg2_back_btn_bind)
        login_pg2_back_btn.place(x = 250, y = 260, width = 100, height = 20)

        widget_list = [login_pg2_lbl1, login_pg2_code_num_ent, login_pg2_Enter_btn, login_pg2_back_btn]
    except FloodWaitError as e:
        messagebox.showerror("Flood", "wait for {}s".format(e.seconds))
        login_pg1()
    except PhoneNumberInvalidError as e:
        messagebox.showerror("Error", 'Phone number invalid error')
        main()
    except Exception as e:
        print(type(e))
        messagebox.showerror('Error', 'Try again')
        main()

def login_pg3():
    #Create login page 3, ask password for login
    global widget_list
    global login_pg3_pass_ent
    global login_pg3_pass_show
    global login_pg3_Enter_btn
    clear(widget_list)

    login_pg3_pass_ent = Entry(show = '*')
    login_pg3_pass_ent.focus_set()
    login_pg3_pass_ent.bind("<Key>", login_pg3_pass_ent_bind)
    login_pg3_pass_ent.place(x = 225, y = 180, width = 150, height = 20)

    login_pg3_pass_show = Button(text = 'show', command = show_hide)
    login_pg3_pass_show.bind("<Key>", login_pg3_pass_show_bind)
    login_pg3_pass_show.place(x = 400, y = 180, width = 50, height = 20)

    login_pg3_Enter_btn = Button(text = 'Sign_in', command = complete_auth2)
    login_pg3_Enter_btn.bind("<Key>", login_pg3_Enter_btn_bind)
    login_pg3_Enter_btn.place(x = 250, y = 220, width = 100, height = 20)
    widget_list = [login_pg3_pass_ent, login_pg3_pass_show, login_pg3_Enter_btn]

def menu_pg():
    #Create menu page
    global widget_list
    global menu_pg_start_btn
    global menu_pg_Log_out_btn
    clear(widget_list)

    menu_pg_start_btn = Button(text = 'Start', command = config_pg1)
    menu_pg_start_btn.focus_set()
    menu_pg_start_btn.bind("<Key>", menu_pg_start_btn_bind)
    menu_pg_start_btn.place(x = 250, y = 180, width = 100, height = 20)

    menu_pg_Log_out_btn = Button(text = 'Log out', command = log_out)
    menu_pg_Log_out_btn.bind("<Key>", menu_pg_Log_out_btn_bind)
    menu_pg_Log_out_btn.place(x = 250, y = 220, width = 100, height = 20)
    widget_list = [menu_pg_start_btn, menu_pg_Log_out_btn]

def config_pg1():
    #Create Config page 1
    global widget_list
    global filename
    global config_pg1_file_path_lbl1
    global config_pg1_reopen_file_btn
    global config_pg1_listbox
    global config_pg1_confirm_btn
    clear(widget_list)
    if filename.get() == '':
        get_path_to_file()
    chats = get_list()
    config_pg1_file_path_lbl1 = Label(textvariable = filename)
    config_pg1_file_path_lbl1.place(y = 100, x = 0, width = 600, height = 20)

    config_pg1_reopen_file_btn = Button(text = 'Reopen', command = get_path_to_file)
    config_pg1_reopen_file_btn.focus_set()
    config_pg1_reopen_file_btn.bind("<Key>", config_pg1_reopen_file_btn_bind)
    config_pg1_reopen_file_btn.place(x = 255, y = 140, width = 90, height = 20)

    config_pg1_listbox = Listbox()
    for chat in chats:
        config_pg1_listbox.insert(END, chat)
    config_pg1_listbox.place(x = 200, y = 180, width = 200, height = 90)

    config_pg1_confirm_btn = Button(text = 'Confirm', command = config_pg2)
    config_pg1_confirm_btn.bind("<Key>", config_pg1_confirm_btn_bind)
    config_pg1_confirm_btn.place(x = 255, y = 290, width = 90, height = 20)

    widget_list = [config_pg1_file_path_lbl1, config_pg1_reopen_file_btn, config_pg1_listbox, config_pg1_confirm_btn]

def config_pg2():
    #Create Config page 2
    global widget_list
    global filename
    global config_pg2_user_count_lbl
    global config_pg2_user_count_ent
    global config_pg2_confirm_btn
    global config_pg2_back_btn
    global chat_name
    global list_of_users
    if chat_name == '':
        print(chat_name)
        chat_name = selected_chat()
    clear(widget_list)
    if filename.get() == '' and chat_name == "nothing is selected":
        messagebox.showerror('Error', 'File and chat\nnot selected')
        config_pg1()
    elif filename.get() == '':
        messagebox.showerror('Error', 'File not selected')
        config_pg1()
    elif chat_name == "nothing is selected":
        messagebox.showerror('Error', 'chat not selected')
        config_pg1()
    else:
        try:
            list_of_users = get_list_of_user()
            config_pg2_user_count_lbl = Label(text = '{} users\nhow much users add?'.format(len(list_of_users)))
            config_pg2_user_count_lbl.place(x = 200, y = 120, width = 200, height = 30)

            config_pg2_user_count_ent = Entry()
            config_pg2_user_count_ent.focus_set()
            config_pg2_user_count_ent.bind("<Key>", config_pg2_user_count_ent_bind)
            config_pg2_user_count_ent.place(x = 270, y = 160, width = 60, height = 20)

            config_pg2_confirm_btn = Button(text = 'Confirm', command = add_members)
            config_pg2_confirm_btn.bind("<Key>", config_pg2_confirm_btn_bind)
            config_pg2_confirm_btn.place(x = 260, y = 190, width = 80, height = 20)

            config_pg2_back_btn = Button(text = 'Back', command = config_pg1)
            config_pg2_back_btn.bind("<Key>", config_pg2_back_btn_bind)
            config_pg2_back_btn.place(x = 260, y = 220, width = 80, height = 20)

            widget_list = [config_pg2_user_count_lbl, config_pg2_user_count_ent, config_pg2_confirm_btn, config_pg2_back_btn]
        except Exception as e:
            messagebox.showerror('Error', 'File invalid')
            filename.set('')
            config_pg1()


#=========================================================== Bind functions ===========================================================
def login_pg1_phone_num_ent_bind(events):
    global login_pg1_Enter_btn
    if events.keysym in ['Return', 'Down']:
        login_pg1_Enter_btn.focus_set()
    elif events.keysym == 'Up':
        pass

def login_pg1_Enter_btn_bind(events):
    global login_pg1_phone_num_ent
    if events.keysym == 'Return':
        login_pg2()
    elif events.keysym == 'Up':
        login_pg1_phone_num_ent.focus_set()

def login_pg2_code_num_ent_bind(events):
    global login_pg2_Enter_btn
    if events.keysym in ['Return', 'Down']:
        login_pg2_Enter_btn.focus_set()

def login_pg2_Enter_btn_bind(events):
    global login_pg2_code_num_ent
    global login_pg2_back_btn
    if events.keysym == 'Return':
        complete_auth()
    elif events.keysym == 'Up':
        login_pg2_code_num_ent.focus_set()
    elif events.keysym == 'Down':
        login_pg2_back_btn.focus_set()

def login_pg2_back_btn_bind(events):
    global login_pg2_Enter_btn
    if events.keysym == 'Return':
        main()
    elif events.keysym == 'Up':
        login_pg2_Enter_btn.focus_set()

def login_pg3_pass_ent_bind(events):
    global login_pg3_Enter_btn
    global login_pg3_pass_show
    if events.keysym in ['Return', 'Down']:
        login_pg3_Enter_btn.focus_set()
    elif events.keysym == 'Right':
        login_pg3_pass_show.focus_set()

def login_pg3_pass_show_bind(events):
    global login_pg3_pass_ent
    global login_pg3_Enter_btn
    if events.keysym == 'Return':
        show_hide()
    elif events.keysym in ['Left', 'Up']:
        login_pg3_pass_ent.focus_set()
    elif events.keysym == 'Down':
        login_pg3_Enter_btn.focus_set()

def login_pg3_Enter_btn_bind(events):
    global login_pg3_pass_ent
    global login_pg3_pass_show
    if events.keysym == 'Return':
        complete_auth2()
    elif events.keysym == 'Up':
        login_pg3_pass_ent.focus_set()
    elif events.keysym == 'Right':
        login_pg3_pass_show.focus_set()

def menu_pg_start_btn_bind(events):
    global menu_pg_Log_out_btn
    if events.keysym == 'Return':
        config_pg1()
    elif events.keysym == 'Down':
        menu_pg_Log_out_btn.focus_set()


def menu_pg_Log_out_btn_bind(events):
    global menu_pg_start_btn
    if events.keysym == 'Return':
        log_out()
    elif events.keysym == 'Up':
        menu_pg_start_btn.focus_set()

def config_pg1_reopen_file_btn_bind(events):
    global config_pg1_listbox
    if events.keysym == 'Down':
        config_pg1_listbox.focus_set()
    elif events.keysym == 'Return':
        get_path_to_file()

def config_pg1_confirm_btn_bind(events):
    global config_pg1_listbox
    if events.keysym == 'Up':
        config_pg1_listbox.focus_set()
    elif events.keysym == 'Return':
        config_pg2()

def config_pg2_user_count_ent_bind(events):
    global config_pg2_confirm_btn
    if events.keysym in ['Return', 'Down']:
        config_pg2_confirm_btn.focus_set()

def config_pg2_confirm_btn_bind(events):
    global config_pg2_back_btn
    if events.keysym == 'Return':
        add_members()
    elif events.keysym == 'Down':
        config_pg2_back_btn.focus_set()

def config_pg2_back_btn_bind(events):
    global config_pg2_confirm_btn
    if events.keysym == 'Return':
        config_pg1()
    elif events.keysym == 'Up':
        config_pg2_confirm_btn.focus_set()

#=========================================================== Auth functions ===========================================================

def complete_auth():
    global client
    global login_pg2_code_num_ent
    global phone_numbers
    global code
    code = login_pg2_code_num_ent.get()
    try:
        client.sign_in(phone_numbers)
    except:
        main()
    try:
        client.sign_in(phone_numbers, code)
        menu_pg()
    except SessionPasswordNeededError:
        login_pg3()
    except:
        messagebox.showerror("Invalid code", "Please try again")
        login_pg2()

def complete_auth2():
    global client
    global login_pg3_pass_ent
    global phone_numbers
    global code
    password = login_pg3_pass_ent.get()
    try:
        client.sign_in(phone_numbers, code)
    except:
        try:
            client.sign_in(password = password)
            menu_pg()
        except Exception as e:
            messagebox.showerror("Error", "Incorrect password")
            login_pg3()

#=========================================================== System functions ===========================================================

def clear(widget_list):
    #Clear all widgets on page
    for i in widget_list:
        i.destroy()
    widget_list = []

def show_hide():
    #Show or hide password on login page 3
    global login_pg3_pass_ent
    if login_pg3_pass_show["text"] == 'show':
        login_pg3_pass_show["text"] = 'hide'
        login_pg3_pass_ent['show'] = ''
    else:
        login_pg3_pass_show["text"] = 'show'
        login_pg3_pass_ent['show'] = '*'

def log_out():
    #Log out from telegram and go to login page 1 to login
    global client
    client.log_out()
    main()

def get_path_to_file():
    global filename
    filename.set(askopenfilename())

def get_list_of_user():
    #Get and return list of user from file
    #File format txt and like
    #@username1
    #@username2
    #@username3
    global filename

    list_of_user = []
    with open(filename.get(), 'r') as file:
        for line in file:
            list_of_user.append(line.split()[0])
    return list_of_user

def give_emoji_free_text(text):
    #Delete emoji
    return emoji.get_emoji_regexp().sub(r' ', text.decode('utf8'))

def get_list():
    #Get and return chat list from telegram
    last_date = None
    chunk_size = 200
    result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
    chats = {}
    for i in result.chats:
        title = give_emoji_free_text(i.title.encode('utf8'))
        chats[title] = i
    return chats

def selected_chat():
    global config_pg1_listbox
    selection = config_pg1_listbox.curselection()
    if selection:
        return config_pg1_listbox.get(selection[0])
    else:
        return("nothing is selected")

def add_member(chat, nickname):
    #Add users to channel, group, or megagroup
    global added_users
    global failed_users
    try:
        target_group_entity = client.get_entity(chat.id)
    except:
        sleep(10)
        target_group_entity = chat.title
    try:
        sleep(10)
        client(AddChatUserRequest(target_group_entity, nickname, 10))
    except Exception as e:
        try:
            sleep(10)
            client(InviteToChannelRequest(target_group_entity, [nickname]))
            added_users += 1
        except Exception as e:
            try:
                try:
                    sleep(10)
                    target_group_entity = chat.migrated_to
                except:
                    try:
                        sleep(10)
                        target_group_entity = InputPeerChannel(chat.id, chat.access_hash)
                    except:
                        pass
                sleep(10)
                client(InviteToChannelRequest(target_group_entity, [nickname]))
                added_users += 1
            except Exception as e:
                print(" \n-----\nusername: {}\n{}\n-----\n ".format(nickname, e))
                failed_users += 1

def random_list(count):
    global list_of_users
    global random_list_of_user
    random_list_of_user = []
    for i in range(count):
        local_varibale = random.choice(list_of_users)
        random_list_of_user.append(local_varibale)
        list_of_users.remove(local_varibale)
    return random_list_of_user

def add_members():
    global added_users
    global failed_users
    global list_of_users
    global config_pg2_user_count_ent
    global chat_name
    count_of_user_for_add = int(config_pg2_user_count_ent.get())
    if count_of_user_for_add > len(list_of_users):
        count_of_user_for_add = len(list_of_users)
    random_list_users = random_list(count_of_user_for_add)
    added_users = 0
    failed_users = 0
    counter = 0
    chats = get_list()
    sleep(10)
    chat = chats[chat_name]
    for user in random_list_users:
        print('{}%'.format(counter/len(random_list_users) * 100))
        add_member(chat, user)
        counter += 1
        if counter % 20 == 0:
            print('Time to sleep\nPlease wait 10 minute')
            sleep(600)
        else:
            sleep(120)
    messagebox.showinfo('Completed', 'added users {}\nfailed users {}'.format(added_users, failed_users))
    chat_name = ''
    config_pg1()

#=========================================================== Main function ===========================================================

def main():
    #Start login to telegram if session not saved else go to menu page
    global client
    global api_id
    global api_hash
    global session_name
    global phone_numbers
    global filename
    global chat_name
    phone_numbers = ''
    chat_name = ''
    filename = StringVar()
    filename.set('')
    client = TelegramClient(session_name, api_id, api_hash)
    client.connect()
    if not client.is_user_authorized():
        login_pg1()
    else:
        menu_pg()

main()
win.mainloop()
