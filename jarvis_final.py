#!/usr/bin/python
#pipwin install pyaudio
#pip install pipwin
#pip install arrow y pytssx3
#pip install SpeechRecognition
#pip install wikipedia
#pip install pyautogui
#pip install psutil
#pip install pyjokes
#pip install wolframalpha
#pip install word2number
import pyttsx3, wikipedia, smtplib, os, pyautogui 
import speech_recognition as sr 
import webbrowser as wb
import psutil, pyjokes, random, requests, json
from urllib.request import urlopen
import wolframalpha, sqlite3, arrow, re, pyttsx3


ayuda = '''Palabras clave para interactuar con la IA(incluir el nombre que le hayas dado):
-HORA (actual)\t\t\t-FECHA (actual)
-APÁGATE (cierra la IA)\t\t-WIKIPEDIA
-GOOGLE\t\t\t\t-YOUTUBE
-CIERRA PC(cerrar sesión)\t-APAGA PC
-REINICIA PC\t\t\t-MÚSICA (reproduce la música que tengas en x carpeta)
-GUARDA \\and\\ TAREA \t\t (guardas tareas en la base de datos)
-RECUÉRDAME \\and\\ TAREAS \t (te dice las tareas que tienes en el txt)
-ELIMINA \\and\\ una \\and\\ TAREA (elimina una tarea)
-ELIMINA \\and\\ TODAS\ (elimina todas las tareas)
-CAPTURA \\and\\ PANTALLA\t\t-DATOS \\and\\ PC (cpu y batería)
-CHISTE\t\t\t\t-CORREO \\and\\ (MANDA \\or\\ ENVÍA)
-BUSCA \\and\\ MAPS\t\t-NOTICIAS (API de noticias estadounidenses y las dice en inglés)
'''
#INICIALIZACIONES BDD Y PYTTSX3
con = sqlite3.connect("jarvis.db")
cur = con.cursor()
ia = ""
user = ""
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
newVoiceRate = 150
engine.setProperty("rate", newVoiceRate)
wolframalpha_id_app = "K2GTYV-QX4KXJ3U8Q"

#INTERACTIVIDAD
#Te dice la hora actual
def time():
    timeday = arrow.now("Europe/Madrid")
    timeday = timeday.naive
    list_time = re.split(r"-|\:| ", str(timeday))
    hour = int(list_time[3])
    minutes = list_time[4]
    seconds = float(list_time[5])
    if hour >= 6 and hour < 12:
            greetings = "Buenos dias"
    elif hour >= 12 and hour < 20:
        greetings = "Buenos tardes"
    else:
        greetings = "Buenas noches"

    speak(f"{greetings}, son las {hour} horas y {minutes} minutos y {seconds:.0f} segundos")
   

