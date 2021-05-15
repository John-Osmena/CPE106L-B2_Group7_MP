from tkinter import *
from PIL import ImageTk, Image
import sqlite3


# Database
#
# conn = sqlite3.connect('mp.db')
#
#
# c = conn.cursor()



def addtoplaylist():
     for x in generate.var:
        with conn2:
            c2.execute("INSERT INTO playlist(Song, Artist) VALUES(?,?)",(x[1], x[2]))

def openplaylist():
    with conn2:
        c2.execute("SELECT * FROM playlist")

    var = c2.fetchall()
    text = ""
    for x in var:
        text += f"{x[0]} -- {x[1]} )\n"

    labelp = Label(frame2, text="PLAYLIST", pady=20)
    labelp.grid(row=1, column=4)
    labelp2 = Label(frame2, text=text)
    labelp2.grid(row=2, column=4)

def energy():
    global enrgbtn
    if enrgbtn == False:
        enrgbtn = True
    else:
        enrgbtn = False



def bpm():
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
    generate.var = c2.fetchone()
    if not bpmbtn:
        bpm=generate.var[5]
    else:
        bpm=0
    if not enrgbtn:
        energy=generate.var[6]
    else:
        energy = 0

    if not dancebtn:
        dance=generate.var[7]
    else:
        dance = 0

    with conn2:
        c2.execute("SELECT * FROM top10s ORDER BY ABS(bpm-:bpm), ABS(nrgy-:energy), ABS(dnce-:dance) LIMIT 10", {'bpm': bpm, 'energy': energy, 'dance':dance})

    generate.var=c2.fetchall()
    text=""
    for x in generate.var:
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

    
# Frame2

    frame2 = Frame(root, padx=100, pady=150, bg="#F2EFE9")
    frame2.pack()
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
    sbtn4 = Button(frame2, text = "Add to playlist", command=addtoplaylist)
    sbtn4.grid(row=0, column=3)
    sbtn4 = Button(frame2, text = "Open playlist", command=openplaylist)
    sbtn4.grid(row=0, column=4)
    gbtn = Button(frame2, text="GENERATE", bg="#904E55", comman=generate)
    gbtn.grid(row=3, column=1, pady=50, ipadx=10,ipady=25)


    root.mainloop()

    conn2.commit()
    conn2.close()