import sys, time, random, os, subprocess
from Tkinter import *

# some global variables
maxwaittime = 4 # maximum waiting time, in seconds
minwaittime = 1.5 # minimal waiting time in seconds
cwidth = 200 # default canvas width for stimulus
cheight = 250
picdir = os.path.join(os.curdir,'pics')

showavg = 0

class Visual(Frame):
    """A visual stimulus object that's also a frame. width and height set the size of the canvas on the frame"""
    def __init__(self,master=None,width=cwidth,height=cheight):
        self.master = master
        Frame.__init__(self, master)        
        self.instruction = StringVar()
                
        # make the canvas of a particular size
        self.circlesize=height/3.5
        self.canvaswidth = width
        self.canvasheight = height
        self.createCanvas()
        
    def createCanvas(self):
        # create the canvas for presenting the visual stimulus
        self.canvas = Canvas(self,width=self.canvaswidth,height=self.canvasheight)
        self.canvas.grid()
        x0 = (self.canvaswidth - self.circlesize)/2
        y0 = 0.5*self.circlesize
        x1 = x0 + self.circlesize
        y1 = y0 + self.circlesize
        self.canvas.create_oval(x0,y0,x1,y1,fill="gray",tags="redlight")
        
        y0 += 1.5*self.circlesize
        y1 += 1.5*self.circlesize
        self.canvas.create_oval(x0,y0,x1,y1,fill="gray",tags="greenlight")
        self.off()

    def waiting(self):
        # set stimulus to waiting by switching on red light
        self.canvas.itemconfig('greenlight',fill='gray')
        self.canvas.itemconfig('redlight',fill='red')
        self.instruction.set('Press the big button when the light turns green.')

    def testing(self):
        # set the stimulus to testing by switching on green light
        self.canvas.itemconfig('greenlight',fill='green')
        self.canvas.itemconfig('redlight',fill='gray')

        return 1
    
    def off(self):
        # set the stimulus to off by switching off both lights
        self.canvas.itemconfig('greenlight',fill='gray')
        self.canvas.itemconfig('redlight',fill='gray')
        self.instruction.set('Press the big button to start the test.')
        
class Decision(Frame):
    """A visual decision-requiring stimulus object that's also a frame. width and height set the size of the canvas on the frame. picdir is the directory where the picture files are stored"""
    def __init__(self,master=None,width=cwidth,height=cheight,picdir='.'):
        self.master = master
        Frame.__init__(self, master)        
        self.instruction = StringVar()
        
        # fraction of the time to show good picture
        self.fracgood = 0.5
        
        # make the canvas of a particular size
        self.canvaswidth = width
        self.canvasheight = height
        self.picdir = picdir
        [self.goodpics,self.badpics] = self.loadPics(picdir)
        if len(self.goodpics) == 0 or len(self.badpics) == 0:
            raise IOError("Was unable to find at least one good and one bad pic. %d %d" %(len(self.goodpics), len(self.badpics)))
        self.createCanvas()
        
    def createCanvas(self):
        # create the canvas for presenting the visual stimulus
        self.canvas = Canvas(self,width=self.canvaswidth,height=self.canvasheight)
        self.canvas.grid()
        
        self.circlesize = self.canvasheight/4
        x0 = (self.canvaswidth - self.circlesize)/2
        x1 = x0 + self.circlesize
        y0 = self.circlesize/4
        y1 = y0+self.circlesize
        self.canvas.create_oval(x0,y0,x1,y1,fill="gray",tags="redlight")

        # where the images will be centered
        self.imagecenter = [self.canvaswidth/2,(self.canvasheight + 1.5*self.circlesize)/2]
        self.off()
        
    def loadPics(self,picdir):
        """Return two lists of picture objects: the good and the bad pictures"""
        allfiles = [f for f in os.listdir(picdir) if os.path.splitext(f)[1] == '.gif']
        goodpics = []; badpics = []
        for f in allfiles:
            if 'cat' in os.path.splitext(f)[0]:
                goodpics.append(PhotoImage(file=os.path.join(picdir,f)))
            else:
                badpics.append(PhotoImage(file=os.path.join(picdir,f)))

        return [goodpics,badpics]
    
    def waiting(self):
        # set stimulus to waiting by switching on red light
        self.canvas.itemconfig('redlight',fill='red')
        self.instruction.set('Press the big button when you see a cat.')
        
    def testing(self):
        # set the stimulus to testing by presenting a picture
        # returns 1 if the picture was good, 0 otherwise
        
        self.canvas.itemconfig('redlight',fill='gray')

        # randomly select which picture to present
        r = random.random()
        if r < self.fracgood:
            pic = self.goodpics[random.randint(0,len(self.goodpics)-1)]
            good = 1
        else:
            pic = self.badpics[random.randint(0,len(self.badpics)-1)]
            good = 0
        
        self.canvas.create_image(self.imagecenter[0],self.imagecenter[1],image=pic,\
                                 anchor=CENTER,tags="image")

        return good
    
    def off(self):
        # set the stimulus to off by removing the picture
        self.canvas.delete("image")
        self.canvas.itemconfig('redlight',fill='gray')
        self.instruction.set('Press the big button to start the test.')
        
