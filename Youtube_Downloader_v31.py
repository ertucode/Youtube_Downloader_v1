    # https://github.com/TomSchimansky/CustomTkinter/wiki
    # pip install -r filepath\requirements.txt
    # pip show modulename >>> Shows dependencies
    # pip freeze > requirements.txt

# --noconfirm --onedir --windowed --icon youtube.ico --add-data "c:\users\ertug\appdata\local\programs\python\python310\lib\site-packages\customtkinter;customtkinter\" "C:\Users\ertug\G_Drive\Code\Python\Youtube_Downloader_v3_venv\Youtube_Downloader_v3\Youtube_Downloader_v31.py"




import tkinter
from tkinter import ttk


import customtkinter
from checkbox import Checkbox
from radio import RadioButton
from button import Button
from warnuser import WarnUser
from combobox import ComboBox

import sys
from pytube import YouTube, Playlist
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')



FRAMEBGCOLOR = "system3dDarkShadow"
BGCOLOR = "gray12"
COMPLETEDCOLOR = "green yellow"

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

def roundUp(n1,n2):
    return int(n1 / n2) + (n1 % n2 > 0)

def q(text):
    while text[-1] == ".":
        text = text[:-1]
    return text




def fixtitle(title):
    title = title.replace('"',"")
    title = title.replace("'","")
    title = title.replace(":","_")
    title = title.replace("<","_")
    title = title.replace(">","_")
    title = title.replace("/","_")
    title = title.replace("\\","_")
    title = title.replace("*","_")
    title = title.replace("?","_")
    title = title.replace("|","_")
    return title

def best_audio(streams):
    audios = streams.filter(only_audio=True)
    bestQ = 0
    for audio in audios:
        abr = ""
        for letter in audio.abr:
            if letter.isdigit():
                abr += letter
        abr = int(abr)
        if abr > bestQ:
            bestQ = abr
            best = audio
    return best

