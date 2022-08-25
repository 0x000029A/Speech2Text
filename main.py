from tkinter import ttk
from tkinter import filedialog
from tkinter import *
import speech_recognition as sr
import arabic_reshaper
from os import path
import os
from fpdf import FPDF
from bidi.algorithm import get_display
from datetime import datetime, date
import threading
from pydub import AudioSegment


def start_processing():
    voice_type = filename[len(filename)-3:len(filename)]
    if voice_type != "wav":
        wav_audio = AudioSegment.from_file(filename, format=voice_type, frame_rate=44100,
                                           channels=2, sample_width=2)
        wav_audio.export("6Sk2AJ.wav", format="wav")
        AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), os.getcwd() + r"\\6Sk2AJ.wav")
    else:
        AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), filename)
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)

    raw_sound = r.recognize_google(audio, language=gglang_radio)
    pdf = FPDF()
    pdf.add_page()

    if gglang_radio == "en-US":
        pdf.set_font('Arial', '', 10)
        header = "Processed on {} at: {}\nLanguage: English".format(date.today(), datetime.now().strftime("%H:%M:%S"))
        pdf.cell(0, 10, header, 'L')
        pdf.ln(10)
        pdf.multi_cell(0, 10, txt=raw_sound, align='L')

    elif gglang_radio == "ar-EG":
        pdf.add_font('Times', '', r"c:\WINDOWS\Fonts\Times.ttf", uni=True)
        pdf.set_font('Times', '', 10)
        araw_sound = arabic_reshaper.reshape(raw_sound)
        bidi_text = get_display(araw_sound, upper_is_rtl=True, base_dir="R")
        header = "Processed on {} at: {}\nLanguage: Arabic".format(date.today(), datetime.now().strftime("%H:%M:%S"))
        pdf.cell(0, 10, header, 'L')
        pdf.ln(10)
        for i in range(0, len(bidi_text), 50):
            if len(bidi_text) - (i + 50) < 0:
                pdf.cell(0, 10, bidi_text[0:len(bidi_text) - i], 'C')
                pdf.ln(10)
                break
            pdf.cell(0, 10, bidi_text[len(bidi_text) - (i + 50):len(bidi_text) - i], 'C')
            pdf.ln(10)
    pdf.output(foldername + "/" + output_filename.get() + ".pdf")
    comp_msg = Message(T2S, text="Processing Completed! Check the file now!", font="Arial, 12")
    comp_msg.config(bg='lightgreen')
    comp_msg.grid(column=1, row=10)
    pb.destroy()
    if voice_type != "wav":
        os.remove("6Sk2AJ.wav")


def start_pb():
    pb.start(10)


def browse_voice_file():
    global filename
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetypes=(("WAV", "*.wav*"), ("MP3", "*.mp3*"),
                                                     ("M4A", "*.m4a*"), ("OGG", "*.ogg*"),
                                                     ("all files", "*.*")))
    notifi_label = Message(T2S, text="File opened! Its path:\n" + filename, font="Arial, 12")
    notifi_label.config(bg='lightgreen', width=250)
    notifi_label.grid(column=0, row=7, columnspan=4)


def browse_output_folder():
    global foldername
    foldername = filedialog.askdirectory(initialdir="/", title="Select a folder")
    notifi_label = Message(T2S, text="The output folder is:\n" + foldername, font="Arial, 12")
    notifi_label.config(bg='lightgreen', width=250)
    notifi_label.grid(column=0, row=8, columnspan=4)



def Main0():
    global gglang_radio
    glang_radio = lang_radio.get()
    if glang_radio == 1:
        gglang_radio = "ar-EG"
    elif glang_radio == 2:
        gglang_radio = "en-US"
    pb.grid(column=0, row=9, columnspan=4)
    t1.start()
    t2.start()


T2S = Tk()
T2S.title("Speech2Text")
T2S.geometry('500x700')
T2S['bg'] = '#FFFFFF'
pb = ttk.Progressbar(
    T2S,
    orient='horizontal',
    mode='indeterminate',
    length=180
)

# Threading
t1 = threading.Thread(target=start_pb)
t2 = threading.Thread(target=start_processing)
#####

# Header
header_text = Message(T2S, text="Welcome to Text2Speech program!\n\nThe program aims to help people to convert audio" +
                                " files to text (PDF) using Google Speech API\n\n" +
                                "Select a file, and the audio language, and hit start", font="Arial, 15", justify=CENTER)
header_text.grid(column=0, row=0, ipadx=100, columnspan=4, pady=20)
header_text.config(width=300)
#####

# Audio file selecting
browse_text = Message(T2S, text="Select an audio file:", font="Arial, 12")
browse_text.grid(column=0, row=1)
browse_text.config(width=125, bg="White")

browse_button = Button(T2S, text="Browse Files", command=browse_voice_file)
browse_button.grid(column=1, row=1)
#######

# Language selecting
browse_text = Message(T2S, text="Select the language spoken", font="Arial, 12")
browse_text.grid(column=0, row=2)
browse_text.config(width=125, bg="White")

lang_radio = IntVar()
Radiobutton(T2S, text='Arabic', variable=lang_radio, value=1).grid(column=1, row=2)
Radiobutton(T2S, text='English', variable=lang_radio, value=2).grid(column=2, row=2)
######

# Output location
browse_text = Message(T2S, text="Select the output location:", font="Arial, 12")
browse_text.grid(column=0, row=3)
browse_text.config(width=125, bg="White")

browse_button = Button(T2S, text="Browse Folders", command=browse_output_folder)
browse_button.grid(column=1, row=3)
###########

# Output file name
browse_text = Message(T2S, text="Enter the output file name", font="Arial, 12")
browse_text.grid(column=0, row=5)
browse_text.config(width=125, bg="White")

output_filename = StringVar(T2S)
Entry(T2S, textvariable=output_filename).grid(column=1, row=5)
#######

# Start button
Button(T2S, text="Start", padx=10, pady=5, command=Main0).grid(column=1, row=6)
T2S.mainloop()