#Te dice la fecha actual
def date():
    dateday = arrow.now("Europe/Madrid").weekday()
    dates = arrow.now("Europe/Madrid")
    datess = dates.naive
    list_dates = re.split(r"-|\:| ", str(datess))
    nday = list_dates[2]
    year = list_dates[0]
    nmonth = list_dates[1]
    list_weekdays = [ "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    day = list_weekdays[dateday]
    list_months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Dicembre"]
    month = list_months[int(nmonth)-1]

#Búsqueda en wikipedia
def wikip():
    speak("¿Qué quieres buscar")
    query = takeCommand().lower()
    wikipedia.set_lang("es")
    result = wikipedia.summary(query, sentences = 2)
    speak(result)

#Búsqueda en Google Chrome ARREGLAR PATH
def chrome():
    speak("¿Que quieres buscar?")
    chromepath = ("C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe")
    search = takeCommand().lower()
    wb.register("chrome", None,wb.BackgroundBrowser(chromepath))
    b = wb.get("chrome")
    b.open_new_tab(search)

#Reproduce la música 
def playmusic():
    #No se exáctamente como mejorar esto la verdad, tienes que estar situado sobre la ruta de los archivos
    songs_dir = ("jarvis_entrega\musica\\")
    songs = os.listdir(songs_dir)
    os.startfile(os.path.join(songs_dir, songs[0]))

#Guarda tareas en la bdd
def recordar():
    timeday = arrow.now("Europe/Madrid")
    timeday = timeday.naive
    speak("¿Que quieres recordar?")
    data = takeCommand().lower()
    speak("A partir de ahora recordaré: "+data)
    cur.execute("INSERT INTO remembers (task, dates) VALUES (?, ?)", (data, timeday))
    con.commit() 

#Te dice las tareas que tengas en la BDD
def recuerdos():
    cur.execute("SELECT task FROM remembers")
    rows = cur.fetchall()
    for r in rows:
        #a = ""
        a = r[0]
        a.rstrip(",")
        speak(a)

#Elimina la tarea que quieras( tienes que decir el nombre de la tarea tal cual la IA la recuerda)
def elim_rec():
    speak("¿Que tarea quieres eliminar?")
    tarea = takeCommand().lower()
    speak("Eliminando "+tarea)
    cur.execute("DELETE FROM remembers where task = ?", (tarea, ))
    con.commit()

#Eliminar todas las tareas
def elim_all_rec():
    speak("Eliminando todas las tareas")
    cur.execute("DELETE FROM remembers")
    con.commit()

#Hacer captura de pantalla
def screenshott():
    img = pyautogui.screenshot()
    timeday = arrow.now("Europe/Madrid")
    timeday = timeday.naive
    list_time = re.split(r"-|\:| ", str(timeday))
    hour = int(list_time[3])
    minutes = list_time[4]
    seconds =float(list_time[5])
    nday = list_time[2]
    year = list_time[0]
    nmonth = list_time[1]
    img.save(f"jarvis_entrega\capturas\{nday}-{nmonth}-{year} at {hour}.{minutes}.{seconds:.0f} .png")

#Datos de la cpu y bateria
def cpu():
    usage = str(psutil.cpu_percent())
    battery = list( psutil.sensors_battery())
    speak(f"El uso de CPU es: {usage}")
    speak(f"La batería esta al: {battery[0]}")

#Cuenta un chiste aleatorio
def chiste():
    speak(pyjokes.get_joke(language="es"))

#Enviar un email, tienes que poner tu email y contraseña
def sendmail(to, content):
    correo = "inserta aqui tu correo"
    password = "inserta aqui tu contraseña"
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(correo, password)
    server.sendmail(correo, to, content)
    server.close()

#Búsqueda en youtube de un video SOLUCIONAR EL PATH DE GOOGLE
def youtube():
    speak("¿Que quieres buscar?")
    chromepath = ("C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe")
    query = takeCommand().lower()
    speak("Buscando en youtube "+query)
    wb.register("chrome", None,wb.BackgroundBrowser(chromepath))
    b = wb.get("chrome")
    b.open_new_tab("https://www.youtube.com/results?search_query="+query)

#Búsqueda localización en Google Maps ARREGLAR PATH GOOGLE
def gmaps():
    speak("¿Que quieres buscar?")
    chromepath = ("C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe")
    wb.register("chrome", None,wb.BackgroundBrowser(chromepath))
    b = wb.get("chrome")
    query = takeCommand()
    speak("Localizando "+query)
    b.open_new_tab("https://www.google.com/maps/place/"+query)

#API de noticias de EEUU, no funciona bien ya que está en inglés y
#el lenguaje de la IA es español
def noticias():
    try:
        jsonObj = urlopen("http://newsapi.org/v2/everything?q=bitcoin&from=2020-09-30&sortBy=publishedAt&apiKey=35951028907b4d78b227be4bfe1e6cc0")
        data = json.load(jsonObj)
        i = 1

        speak("Aqui tenemos los titulares del bitcoin")
        for item in data["articles"]:
            speak(item["title"])
            i += 1
    except Exception as e:
        print(str(e))

#API wolframalpha con numerosas funcionalidades, en este caso hace cálculos.
def calculator(query):
    client = wolframalpha.Client(wolframalpha_id_app)
    indx = query.lower().index("calcula")
    query = query.split()[indx + 1:]
    res = client.query("".join(query))
    answer = next(res.results).text
    print("La respuesta es: " +answer)
    speak("La respuesta es: " +answer)

#API wolframalpha con numerosas funcionalidades, en este caso te define palabras
#aunque no funciona bien ya que está en inglés
def definition(query):
    client = wolframalpha.Client(wolframalpha_id_app)
    res = client.query(query)
    try:
        print(next(res.results).text)
        speak(next(res.results).text)
    except StopIteration:
        print("No Results")




#--------------------------#
#MÉTODOS DE CONTROL
#Método para cuando inicies por primera vez la IA te pida los datos y los inserte en la BD
def config_entry():
    speak("¡Hola! Soy tu inteligencia artificial personalizada. ¿A partir de ahora, como quieres que me llame?")
    ia = takeCommand().lower()
    print(ia)
    speak("¿Y como te gustaría que te llame?")
    user = takeCommand().lower()
    print(user)
    cur.execute("INSERT INTO config ( ia_name, usser_name) VALUES (?, ?)", (ia, user))
    con.commit()
    speak(f"Perfecto {user} a partir de ahora me llamaré {ia}" )
    
#Método para que la IA hable
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

#Método para recoger la entrada de sonido, solucionado el que cuando no entienda lo que dices no vuelva
#al punto de partida
def takeCommand():
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando")
        r.pause_threshold = 0.5
        audio = r.listen(source)

    try:
        print("Reconociendo....")
        query = r.recognize_google(audio, language="es")
    except Exception as e:
        print(e)
        speak("No te entiendo. ¿Puedes repetirlo?")
        query = takeCommand()
            
            
    return query

#Saludo al encender la IA(cuando ya tenga la configuración hecha)
def wishme():
    speak(f"Hola, {ia} a tu servicio, ¿que quieres que haga por ti, {user}?")


#MAIN
if __name__ =="__main__":
    print(ayuda)
    cur.execute("CREATE TABLE if not exists config (ia_name, usser_name)")
    cur.execute("CREATE TABLE if not exists remembers (task, dates)")
    con.commit()
    cur.execute("SELECT * FROM config")
    result = list(cur.fetchall())
    
    if len(result) == 0:
        #Estariamos ejecutando por primera vez la IA
        config_entry()
        speak("?Que puedo hacer por ti?")
    
    else:
        #Ya tendríamos hecha la configuración de la IA
        cur.execute("SELECT * FROM config")
        result = list(cur.fetchall())
        ia, user = result[0]
        wishme()

    while True:
        query = takeCommand().lower()
        print(query)
        if ia in query:
            if "hora" in query:
                time()
            elif "fecha" in query:
                date()
            elif "apágate" in query:
                speak("Apagando. ¡Adioooos!")
                quit()
            elif "wikipedia" in query:
                wikip()
            elif "google" in query:
                chrome()
            elif "youtube" in query:
                youtube()
            elif "cierra pc" in query:
                os.system("shutdown /l")
            elif "apaga pc" in query:
                os.system("shutdown /s /t 1")
            elif "reinicia pc" in query:
                os.system("shutdown /r /t 1")
            elif "música" in query: 
                playmusic()
            elif "guarda" in query and "tarea" in query:
                recordar()
            elif "recuérdame" in query and "tareas" in query:
                recuerdos()
            elif "elimina" in query and "una" in query and "tarea" in query:
                elim_rec()
            elif "elimina" in query and "todas" in query:
                elim_all_rec()
            elif "captura" in query and "pantalla" in query:
                screenshott()
                speak("Done")
            elif "datos" in query and "pc" in query:
                cpu()
            elif "chiste" in query:
                chiste()
            elif "correo" in query and ("manda" or "envía") in query:
                reciever = input("¿A quien le tenemos que enviar el correo?")
                speak("¿Que contenido tiene el mensaje?")
                cont = takeCommand()
                sendmail(reciever,cont)
            elif "busca" in query and "maps" in query:
                gmaps()
            elif "noticias" in query:
                noticias()
            