class Auditory(Frame):
    """An auditory stimulus object that's also a frame"""
    def __init__(self,master=None,width=cwidth,height=cheight):
        self.master = master
        Frame.__init__(self, master)
        self.instruction = StringVar()
        self.canvaswidth = width
        self.canvasheight = height
        self.circlesize = height/3.5
        self.createCanvas()        
        
    def createCanvas(self):
        # create the canvas for presenting the visual stimulus
        self.canvas = Canvas(self,width=self.canvaswidth,height=self.canvasheight)
        self.canvas.grid()

        # put in a single red light
        x0 = (self.canvaswidth - self.circlesize)/2
        y0 = (self.canvasheight - self.circlesize)/2
        x1 = x0 + self.circlesize
        y1 = y0 + self.circlesize
        handle = self.canvas.create_oval(x0,y0,x1,y1,fill="gray")
        self.canvas.itemconfig(handle,tags=('redlight'))

    def waiting(self):
        self.canvas.itemconfig('redlight',fill='red')
        self.instruction.set('Press the big button when you hear a beep.')
        
    def testing(self):
        #self.master.bell()
        #os.system("beep")
        p = subprocess.Popen("beep", shell=False)
        #sts = os.waitpid(p.pid, 0)[1]
        return 1
    
    def off(self):
        self.canvas.itemconfig('redlight',fill='gray')
        self.instruction.set('Press the big button to start the test.')
        
