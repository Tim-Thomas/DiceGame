from tkinter import *
import tkinter.messagebox
import random
from Die import *

bgColor = "DarkGreen"

class Yahtzee:

    def __init__(self, master):
        self.master = master
        self.holds = [0,0,0,0,0]
        
        self.dice=[Die(), Die(), Die(), Die(), Die()]
        self.diceNumbers = [0,0,0,0,0]

        self.nRollsRemain = 4
        self.InitUI(master)
        self.rollDice()

    def InitUI(self, master):
        ##This is necessary for making Tkinter and IDLE play nice
        master.protocol("WM_DELETE_WINDOW", master.destroy)

        ##Setting up the menu bar. New Game and Exit go here
        menubar = Menu(master)

        gamemenu = Menu(menubar, tearoff=0)
        gamemenu.add_command(label="New Game", command= lambda:self.resetBoard())
        gamemenu.add_separator()
        gamemenu.add_command(label="Exit", command = master.destroy)
        menubar.add_cascade(label="Game", menu=gamemenu)

        master.config(menu=menubar)

        ##Laying out the frames for tkinter
        self.main_container = Frame(master,bg=bgColor)
        self.main_container.grid(row=0,column=0,sticky="nsew")
        master.grid_rowconfigure(0,weight=1)
        master.grid_columnconfigure(0,weight=1)

        self.top_frame=Frame(self.main_container,bg=bgColor)
        self.bottom_middle_frame=Frame(self.main_container,bg=bgColor)
        self.bottom_left_frame=Frame(self.main_container,bg=bgColor)
        self.bottom_right_frame=Frame(self.main_container,bg=bgColor)

        self.top_frame.grid(row=0,column=0,pady=10,columnspan=3)
        self.bottom_middle_frame.grid(row=1,column=1,sticky="ns",pady=10)
        self.bottom_left_frame.grid(row=1,column=0,sticky="nsew")
        self.bottom_right_frame.grid(row=1,column=2,sticky="nsew")
        
        self.main_container.grid_rowconfigure(1,weight=1)
        self.main_container.grid_columnconfigure(0,weight=1)
        self.main_container.grid_columnconfigure(1,weight=3)
        self.main_container.grid_columnconfigure(2,weight=1)

        ## The five dice
        diceRow = 0
        self.d1Label = Label(self.top_frame, image = images[self.diceNumbers[0]], relief = "sunken")
        self.d1Label.grid(row=diceRow,column=0,padx=5,pady=10)

        self.d2Label = Label(self.top_frame, image = images[self.diceNumbers[1]], relief = "sunken")
        self.d2Label.grid(row=diceRow,column=1,padx=5)

        self.d3Label = Label(self.top_frame, image = images[self.diceNumbers[2]], relief = "sunken")
        self.d3Label.grid(row=diceRow,column=2,padx=5)

        self.d4Label = Label(self.top_frame, image = images[self.diceNumbers[3]], relief = "sunken")
        self.d4Label.grid(row=diceRow,column=3,padx=5)

        self.d5Label = Label(self.top_frame, image = images[self.diceNumbers[4]], relief = "sunken")
        self.d5Label.grid(row=diceRow,column=4,padx=5)

        self.dieElements = [self.d1Label,self.d2Label,self.d3Label,self.d4Label,self.d5Label]

        ## The hold buttons
        holdRow = 1
        self.h1Button = Button(self.top_frame, text="Hold", command= lambda: self.updateHolds(0), state=DISABLED)
        self.h1Button.grid(row=holdRow, column = 0)

        self.h2Button = Button(self.top_frame, text="Hold", command= lambda: self.updateHolds(1), state=DISABLED)
        self.h2Button.grid(row=holdRow, column = 1)

        self.h3Button = Button(self.top_frame, text="Hold", command= lambda: self.updateHolds(2), state=DISABLED)
        self.h3Button.grid(row=holdRow, column = 2)

        self.h4Button = Button(self.top_frame, text="Hold", command= lambda: self.updateHolds(3), state=DISABLED)
        self.h4Button.grid(row=holdRow, column = 3)

        self.h5Button = Button(self.top_frame, text="Hold", command= lambda: self.updateHolds(4), state=DISABLED)
        self.h5Button.grid(row=holdRow, column = 4)

        self.holdElements = [self.h1Button,self.h2Button,self.h3Button,self.h4Button,self.h5Button]

        ## Roll Button and Rolls Remaining Text

        self.rollText = StringVar()

        self.rollLabel = Label(self.top_frame, textvariable = self.rollText, bg = bgColor,font=("Helvetica", 10),anchor=CENTER, fg="White")
        self.rollLabel.grid(row=2,column=1,columnspan=3,pady=3)

        self.rollButton = Button(self.top_frame, text="Roll the dice!", font=14, command = self.rollDice)
        self.rollButton.grid(row=3,column=1,padx=20,columnspan=3)

        ## Top Buttons

        self.oneButton = Button(self.bottom_middle_frame, text="Ones (Total 1s)", command = lambda: self.score(self.oneButton, self.oneText, self.oneLabel, "top"),width=30)
        self.oneButton.grid(row = 0, column=0,sticky="EW",pady=1)

        self.twoButton = Button(self.bottom_middle_frame, text="Twos (Total 2s)", command = lambda: self.score(self.twoButton, self.twoText, self.twoLabel, "top"))
        self.twoButton.grid(row = 1, column=0,sticky="EW",pady=1)

        self.threeButton = Button(self.bottom_middle_frame, text="Threes (Total 3s)", command = lambda: self.score(self.threeButton, self.threeText, self.threeLabel, "top"))
        self.threeButton.grid(row = 2, column=0,sticky="EW",pady=1)

        self.fourButton = Button(self.bottom_middle_frame, text="Fours (Total 4s)", command = lambda: self.score(self.fourButton, self.fourText, self.fourLabel, "top"))
        self.fourButton.grid(row = 3, column=0,sticky="EW",pady=1)

        self.fiveButton = Button(self.bottom_middle_frame, text="Fives (Total 5s)", command = lambda: self.score(self.fiveButton, self.fiveText, self.fiveLabel, "top"))
        self.fiveButton.grid(row = 4, column=0,sticky="EW",pady=1)

        self.sixButton = Button(self.bottom_middle_frame, text="Sixes (Total 6s)", command = lambda: self.score(self.sixButton, self.sixText, self.sixLabel, "top"))
        self.sixButton.grid(row = 5, column=0,sticky="EW",pady=1)

        ## Bottom Buttons

        self.ToaKButton = Button(self.bottom_middle_frame, text="Three of a Kind (Die Total)", command = lambda:self.score(self.ToaKButton, self.ToaKText, self.ToaKLabel, "bottom"))
        self.ToaKButton.grid(row=8,column=0, sticky="EW",pady=1)

        self.FoaKButton = Button(self.bottom_middle_frame, text="Four of a Kind (Die Total)", command = lambda:self.score(self.FoaKButton, self.FoaKText, self.FoaKLabel, "bottom"))
        self.FoaKButton.grid(row=9,column=0, sticky="EW",pady=1)

        self.FHButton = Button(self.bottom_middle_frame, text="Full House (25 Points)", command = lambda:self.score(self.FHButton, self.FHText, self.FHLabel, "bottom"))
        self.FHButton.grid(row=10,column=0, sticky="EW", pady=1)

        self.smallStraightButton = Button(self.bottom_middle_frame, text="Small Straight (30 Points)", command = lambda:self.score(self.smallStraightButton, self.smallStraightText, self.smallStraightLabel, "bottom"))
        self.smallStraightButton.grid(row=11, column=0, sticky="EW", pady=1)

        self.largeStraightButton = Button(self.bottom_middle_frame, text="Large Straight (40 Points)", command = lambda:self.score(self.largeStraightButton, self.largeStraightText, self.largeStraightLabel, "bottom"))
        self.largeStraightButton.grid(row=12, column=0, sticky="EW", pady=1)

        self.YahtzeeButton = Button(self.bottom_middle_frame, text="Yahtzee! (50 Points)", command = lambda:self.score(self.YahtzeeButton, self.YahtzeeText, self.YahtzeeLabel, "bottom"))
        self.YahtzeeButton.grid(row=13, column=0, sticky="EW", pady=1)

        self.chanceButton = Button(self.bottom_middle_frame, text="Chance (Die Total)", command = lambda:self.score(self.chanceButton, self.chanceText, self.chanceLabel, "bottom"))
        self.chanceButton.grid(row=14, column=0, sticky="EW", pady=1)

        ## Top Text

        self.upperTotalLabel = Label(self.bottom_middle_frame, text = "Upper Scored Total:",anchor=NE, bg=bgColor, font="bold")
        self.upperTotalLabel.grid(row=6, column=0,pady=1,sticky="NEW")

        self.upperBonusLabel = Label(self.bottom_middle_frame, text = "Bonus:",anchor=E, bg=bgColor, font="bold")
        self.upperBonusLabel.grid(row=7, column=0,pady=1,sticky="NEW")

        ## Bottom Text
        self.lowerTotalLabel = Label(self.bottom_middle_frame, text = "Lower Scored Total:",anchor=E, bg=bgColor, font="bold")
        self.lowerTotalLabel.grid(row=15, column=0,pady=1,sticky="EW")

        self.yahtzeeBonusLabel = Label(self.bottom_middle_frame, text= "Yahtzee Bonus:", anchor=E, bg=bgColor, font="bold")
        self.yahtzeeBonusLabel.grid(row=16, column=0, pady=1, sticky="EW")

        self.upperBonusLabel = Label(self.bottom_middle_frame, text = "Grand Total:",anchor=E, bg=bgColor, font="bold")
        self.upperBonusLabel.grid(row=18, column=0,pady=10,sticky="EW")

        ## Top Score Boxes

        self.oneText = StringVar()
        self.oneLabel = Label(self.bottom_middle_frame, textvariable = self.oneText, bg="beige",width=10,relief="sunken", fg="red")
        self.oneLabel.grid(row=0,column=1, padx=5,sticky="EW")

        self.twoText = StringVar()
        self.twoLabel = Label(self.bottom_middle_frame, textvariable=self.twoText, bg="beige",width=10,relief="sunken", fg="red")
        self.twoLabel.grid(row=1,column=1, padx=5,sticky="EW")

        self.threeText = StringVar()
        self.threeLabel = Label(self.bottom_middle_frame, textvariable=self.threeText, bg="beige",width=10,relief="sunken", fg="red")
        self.threeLabel.grid(row=2,column=1, padx=5,sticky="EW")

        self.fourText = StringVar()
        self.fourLabel = Label(self.bottom_middle_frame, textvariable=self.fourText, bg="beige",width=10,relief="sunken", fg="red")
        self.fourLabel.grid(row=3,column=1, padx=5,sticky="EW")

        self.fiveText = StringVar()
        self.fiveLabel = Label(self.bottom_middle_frame, textvariable=self.fiveText, bg="beige",width=10,relief="sunken", fg="red")
        self.fiveLabel.grid(row=4,column=1, padx=5,sticky="EW")

        self.sixText = StringVar()
        self.sixLabel = Label(self.bottom_middle_frame, textvariable=self.sixText,bg="beige",width=10,relief="sunken", fg="red")
        self.sixLabel.grid(row=5,column=1, padx=5,sticky="EW")

        self.upperTotalText = StringVar()
        self.upperTotalText.set(0)
        self.upperTotalLabel = Label(self.bottom_middle_frame, textvariable=self.upperTotalText,width=10,relief="sunken", bg="beige")
        self.upperTotalLabel.grid(row=6,column=1, padx=5, sticky="EW")

        self.upperBonusText = StringVar()
        self.upperBonusText.set(0)
        self.upperBonusLabel = Label(self.bottom_middle_frame, textvariable=self.upperBonusText,width=10,relief="sunken",bg="beige")
        self.upperBonusLabel.grid(row=7,column=1, padx=5, sticky="EW")

        ##Bottom Score Boxes
        
        self.ToaKText = StringVar()
        self.ToaKLabel = Label(self.bottom_middle_frame, textvariable=self.ToaKText, width=10, relief="sunken", bg="beige", fg="red")
        self.ToaKLabel.grid(row=8, column=1, padx=5, sticky="EW")

        self.FoaKText = StringVar()
        self.FoaKLabel = Label(self.bottom_middle_frame, textvariable=self.FoaKText, width=10, relief="sunken", bg="beige", fg="red")
        self.FoaKLabel.grid(row=9, column=1, padx=5, sticky="EW")

        self.FHText = StringVar()
        self.FHLabel = Label(self.bottom_middle_frame, textvariable=self.FHText, width=10, relief="sunken", bg="beige", fg="red")
        self.FHLabel.grid(row=10, column=1, padx=5, sticky="EW")

        self.smallStraightText = StringVar()
        self.smallStraightLabel = Label(self.bottom_middle_frame, textvariable=self.smallStraightText, width=10, relief="sunken", bg="beige", fg="red")
        self.smallStraightLabel.grid(row=11, column=1, padx=5, sticky="EW")

        self.largeStraightText = StringVar()
        self.largeStraightLabel = Label(self.bottom_middle_frame, textvariable=self.largeStraightText, width=10, relief="sunken", bg="beige", fg="red")
        self.largeStraightLabel.grid(row=12, column=1, padx=5, sticky="EW")

        self.YahtzeeText = StringVar()
        self.YahtzeeLabel = Label(self.bottom_middle_frame, textvariable=self.YahtzeeText, width=10, relief="sunken", bg="beige", fg="red")
        self.YahtzeeLabel.grid(row=13, column=1, padx=5, sticky="EW")

        self.chanceText = StringVar()
        self.chanceLabel = Label(self.bottom_middle_frame, textvariable=self.chanceText, width=10, relief="sunken", bg="beige", fg="red")
        self.chanceLabel.grid(row=14, column=1, padx=5, sticky="EW")

        self.YahtzeeBonusText = StringVar()
        self.YahtzeeBonusText.set(0)
        self.YahtzeeBonusLabel = Label(self.bottom_middle_frame, textvariable=self.YahtzeeBonusText, width=10, relief="sunken", bg="beige")
        self.YahtzeeBonusLabel.grid(row=16, column=1, padx=5, sticky="EW")

        ## Botttom Total Boxes
        self.lowerTotalText = StringVar()
        self.lowerTotalText.set(0)
        self.lowerTotalLabel = Label(self.bottom_middle_frame, textvariable=self.lowerTotalText,width=10,relief="sunken",bg="beige")
        self.lowerTotalLabel.grid(row=15,column=1, padx=5, sticky="EW")

        self.grandTotalText = StringVar()
        self.grandTotalText.set(0)
        self.grandTotalLabel = Label(self.bottom_middle_frame,textvariable=self.grandTotalText,width=10,relief="sunken",bg="beige")
        self.grandTotalLabel.grid(row=18,column=1, padx=5, pady=15,sticky="EW")

        ## A list of tuples of everything about a line
        self.lines = [(self.oneButton,self.oneText,self.oneLabel,scoreAces),(self.twoButton,self.twoText,self.twoLabel,score2s),(self.threeButton,self.threeText,self.threeLabel,score3s),(self.fourButton,self.fourText,self.fourLabel,score4s),(self.fiveButton,self.fiveText,self.fiveLabel,score5s),(self.sixButton,self.sixText,self.sixLabel,score6s),(self.ToaKButton,self.ToaKText,self.ToaKLabel,score3OfaKind),(self.FoaKButton,self.FoaKText,self.FoaKLabel,score4OfaKind),(self.FHButton,self.FHText,self.FHLabel,scoreFullHouse),(self.smallStraightButton,self.smallStraightText, self.smallStraightLabel, scoreSmallStraight),(self.largeStraightButton,self.largeStraightText,self.largeStraightLabel,scoreLargeStraight),(self.YahtzeeButton,self.YahtzeeText,self.YahtzeeLabel,scoreYahtzee),(self.chanceButton,self.chanceText,self.chanceLabel,scoreChance)]

        ## Lists of items getting summed into the "total" boxes
        self.topScoredTexts = []
        self.bottomScoredTexts = []

    def resetBoard(self):
        self.__init__(self.master)

    ## This and Score do the bulk of the work
    def rollDice(self):
        self.nRollsRemain -= 1
        ## 3 is a magic number that means the game should be in the "?????" state
        if self.nRollsRemain == 3:
            self.diceNumbers = [0,0,0,0,0]
        else:
        ##Roll the dice that aren't being held
            for i in range(0,5):
                if not self.holds[i]:
                    self.dice[i].roll()
            for i,each in enumerate(self.dice):
                self.diceNumbers[i] = self.dice[i].getValue()

        ##update die images
        for i,each in enumerate(self.dieElements):
            each.configure(image = images[self.diceNumbers[i]])

        ##update score values
        for each in self.lines:
            if not each[2].cget('foreground')=="BLACK":
                if self.nRollsRemain == 3:
                    each[1].set("")
                    each[0].config(state=DISABLED)
                else:
                    each[0].config(state=NORMAL)
                    each[1].set(each[3](self.diceNumbers))

        ##count rolls and update the text above the roll button
        if self.nRollsRemain == 0:
            self.rollText.set("Click a category to score it")
            self.rollButton.config(relief="sunken",state=DISABLED)
            for each in self.holdElements:
                each.config(state=DISABLED)
        elif self.nRollsRemain == 3:
            self.rollText.set("")
        else:
            self.rollText.set("Rolls Remaining: " + str(self.nRollsRemain))
            for each in self.holdElements:
                each.config(state=NORMAL)

    def updateHolds(self, toggle=-1):
        ##if an argument was passed, flip the value of that element
        if not toggle == -1:
            self.holds[toggle] = not self.holds[toggle]
        for i,each in enumerate(self.holds):
            if each == TRUE:
                self.holdElements[i].config(relief="solid")
                self.dieElements[i].config(relief="solid")
            else:
                self.holdElements[i].config(relief="raised")
                self.dieElements[i].config(relief="sunken")

    ## This is called every time any button is pushed other than Hold or Roll
    def score(self, whichButton, whichText, whichLabel, whichHalf):
        if whichHalf == "top":
            self.topScoredTexts.append(int(whichText.get()))
        else:
            self.bottomScoredTexts.append(int(whichText.get()))
        
        self.upperTotalText.set(sum(self.topScoredTexts))

        ## Check for top bonus condition
        if int(self.upperTotalText.get()) >= 63:
            self.upperBonusText.set(35)

        self.lowerTotalText.set(sum(self.bottomScoredTexts))

        ## Yahtzee Bonus test. No Jokers, though.
        if self.YahtzeeButton.cget('state') == "disabled" and self.YahtzeeText.get() == "50" and scoreYahtzee(self.diceNumbers) == 50:
            self.YahtzeeBonusText.set(int(self.YahtzeeBonusText.get())+100)

        ## Sum up bonuses + top and bottom totals for grand total
        self.grandTotalText.set(int(self.upperTotalText.get()) + int(self.lowerTotalText.get()) + int(self.upperBonusText.get()) + int(self.YahtzeeBonusText.get()))

        ## Set the button that was pushed so that you can't score it twice
        whichButton.config(relief="sunken", state=DISABLED)
        whichLabel.config(fg="BLACK")

        self.rollButton.config(relief="raised",state=NORMAL)
        ## If we've scored everything, prompt the user to start over or exit
        if len(self.lines) == len(self.topScoredTexts)+len(self.bottomScoredTexts):
            if tkinter.messagebox.askyesno("Game Over", "Final Score: " + self.grandTotalText.get() + "\nPlay Again?"):
                self.resetBoard()
            else:
                self.master.destroy()
                sys.exit(1)
        ## Get ready to go again
        self.holds = [0,0,0,0,0]
        self.updateHolds()
        for each in self.holdElements:
                each.config(state=DISABLED)
        self.nRollsRemain = 4
        self.rollDice()

root = Tk()

#loading the die images
images = [PhotoImage(file=str(x)+".gif") for x in range(0,7)]

root.wm_title("Yahtzee!")
ThisGame = Yahtzee(root)

root.mainloop()