class App():
    def __init__(self,type="s",url=""):
        self.root = customtkinter.CTk()
        self.type = type
        self.url = url
        self.WIDTH, self.HEIGHT = 1250, 500
        self.FULLHEIGHT = self.HEIGHT + 150
        self.center_window()
        self.root.title("Youtube Downloader v3")

        self.LISTFRAMEX = 300
        self.LISTFRAMEY = self.HEIGHT * 0.05
        self.LISTFRAMEWIDTH = self.WIDTH * 0.73
        self.LISTFRAMEHEIGHT = self.HEIGHT * 0.7
        self.LISTFRAME = customtkinter.CTkFrame(master=self.root,corner_radius= 10, fg_color = FRAMEBGCOLOR)
        self.LISTFRAME.place(x = self.LISTFRAMEX,y = self.LISTFRAMEY , width = self.LISTFRAMEWIDTH, height = self.LISTFRAMEHEIGHT)

        self.LEFTFRAMEX = 50
        self.LEFTFRAMEY = self.HEIGHT * 0.05
        self.LEFTFRAMEWIDTH = 200
        self.LEFTFRAMEHEIGHT = self.HEIGHT * 0.9
        self.LEFTFRAME = customtkinter.CTkFrame(master=self.root,corner_radius=10,fg_color=FRAMEBGCOLOR)
        self.LEFTFRAME.place(x = self.LEFTFRAMEX,y= self.LEFTFRAMEY , width = self.LEFTFRAMEWIDTH , height = self.LEFTFRAMEHEIGHT)

        self.RADIOFRAMEY = self.LISTFRAMEY + self.LISTFRAMEHEIGHT + 0.030 * self.HEIGHT
        self.RADIOFRAMEHEIGHT = 0.07 * self.HEIGHT
        self.RADIOFRAME = customtkinter.CTkFrame(master=self.root,corner_radius= 10,fg_color=FRAMEBGCOLOR)
        self.RADIOFRAME.place(x = self.LISTFRAMEX,y = self.RADIOFRAMEY  , width = self.LISTFRAMEWIDTH, height = self.RADIOFRAMEHEIGHT)

        self.UFRAMEY = self.RADIOFRAMEY + self.RADIOFRAMEHEIGHT + self.HEIGHT * 0.01
        self.UFRAMEHEIGHT = self.HEIGHT * 0.1
        self.URLFRAME = customtkinter.CTkFrame(master=self.root,corner_radius= 10,fg_color=FRAMEBGCOLOR)
        self.URLFRAME.place(x = self.LISTFRAMEX, y = self.UFRAMEY, width = self.LISTFRAMEWIDTH, height = self.UFRAMEHEIGHT)

        self.CONFRAMEY = self.UFRAMEY + self.UFRAMEHEIGHT + 20
        self.CONFRAMEHEIGHT = self.HEIGHT * 0.275
        self.CONFRAMEWIDTH = self.WIDTH * 0.93
        self.CONSOLEFRAME = customtkinter.CTkFrame(master=self.root,corner_radius= 10,fg_color=FRAMEBGCOLOR)
        self.CONSOLEFRAME.place(x = self.LEFTFRAMEX, y = self.CONFRAMEY, width = self.CONFRAMEWIDTH, height = self.CONFRAMEHEIGHT)

        self.changeStyle()
        import tkinter.font as tkfont
        goodfonts = "Century Schoolbook","Cascadia Code","Rockwell Extra Bold"
        LISTBOXFONT = tkfont.Font(family="Cascadia Code", size = "9",weight="bold")
        self.LISTBOX = tkinter.Listbox(self.CONSOLEFRAME,font = LISTBOXFONT,fg = "gray84",bd = 0,bg =FRAMEBGCOLOR,width = 168,height = 8)
        ##come
        self.LISTBOX.place(relx=-0.001, rely=-0.001, anchor="nw")
        self.STARTINGPOINT = 0
        self.PLAYLISTRADIOVARIABLE = tkinter.IntVar()
        self.PLAYLISTRADIOVARIABLE.set(self.STARTINGPOINT)   
        self.PutUrlFrameItems()
        self.ChangeLayout()
        self.PutLeftFrameItems()
        
    def changeStyle(self):
        style= ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground= FRAMEBGCOLOR, background= FRAMEBGCOLOR, foreground = "white", arrowcolor = "white",selectbackground="blue",lightcolor = FRAMEBGCOLOR)
        style.configure("TCombobox", bordercolor = "white")
        self.root.option_add('*TCombobox*Listbox.background', FRAMEBGCOLOR)
        self.root.option_add('*TCombobox*Listbox.foreground', "white")
        self.root.option_add('*TCombobox*Listbox.selectbackground', "dark slate gray")

    def PutUrlFrameItems(self):
        self.changeUrlButton = Button(self.URLFRAME,0.9,0.5,"Change Url",self.ChangeUrl,"coral1","red",150)
        self.URLENTRY = customtkinter.CTkEntry(master=self.URLFRAME, placeholder_text="Enter URL",
                                        width = self.WIDTH * 0.4,text_font=("Cascadia Code",9))
        self.URLENTRY.pack(side = "left", padx = 8)
        self.URLENTRY.insert(0,self.url)

        self.TYPERADIOVARIABLE = tkinter.IntVar()
        self.URLRADIOBOX1 = RadioButton(self.URLFRAME,0,1,sharedVar=[self.PLAYLISTRADIOVARIABLE,self.TYPERADIOVARIABLE],idd="Playlist")
        self.URLRADIOBOX2 = RadioButton(self.URLFRAME,1,1,sharedVar=[self.PLAYLISTRADIOVARIABLE,self.TYPERADIOVARIABLE],idd="Single Track")   
        if self.type == "p" : self.TYPERADIOVARIABLE.set(0)
        else : self.TYPERADIOVARIABLE.set(1)

    def ChangeUrl(self):

        t = "p" if self.TYPERADIOVARIABLE.get() == 0 else "s"
        if self.url == self.URLENTRY.get() and self.type == t: return

        self.changeUrlButton.button.set_text("Processing...")
        self.changeUrlButton.button.configure(fg_color = "red", text_color = "white")
        self.changeUrlButton.button.state = "disabled"
        self.root.update()
        try:
            if self.type == "p":
                for lst in self.checkBoxList:
                    for box in lst:
                        del box
                self.checkBoxList = []
                for box in self.radioboxs:
                    del box
                self.radioboxs = []
                for child in self.LISTFRAME.winfo_children():
                    if not type(child).__name__ == "CTkCanvas":
                        child.destroy() 
                for child in self.RADIOFRAME.winfo_children():
                    if not type(child).__name__ == "CTkCanvas":
                        child.destroy()
            elif self.type == "s":
                for child in self.LISTFRAME.winfo_children():
                    if not type(child).__name__ == "CTkCanvas":
                        child.destroy()
                
                del self.singleCheckBox

        except Exception as e:  print(f"{e} + >>>Exception")


        self.url = self.URLENTRY.get()
        self.type = "p" if self.TYPERADIOVARIABLE.get() == 0 else "s"


        self.ChangeLayout()

    def PutLeftFrameItems(self):
        self.selectAllButton= Button(self.LEFTFRAME,0.5,0.05,"Select All Items",self.SelectAll,"dark slate blue","purple1",width= 180)
        self.deselectAllButton = Button(self.LEFTFRAME,0.5,0.12,"Deselect All Items",self.deSelectAll,"maroon","black",width= 180)
        self.selectShownButton = Button(self.LEFTFRAME,0.5,0.19,"Select Shown Items",self.SelectShown,"dark slate blue","purple1",width= 180)
        self.deselectShownButton = Button(self.LEFTFRAME,0.5,0.26,"Deselect Shown Items",self.deSelectShown,"maroon","black",width= 180)
        


        self.vidbox = Checkbox(self.LEFTFRAME, "Video", 100, "off",type = "b",locx = 0.25,locy = 0.32)
        self.vidbox.packBox()
        self.audbox = Checkbox(self.LEFTFRAME, "Audio", 100, "off",type = "b",locx = 0.25,locy = 0.40)
        self.audbox.packBox()
        
        def Alltypes():
            if self.allbox.var.get() == "off":
                self.vidbox.check()
                self.audbox.check()
                try:self.subbox.check();
                except:pass;
            elif self.allbox.var.get() == "on":
                self.vidbox.decheck()
                self.audbox.decheck()
                try:self.subbox.decheck();
                except:pass;

        self.allbox = Checkbox(self.LEFTFRAME, "All", 100, "off",type = "b",locx = 0.6,locy = 0.4)
        self.allbox.packBox()
        self.allbox.checkbox.configure(command = Alltypes) 
        self.downloadButton = Button(self.LEFTFRAME,0.5,0.9,"Download",self.DownloadButtonFunc,"grey16","grey30")

    def CheckIfUrlAgreesWithType(self):
        self.purl = False
        self.yurl = False
        if not self.url == "" and not self.url == " ":
            if self.type == "p":
                try:
                    self.p = Playlist(self.url)
                    xd = self.p.title
                    self.purl = True
                except:
                    try:
                        self.yt = YouTube(self.url,on_progress_callback=self.downloadCallback,on_complete_callback=self.doneCallback)
                        self.type = "s"
                        self.yurl = True
                        WarnUser("You have given a single file link, But chosen playlist")
                    except:
                        WarnUser("Invalid URL")

            if self.type == "s":
                try:
                    self.yt = YouTube(self.url,on_progress_callback=self.downloadCallback)
                    self.yurl = True
                except:
                    try:
                        p = Playlist(self.url)
                        xd = p.title
                        WarnUser("You have given a playlist link, But chosen single file")
                    except:
                        WarnUser("Invalid URL")

    def doneCallback(self):
        self.videoprogressbar.destroy()


        


    def ChangeLayout(self):
        self.CheckIfUrlAgreesWithType()
        if self.purl:
            self.getTitlesAndYoutubes()
            self.VIDEOCOUNT = len(self.titles)
            self.LISTLENGTH = 10
            self.LISTCOUNT = roundUp(self.VIDEOCOUNT,self.LISTLENGTH)

            self.checkBoxList = []
            
            for j in range (0,self.LISTCOUNT):
                # For boxes for a perticulator frame
                checkboxs = []
                for i in range(1,self.LISTLENGTH + 1 ):   #This starts from 1 not 0!!!
                    if i+j*self.LISTLENGTH > self.VIDEOCOUNT: break
                    checkboxs.append(Checkbox(self.LISTFRAME,f"{str(i+j*self.LISTLENGTH)}", 400, title = self.titles[i+j*self.LISTLENGTH-1]))
                self.checkBoxList.append(checkboxs)

            ############# INDIVIDUAL --- RADIOS ----- ####################            
            self.radioboxs = []
            for i in range(0,self.LISTCOUNT):
                self.radioboxs.append(RadioButton(self.RADIOFRAME,i,0,sharedVar=[self.PLAYLISTRADIOVARIABLE],boxes = self.checkBoxList))

            # Showing the first 10 items of the playlist
            for box in self.checkBoxList[self.STARTINGPOINT]:
                box.packBox()


        if self.yurl:
            self.LISTCOUNT = 1
            self.LISTLENGTH = 10

            self.singleCheckBox = Checkbox(self.LISTFRAME,f"{str(1)}",400,title = self.yt.title)
            self.singleCheckBox.packBox()

        if self.yurl:
            if self.yt.captions:
                self.putSubFrameItems()
            else:
                for child in self.SUBFRAME.winfo_children():
                    if not type(child).__name__ == "CTkCanvas":
                        child.destroy()

        if self.purl:
            self.putSubFrameItems()

        
        self.changeUrlButton.button.set_text("Change Url")
        self.changeUrlButton.button.state = "normal"
        self.changeUrlButton.button.configure(fg_color = "coral1")
        self.changeUrlButton.button.configure(text_color = "white")
        self.root.update()

    def putSubFrameItems(self):
        self.SUBFRAME = customtkinter.CTkFrame(master=self.LEFTFRAME,corner_radius=10,fg_color=FRAMEBGCOLOR)
        self.SUBFRAME.place(x = 0,y= self.LEFTFRAMEHEIGHT * 0.48, width = self.LEFTFRAMEWIDTH , height = self.LEFTFRAMEHEIGHT / 3)
        self.subbox = Checkbox(self.SUBFRAME, "Sub", 100, "off",type = "b",locx = 0.25,locy = 0.02)
        self.subbox.packBox()
        def GiveAdvice():
            WarnUser("[tr] > Turkish, [en] > English, [a.lang] Auto Generated")

        self.subQbut = Button(self.SUBFRAME,0.1,0.1,"?",GiveAdvice,"PaleGreen4","SpringGreen4",width = 30)

        captions = self.yt.captions if self.yurl else self.YouTubes[0].captions
        self.suboptions = []
        for capt in captions:
            st = f"{capt}"
            sts = st.split('"')
            self.suboptions.append(sts[-2])
        if len(self.suboptions) == 0: self.suboptions.append("en")
        self.subcombo = ComboBox(self.SUBFRAME,0.8,0.1,5,self.suboptions)

    def getTitlesAndYoutubes(self):
        # Get titles and youtubes for playlist
        self.titles = None

        if self.purl:
            if self.type == "p":
                self.p = Playlist(self.url)
                self.urls = self.p.video_urls
                def get_youtube(url):
                        return YouTube(url,on_progress_callback = self.downloadCallback)
                        
                def get_title(ind,youtubeItem):
                        return (ind,youtubeItem.title)

                self.YouTubes = []
                for urll in self.urls:
                    self.YouTubes.append(get_youtube(urll))

                processes = []

                # YouTubes, url

                with ThreadPoolExecutor(max_workers=20) as executor:
                    for ind,youtubeItem in enumerate(self.YouTubes):
                        processes.append(executor.submit(lambda p: get_title(*p), (ind,youtubeItem)))


                NumberAndTitle = []
                for task in as_completed(processes):
                    NumberAndTitle.append(task.result())
                NumberAndTitle.sort()

                # NumberAndTitle = []
                # for ind,youtubeItem in enumerate(self.YouTubes):
                #     NumberAndTitle.append(get_title(ind,youtubeItem))

                self.titles = []
                for item in NumberAndTitle:
                    self.titles.append(item[1])
                if len(self.titles) > 210:
                    self.titles = self.titles[:210]
                    WarnUser("Can't put more than 210 videos")

        elif self.yurl:
            pass

    def center_window(self):
        w = self.WIDTH # width for the Tk root
        h = self.FULLHEIGHT # height for the Tk root

        # get screen width and height
        ws = self.root.winfo_screenwidth() # width of the screen
        hs = self.root.winfo_screenheight() # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        # set the dimensions of the screen 
        # and where it is placed
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def printNewLine(self,text):
        self.LISTBOX.insert("end"," "+ text)
        self.LISTBOX.yview("end")
        self.root.update()

    def printSameLine(self,text):
        if self.LISTBOX.get("end")[1] == " " or self.LISTBOX.get("end")[1] == "-":
            self.LISTBOX.delete("end")
        self.LISTBOX.insert("end"," "+ text)
        self.LISTBOX.yview("end")
        self.root.update()

    def downloadCallback(self, stream, file_handle, bytes_remaining):
        fileSize = stream.filesize
        bytes_downloaded = fileSize - bytes_remaining
        percentage = round((bytes_downloaded / fileSize) * 100, 2)
        mbb = fileSize * 10**-6
        mb = bytes_downloaded * 10**-6

        self.videoprogressbar = customtkinter.CTkProgressBar(master=self.LEFTFRAME,width = 100)
        self.videoprogressbar.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)
        self.videoprogressbar.set(percentage * 10**-2)
    
        self.printSameLine(f" {percentage}% - {mb:.2f} MB / {mbb:.2f} MB - {stream.title}")

    def SelectAll(self):
        if self.purl:
            for boxes in self.checkBoxList:
                for box in boxes:
                    box.state = "on"
                    if box.showing:
                        box.checkbox.select()

    def deSelectAll(self):
        if self.purl:
            for boxes in self.checkBoxList:
                for box in boxes:
                    box.state = "off"
                    if box.showing:
                        box.checkbox.deselect()

    def SelectShown(self):
        if self.purl:
            for boxes in self.checkBoxList:
                for box in boxes:
                    if box.showing:
                        box.state = "on"
                        box.checkbox.select()

    def deSelectShown(self):
        if self.purl:
            for boxes in self.checkBoxList:
                for box in boxes:
                    if box.showing:
                        box.state = "off"
                        box.checkbox.deselect()


    def DownloadButtonFunc(self):
        if len(self.LISTFRAME.winfo_children()) > 1:
            self.somevideochosen = False
            self.downloadButton.button.set_text("Downloading...")
            self.downloadButton.button.state = "disabled"
            self.downloadButton.button.configure(fg_color = "blue")
            self.changeUrlButton.button.configure(text_color = "white")
            self.LISTBOX.delete(0,'end')
            # butterminate.button.configure(state=tkinter.DISABLED)
            self.downloadButton.button.configure(state=tkinter.DISABLED)

            self.audio = True if self.audbox.state == "on" else False
            self.video = True if self.vidbox.state == "on" else False
            try:self.sub = True if self.subbox.state == "on" else False
            except:self.sub = False
            if self.sub:
                self.lan = self.subcombo.combobox.get()
                self.lan = self.lan if len(self.lan) > 0 else "en"
            try:
                self.videoprogressbar.destroy()
            except:
                pass
            desiredItemCount = 0
            if self.purl:
                for boxes in self.checkBoxList:
                    for box in boxes:
                        if box.state == "on":
                            desiredItemCount += 1
                        box.changeColor("white")
                if not desiredItemCount == 1:
                    self.listprogressbar = customtkinter.CTkProgressBar(master=self.LEFTFRAME,width = 100)
                    self.listprogressbar.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)
                    self.listprogressbar.set(0)
                downloadedCount = 0
                for boxes in self.checkBoxList:
                    for box in boxes:
                        if box.state == "on":
                            self.somevideochosen = True
                            if self.audio or self.sub or self.video:
                                box.changeColor("sky blue")
                                self.yt = self.YouTubes[int(box.id)-1]
                                self.downloadVideo()
                                try:
                                    self.videoprogressbar.destroy()
                                except:
                                    pass 
                                if not desiredItemCount == 1:
                                    downloadedCount += 1
                                    self.listprogressbar.set(downloadedCount / desiredItemCount)
                                box.changeColor(COMPLETEDCOLOR)

            elif self.yurl:
                # self.singleCheckBox.changeColor(COMPLETEDCOLOR)
                if self.singleCheckBox.state == "on":
                    self.somevideochosen = True
                    if self.audio or self.sub or self.video:
                        downloadedCount = 1
                        self.downloadVideo()
                        self.singleCheckBox.changeColor(COMPLETEDCOLOR)
                        try:
                            self.videoprogressbar.destroy()
                        except:
                            pass 
                            

            
            if self.audio or self.sub or self.video:
                if not downloadedCount == 0:
                    self.printNewLine("Downloads Completed..")
                    self.LISTBOX.itemconfig("end", {'fg': 'yellow'})
            else:
                WarnUser("You have not chosen any file type")

            if not self.somevideochosen:
                WarnUser("You have not chosen any videos")
                
            self.downloadButton.button.configure(state=tkinter.NORMAL)
            # butterminate.button.configure(state=tkinter.NORMAL)

            try:
                self.videoprogressbar.destroy()
            except:
                pass 
            try:
                self.listprogressbar.destroy()
            except:
                pass
            self.downloadButton.button.set_text("Download")
            self.downloadButton.button.state = "normal"
            self.downloadButton.button.configure(fg_color = "black")
            self.changeUrlButton.button.configure(text_color = "white")


    def downloadVideo(self): 
        self.printNewLine(f"Downloading - {self.yt.title} " + u"\u23e9" " Close Application to Cancel")
        
        if not self.purl:
            dir = f'{desktop}\\Youtube_Download'
        else:
            ptitle = fixtitle(self.p.title)
            dir = f'{desktop}\\Youtube_Download\\{ptitle}'

        if not os.path.exists(dir):
            os.mkdir(dir)

        if self.video:
            best = self.yt.streams.filter(file_extension='mp4').filter(progressive=True).get_highest_resolution()
            best.download(output_path=dir)
            # self.printNewLine(f"Downloaded video: {dir}/{best.title}.{best.subtype}")
            self.printSameLine("Video " + u"\u2714")
        if self.audio:
            audio = best_audio(self.yt.streams)
            audio.download(output_path=dir)
            self.printSameLine("Audio " + u"\u2714")
        if self.sub:
            vtitle = fixtitle(self.yt.title)
            if (self.yt.captions):
                if self.lan in self.yt.captions:
                    self.downloadSub(vtitle,self.lan,dir)
                elif "a."+self.lan in self.yt.captions:
                    self.downloadSub(vtitle,"a."+self.lan,dir)
                else:
                    self.printNewLine("Subtitle" + u"\u2716" "Language not available")

            else:
                self.printNewLine("Subtitle not available")

    def downloadSub(self,vtitle,lan,dir):
        
        hours = self.yt.length / 60 / 60
        minutes = (hours % 1) * 60
        secs = ( minutes % 1) * 60
        cutoff = 9.5
        if (hours > cutoff):
            estimation_in_minutes = (1175 + (89.28571 - 1175)/(1 + (int(hours)/16.07373)**428.7844)) / 60
            self.printNewLine(f"-Downloading subtitle")
            self.printNewLine(f"-Vidoe length: {int(hours)}:{int(minutes)}:{int(secs)} - Estimated subtitle download time: {estimation_in_minutes} min")

        caption = self.yt.captions[lan]
        text = caption.generate_srt_captions()
        text = text.replace('\u266a',"")
        lines = text.split("\n")
        f = open(f"{dir}\\{q(vtitle)}_{lan}.txt", 'w')  

        for i,line in enumerate(lines):
            try:
                f.write(f"{line}\n")
            except:
                f.write("Unsupported characters \n")
        if (hours > cutoff):
            self.LISTBOX.delete("end")
        self.printSameLine("Subtitle " + u"\u2714")
        f.close()

if __name__ == "__main__":
    given = False

    try:
        given = sys.argv[1]
        print(f"Input: {given}")
    except:
        pass
    if given:

        t1 = given
        if t1[-1]=="/": t1 = t1[:-1]
        t2 = t1[8:]
        splits = t2.split(",")  
        url = splits[0]
        options = splits[1]

        if options[0] == "P":
            type = "p"
        elif options[0] == "S":
            type = "s"
    if given:
        app = App(type,url)
    else:
        app = App()
    app.root.mainloop()



    