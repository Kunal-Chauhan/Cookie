import pyttsx3  # text to speech
import datetime
import speech_recognition as sr
import random
import wikipedia
import webbrowser
import os
import shutil

from datetime import date

engine = pyttsx3.init('sapi5')  # sapi5 = speech API, ,helps in recognition
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

format_dict = {"word": ".docx", "powerpoint": ".pptx", "music": ".mp3", "text": ".txt", "python file": ".py",
               "jupiter notebook": ".ipynb", "portable document": ".pdf", "pdf": ".pdf", "image": ".jpg", "executable": ".exe", "application": ".exe", "video": "mp4"}
folder_dict = {"documents": "C:\\Users\\rismv\\OneDrive\\Documents\\", "downloads": "C:\\Users\\rismv\\Downloads\\", "pictures": "C:\\Users\\rismv\\OneDrive\\Pictures\\", "desktop": "C:\\Users\\rismv\\OneDrive\\Desktop\\",
               "Documents": "C:\\Users\\rismv\\OneDrive\\Documents\\", "Downloads": "C:\\Users\\rismv\\Downloads\\", "Pictures": "C:\\Users\\rismv\\OneDrive\\Pictures\\", "Desktop": "C:\\Users\\rismv\\OneDrive\\Desktop\\", "document": "C:\\Users\\rismv\\OneDrive\\Documents\\", "download": "C:\\Users\\rismv\\Downloads\\", "picture": "C:\\Users\\rismv\\OneDrive\\Pictures\\",
               "Document": "C:\\Users\\rismv\\OneDrive\\Documents\\", "Download": "C:\\Users\\rismv\\Downloads\\", "Picture": "C:\\Users\\rismv\\OneDrive\\Pictures\\"}


