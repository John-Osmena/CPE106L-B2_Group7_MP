from tkinter import *
from PIL import ImageTk, Image
import sqlite3


# Database
#

    global bpmbtn
    if bpmbtn == False:
        bpmbtn = True
    else:
        bpmbtn = False


def dance():
    global dancebtn
    if dancebtn == False:
        dancebtn = True
    else:
        dancebtn = False


def generate():
    sentry = songentry.get()
    with conn2:
        c2.execute("SELECT * FROM top10s WHERE title = :entry ", {'entry': sentry})
    var = c2.fetchone()
    if not bpmbtn:
        bpm=var[5]
    else:
        bpm=0
    if not enrgbtn:
        energy=var[6]
    else:
        energy = 0

    if not dancebtn:
        dance=var[7]
    else:
        dance = 0

    with conn2:
        c2.execute("SELECT * FROM top10s ORDER BY ABS(bpm-:bpm), ABS(nrgy-:energy), ABS(dnce-:dance) LIMIT 10", {'bpm': bpm, 'energy': energy, 'dance':dance})

    var=c2.fetchall()
    text=""
    for x in var:
        text+=f"{x[1]} -- {x[2]} ({x[4]})\n"
    label1=Label(frame2, text="SIMILAR SONGS", pady=20)
    label1.grid(row=4,column=1)
    label2=Label(frame2, text=text)
    label2.grid(row=5, column=1)



# conn.commit()
#
#
# conn.close()


if __name__ == '__main__':

    global bpmbtn
    bpmbtn = True
    global enrgbtn
    enrgbtn = True
    global dancebtn
    dancebtn = True

    conn2 = sqlite3.connect('mp106.db')
    c2 = conn2.cursor()

    root = Tk()
    root.title('Sign in')
    root.geometry("400x600")

# Frame1
    #Creation of bg frame 
    frame1 = Frame(root, bg = "#564E58")
    #Packing of the frame to the whole window to make it expandable and collpasable
    frame1.pack(fill='both', expand='yes')

    fname = Entry(frame1, width=30)
    lname = Entry(frame1, width=30)
    username = Entry(frame1, width=30)
    password = Entry(frame1, width=30)

    fnamel = Label(frame1, text="First Name", bg="#564E58", fg='white')
    lnamel = Label(frame1, text="Last Name", bg="#564E58", fg='white')
    usernamel = Label(frame1, text="Username", bg="#564E58", fg='white')
    passwordl = Label(frame1, text="Password", bg="#564E58", fg='white')

    submitbtn = Button(frame1, text="Submit", command=submit)

    loginbtn = Button(frame1, text="Login", command=login, width=10)
    loginbtn.place(x=200, y=200, anchor=CENTER)

    signupbtn = Button(frame1, text="Signup", command=signup, width=10)
    signupbtn.place(x=200, y=230, anchor=CENTER)
    
# Frame2

    frame2 = Frame(root, padx=100, pady=150, bg="#F2EFE9")
    frame2.pack(fill='both', expand='yes')

    songlabel = Label(frame2, text="Song")
    songlabel.grid(row=0, column=0)

    songentry = Entry(frame2, width=30)
    songentry.grid(row=0, column=1)

    similarlabel = Label(frame2, text="Similar By")
    similarlabel.grid(row=1, column=1,pady=30, ipadx=20)

    sbtn1 = Button(frame2, text="BPM", command=bpm)
    sbtn1.grid(row=2, column=0)
    sbtn2 = Button(frame2, text="Energy",command=energy)
    sbtn2.grid(row=2, column=1)
    sbtn3 = Button(frame2, text="Dance",command=dance)
    sbtn3.grid(row=2, column=2)
    sbtn4 = Button(frame2, text = "Add to playlist")
    sbtn4.grid(row=0, column=3)
    sbtn4 = Button(frame2, text = "Open playlist")
    sbtn4.grid(row=0, column=4)
    gbtn = Button(frame2, text="GENERATE", bg="#904E55", comman=generate)
    gbtn.grid(row=3, column=1, pady=50, ipadx=10,ipady=25)


    root.mainloop()

    conn2.commit()
    conn2.close()