class ReactionTimer:
    """Class defining a reaction time timer"""
    def __init__(self):
        root = Tk()
        self.root = root
        root.title("Reaction Timer")
        
        # status of the stimulus
        # 0 means test hasn't started
        # 1 means it's waiting to present the stimulus
        # 2 means it has presented the stimulus and is waiting for a response
        self.status = 0

        # current type of test being run
        # 0 is visual
        # 1 is auditory
        self.testtype=0
        self.testvar = IntVar()
        self.testvar.set(self.testtype)

        self.lastbadtime = 0
        
        # list of recorded reaction times and the number of iterations
        # that were successfully recorded
        self.rxntimes = []
        self.itercount = 0
        self.badcount = 0 #number of bad clicks

        self.nrecord = 5
        self.timevars = [StringVar() for r in range(self.nrecord)]
        self.recfields = []
        self.reclabels = []
        self.avgvar = StringVar()
        self.avgtime = 0
        self.recframeheight = 1000

        self.bbtext = StringVar() # label on the big button
        self.bbtext.set('Start')
        
        self.setupFrames()

    def setupFrames(self):
        root = self.root

        # stimulus object, start with the visual one
        self.visstim = Visual(root,cwidth,cheight)
        self.audstim = Auditory(root,cwidth,cheight)
        self.decstim = Decision(root,cwidth,cheight,picdir)
        self.stim = self.visstim        
        self.stim.grid(row=3,column=2,rowspan=2)

        # set up the various frames involved
        # frame with choices for different tests
        self.choiceframe = self.makeChoiceFrame(root)
        self.choiceframe.grid(row=1,column=1,columnspan = 3,sticky='W',pady=5,padx=10)

        # put in the instructions bar
        self.instlabel = Label(textvar=self.stim.instruction)
        self.instlabel.grid(row=2,column=1,columnspan=3)
        
        # frame with the time records                
        self.recframe = self.makeRecFrame(root)
        self.recframe.grid(row=3,column=1,padx=10)
        
        #button to press        
        self.bigButton = Button(root,textvariable=self.bbtext,height=10,width=8,command=self.runTest)
        self.bigButton.grid(row=3,column=3,rowspan=2,padx=10)

        # quit and undo buttons
        self.buttonframe = self.makeButtonFrame(root)
        self.buttonframe.grid(row=4,column=1)

        self.clearbutton = Button(root,text = "Clear",command=self.reset)
        self.clearbutton.grid(row=4,column=3)
                              
    def makeButtonFrame(self,master):
        # make frame with the quit and undo buttons
        buttonframe = Frame(master)
        self.quitButton = Button(buttonframe,text="Quit",command=self.finish)
        self.quitButton.grid(row=1,column=1,padx=2)

        self.undoButton = Button(buttonframe,text="Undo",command=self.undo)
        self.undoButton.grid(row=1,column=2,padx=2)

        self.showavgButton = Button(buttonframe,text="Show Avg.",command=self.displayavg)
        self.showavgButton.grid(row=1,column=3,padx=2)

        return buttonframe
    
    def makeChoiceFrame(self,master):
        # make frame containing the test choice buttons
        choiceframe = Frame(master)
        choicelabel = Label(choiceframe,text="Type of test:")
        choicelabel.grid(row=0,column=1,pady=3)

        r1=Radiobutton(choiceframe,text="Visual",variable=self.testvar,value=0,indicatoron=0,padx=10,pady=5,command=self.setTestType)
        r2=Radiobutton(choiceframe,text="Auditory",variable=self.testvar,value=1,indicatoron=0,padx=10,pady=5,command=self.setTestType)
        r3=Radiobutton(choiceframe,text="Decision",variable=self.testvar,value=2,indicatoron=0,padx=10,pady=5,command=self.setTestType)

        r1.grid(row=0,column=2,padx=5)
        r2.grid(row=0,column=3,padx=5)
        r3.grid(row=0,column=4,padx=5)
        return choiceframe        

    def makeRecFrame(self,master):
        # make frame containing the timing records
        recframe = Frame(master,height=self.recframeheight)

        # fields for recording the reaction times
        for r in range(self.nrecord):
            obj = Label(recframe,width=10,textvariable=self.timevars[r])
            obj.grid(row=r,column=2,pady=5)
            self.recfields.append(obj)
            obj = Label(recframe,text="Time %d: " %(r+1))
            obj.grid(row=r,column=1)
            self.reclabels.append(obj)

        # show the average as well:
        self.avgframe = LabelFrame(recframe)
        self.avgframe.grid(row=self.nrecord,column=1,columnspan=2,pady=5)
        self.avglabel = Label(self.avgframe,text="Average: ")
        self.avglabel.grid(row=0,column=1)
        self.avgfield = Label(self.avgframe,width=10,textvariable=self.avgvar)
        self.avgfield.grid(row=0,column=2)
        
        return recframe

    def runTest(self):
        # run the actual test
        self.status = 1
        # set the stimulus to waiting
        self.stim.waiting()
        self.bbtext.set('End')
        self.bigButton.config(command=self.endTest)
        self.root.update()

        # set an alarm to wait a random time        
        waittime = minwaittime+random.random()*(maxwaittime-minwaittime)
        self.curalarm = self.root.after(int(waittime*1000),self.startTest)

    def startTest(self):
        if self.status == 1:
            # set the stimulus to testing
            good = self.stim.testing()
                
            self.root.update()
            if good:
                self.status = 2
            self.tstart = time.time()
            # if nothing happens for 10 seconds (or 2 seconds with a bad stimulus), then reset the test
            if good:
                self.runalarm = self.root.after(10000,self.reset)
            else:
                self.runalarm = self.root.after(2000,self.reset)
        
    def endTest(self):
        if self.status==2: #test is running
            tend = time.time()
            self.rxntimes.append(tend-self.tstart)
            # counter for where to print the result
            lblct = self.itercount%self.nrecord
            self.timevars[lblct].set('%5.3f' %self.rxntimes[-1])
            self.itercount += 1

            # set the average time based on the currently shown records
            tmp = 0; ntmp = 0
            for c in range(self.nrecord):
                timestr = self.timevars[c].get()
                if timestr != '':
                    ntmp += 1
                    tmp +=  float(timestr)

	    if ntmp == 0:
		self.avgtime = 0
		self.avgvar.set('')
	    else:
            	self.avgtime = tmp / ntmp
                if showavg:
                    self.avgvar.set('%5.3f' %self.avgtime)
                else:
                    self.avgvar.set('???')
        else:
            self.badcount += 1 #counts number of bad clicks
            #print "You clicked the button before the light turned green. This trial doesn't count."
            # cancel the waiting alarm
            self.root.after_cancel(self.curalarm)
            self.popupMessage()

        self.reset()        

    def reset(self):
        """Reset the reaction time test to the off state"""
        self.status = 0
        self.stim.off() # set the stimulus to the off state
        self.bbtext.set('Start')
        self.bigButton.config(command=self.runTest)
        self.root.update()
        try:
            self.root.after_cancel(self.runalarm)
        except AttributeError:
            pass

        try:
            self.root.after_cancel(self.curalarm)
        except AttributeError:
            pass
        
    def setTestType(self):
        # set the type of the test and change the stimulus appropriately

        if self.testvar.get() == self.testtype:
            return
        
        self.stim.grid_remove()        
        
        self.testtype = self.testvar.get()
        if self.testtype == 0:
            self.stim = self.visstim
        elif self.testtype == 1:
            self.stim = self.audstim
        elif self.testtype == 2:
            self.stim = self.decstim
        else:
            print "Unknown test type! Must be 0, 1, or 2"

        # erase various records
        self.rxntimes = []
        self.itercount = 0
        self.badcount = 0 #number of bad clicks
        for r in range(self.nrecord):
            self.timevars[r].set('')
        self.avgvar.set('')

        # stop any currently running test                
        self.instlabel.config(textvar=self.stim.instruction)
        self.stim.grid(row=3,column=2,rowspan=2)
        self.reset()
        
    def popupMessage(self):
        """Pop up a message box with the message of the given index"""
        if self.testtype == 0:
            message = 'You clicked the button before the light turned green. This trial does not count.'
        elif self.testtype == 1:
             message = 'You clicked the button before the beep sounded. This trial does not count.'
        elif self.testtype == 2:
             message = 'You clicked the button before a cat picture was shown. This trial does not count.'    
        else:
            raise ValueError("Error in popupMessage: test type must be 0 or 1")
        
        mb = MessageBox(self.root,message,'Too early!')
        self.root.wait_window(mb)

    def displayavg(self):
        self.avgvar.set("%5.3f" %self.avgtime)
        self.recframe.update()
        return 0

    def undo(self):
        # undo the last reaction time measurement
        self.rxntimes = self.rxntimes[:-1]
        # counter for where the result was printed
        self.itercount -= 1
        lblct = self.itercount%self.nrecord

        self.timevars[lblct].set('')

        if self.itercount < 0:
            self.itercount = 0

        if self.itercount == 0:
            self.avgvar.set('')
            self.avgtime = 0
        else:
            tmp = 0; ntmp = 0
            for c in range(self.nrecord):
                timestr = self.timevars[c].get()
                if timestr != '':
                    tmp +=  float(timestr)
                    ntmp += 1
            self.avgtime = tmp / ntmp
                
            self.avgvar.set('%5.3f' %self.avgtime)

        self.recframe.update()
    def finish(self):
        # end all the tests
        sys.exit()

class MessageBox(Toplevel):
    """Class defining a dialog box that pops up with a message to the user."""
    def __init__(self,parent,message="",title=None):        
        Toplevel.__init__(self, parent)
        if title:
            self.title(title)
        self.parent = parent

        self.message = message
        body = Frame(self)
        self.initial_focus = self.body(body)
        body.grid()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus=self
        
        self.makeButtons(body)

        self.protocol("WM_DELETE_WINDOW", self.close)

        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))
        
    def body(self,master):
        """The body of the message box. Returns the widget that should have initial focus"""
        self.message = Message(self,text=self.message,width=200)
        self.message.grid(row=0,column=0,padx=10,pady=5)        

    def makeButtons(self,master):
        """Make the button for the dialog box"""
        self.okButton = Button(master,text='OK',command=self.close)
        self.okButton.grid(row=1,column=0,pady=5)
        self.bind("<Return>", self.close)
        
    def close(self,event=None):
        """Close the message box"""
        self.destroy()
        
        
rt = ReactionTimer()
rt.root.mainloop()