class assistant:

    def speak(self, audio):
        engine.say(audio)
        engine.runAndWait()  # to make the speech audible

    def wish(self):
        # will give the current hour 1-24
        hour = int(datetime.datetime.now().hour)
        if hour >= 0 and hour < 12:
            self.speak("Good Morning!")
        elif hour >= 12 and hour < 18:
            self.speak("Good Afternoon!")
        else:
            self.speak("Good Evening!")

        self.speak(" How may I assist you?")

    def takeAudio(self):
        r = sr.Recognizer()  # initialising the recogniser
        with sr.Microphone() as source:  # using mic as source
            print("Listening...")
            r.adjust_for_ambient_noise(source, duration=1)
            r.pause_threshold = 1  # it will start recognising if no voice input is given for 1 sec
            audio = r.listen(source)

        try:  # if no error in recognising
            print("recognising...")
            query = r.recognize_google(audio, language='en-in')
            print(f"You said : {query}\n")
        except Exception as e:  # if error occurs, it will print line 42
            print("Pardon me, please say that again")
            return "None"
        return query

    def wakeWord(self, audio):
        WAKE_WORDS = ['hey cookie', 'hello cookie']
        audio = audio.lower()
        for phrase in WAKE_WORDS:
            if phrase in audio:
                return True
        return False

    def greeting(self, audio):
        # Greeting Inputs
        GREETING_INPUTS = ['hi', 'hey', 'hola', 'greetings', 'wassup', 'hello']

        # Greeting Response back to the user
        GREETING_RESPONSES = ['whats good', 'hello',
                              'hey there', 'hi', 'hey', 'hola']

        for word in audio.split():  # removing the silence in audio input
            if word.lower() in GREETING_INPUTS:
                return random.choice(GREETING_RESPONSES) + '.'
        return ''

    def assistantResponse(self, audio):
        print(audio)
        # Convert the text to speech
        self.speak(audio)

    def image_resize(self, y):
        from PIL import Image
        image = Image.open("stored_images\\"+y+".jpg")
        new_image = image.resize((32, 32))
        new_image.save("stored_images\\"+y+".jpg")

        print(image.size)
        print(new_image.size)

    def classify(self, y):
        import cv2 as cv
        import matplotlib.pyplot as plt
        import numpy as np
        from tensorflow.keras import datasets, layers, models
        (training_images, training_labels), (testing_images,
                                             testing_labels) = datasets.cifar10.load_data()
        training_images, testing_images = training_images/255, testing_images/255

        class_names = ['Plane', 'Car', 'Bird', 'Cat',
                       'Deer', 'Dog', 'Frog', 'Horse', 'Ship', 'Truck']

        """for i in range(16):
                plt.subplot(4, 4, i + 1)
                plt.xticks([])
                plt.yticks([])
                plt.imshow(training_images[i], cmap=plt.cm.binary)
                plt.xlabel(class_name[training_labels[i][0]])

            plt.show()
            """
        training_images = training_images[:20000]
        training_labels = training_labels[:20000]
        testing_images = testing_images[:4000]
        testing_labels = testing_labels[:4000]

        """model = models.Sequential()
            model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)))
            model.add(layers.MaxPooling2D((2, 2)))
            model.add(layers.Conv2D(64, (3, 3), activation='relu'))
            model.add(layers.MaxPooling2D((2, 2)))
            model.add(layers.Conv2D(64, (3, 3), activation='relu'))
            model.add(layers.Flatten())
            model.add(layers.Dense(64, activation='relu'))
            model.add(layers.Dense(10, activation='softmax'))

            model.compile(optimizer='adam',
                        loss='sparse_categorical_crossentropy', metrics=['accuracy'])

            model.fit(training_images, training_labels, epochs=10,
                    validation_data=(testing_images, testing_labels))

            loss, accuracy = model.evaluate(testing_images, testing_labels)
            print(f"Loss: {loss}")
            print(f"Accuracy: {accuracy}")

            model.save('image_classifier.model')
            """
        model = models.load_model('image_classifier.model')

        self.image_resize(y)
        img = cv.imread("stored_images\\"+y+".jpg")
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

        plt.imshow(img, cmap=plt.cm.binary)
        prediction = model.predict(np.array([img])/255)
        index = np.argmax(prediction)
        print(f'Prediction is {class_names[index]}')
        self.speak(f'Prediction is {class_names[index]}')
        plt.show()

    def main(self):
        audio = self.takeAudio()
        response = ''
        if (self.wakeWord(audio) == True):
            # Check for greetings by the user
            response = response + self.greeting(audio)
            self.assistantResponse(response)

        self.wish()
        while True:

            # Checking for the wake word/phrase
            query = self.takeAudio().lower()

            if 'open youtube' in query:
                webbrowser.open("youtube.com")

            elif 'open google' in query:
                webbrowser.open("google.com")

            elif 'open stack overflow' in query:
                webbrowser.open("stackoverflow.com")

            elif 'open github' in query:
                webbrowser.open("github.com")

            elif 'open vs code' in query:
                path = "C:\\Users\\rismv\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
                os.startfile(path)

            elif 'play music' in query:
                music_dir = 'C:\\Users\\rismv\\Music'
                songs = os.listdir(music_dir)
                s = random.choice(songs)
                os.startfile(os.path.join(music_dir, s))

            elif 'downloads' in query:
                self.speak("What would you like to open?")
                x = self.takeAudio()
                self.speak("What's the format of your file?")
                y = self.takeAudio().lower()
                f = format_dict[y]
                try:
                    path = "C:\\Users\\rismv\\Downloads\\"+x+f
                    os.startfile(path)
                except:
                    path = "C:\\Users\\rismv\\Downloads\\"+x.capitalize()+f
                    os.startfile(path)

            elif 'documents' in query:
                self.speak("What would you like to open?")
                x = self.takeAudio()
                self.speak("What's the format of your file?")
                y = self.takeAudio().lower()
                f = format_dict[y]
                try:
                    path = "C:\\Users\\rismv\\OneDrive\\Documents\\"+x+f
                    os.startfile(path)
                except:
                    path = "C:\\Users\\rismv\\OneDrive\\Documents\\"+x.capitalize()+f
                    os.startfile(path)

            elif 'pictures' in query:
                self.speak("What would you like to open?")
                x = self.takeAudio()
                try:
                    path = "C:\\Users\\rismv\\OneDrive\\Pictures\\"+x+".jpg"
                    os.startfile(path)
                except:
                    path = "C:\\Users\\rismv\\OneDrive\\Pictures\\"+x.capitalize()+".jpg"
                    os.startfile(path)

            elif 'music' in query:
                self.speak("What would you like to open?")
                x = self.takeAudio()
                try:
                    path = "C:\\Users\\rismv\\Music\\"+x+".mp3"
                    os.startfile(path)
                except:
                    path = "C:\\Users\\rismv\\Music\\"+x.capitalize()+".mp3"
                    os.startfile(path)

            elif 'video' in query:
                self.speak("What would you like to open?")
                x = self.takeAudio()
                try:
                    path = "C:\\Users\\rismv\\Videos\\"+x+".mp4"
                    os.startfile(path)
                except:
                    path = "C:\\Users\\rismv\\Videos\\"+x.capitalize()+".mp4"
                    os.startfile(path)

            elif 'desktop' in query:
                self.speak("What would you like to open?")
                x = self.takeAudio()
                self.speak("What's the format of your file?")
                y = self.takeAudio().lower()
                f = format_dict[y]
                try:
                    path = "C:\\Users\\rismv\\OneDrive\\Desktop\\"+x+f
                    os.startfile(path)
                except:
                    path = "C:\\Users\\rismv\\OneDrive\\Desktop\\"+x.capitalize()+f
                    os.startfile(path)

            elif 'classify' in query:
                self.speak("From where would you like to choose your image?")
                x = self.takeAudio()
                print("Source is ", x)
                self.speak("What's the name of your image?")
                y = self.takeAudio()
                print("Image name is ", y)
                f = folder_dict[x]
                print("Location name is ", f)
                try:
                    source = f+y+".jpg"
                    destination = "stored_images\\"+y+".jpg"
                    shutil.copyfile(source, destination)
                    self.speak("I am working on it please wait")
                    self.classify(y)
                except:
                    source = f+y.capitalize()+".jpg"
                    destination = "stored_images\\"+y.capitalize()+".jpg"
                    shutil.copyfile(source, destination)
                    self.speak("I am working on it please wait")
                    self.classify(y.capitalize())

            elif 'the time' in query:
                Time = datetime.datetime.now().strftime("%H:%M:%S")
                self.speak(f"The time is {Time}")

            elif 'the date' in query:
                date = datetime.date.today()
                today = date.today()
                wd = today.weekday()
                days = ["monday", "tuesday", "wednesday",
                        "thursday", "friday", "saturday", "sunday"]
                self.speak(f"It's {days[wd]}, the {date}")

            elif 'wikipedia' in query:
                self.speak('Searching Wikipedia...')
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2)
                self.speak("According to Wikipedia")
                print(results)
                self.speak(results)

            elif 'shutdown' in query:
                if platform == "win32":
                    os.system('shutdown /p /f')
                elif platform == "linux" or platform == "linux2" or "darwin":
                    os.system('poweroff')

            elif 'thank you' in query:
                self.speak('you are welcome!')
                break


A = assistant()
A.main()
