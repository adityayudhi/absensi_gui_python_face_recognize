#  --------- TOLONG LUANGKAN WAKTU UNTUK MEMBACA ----------
# MODIFIED BY ADITYA YUDHI HANAFI
# PLEASE USE IT WISELY
# JANGAN DIPAKAI KOMERSIL YA TOLONG :(
# KALAU MAU DONASI BOLEH KOK, PM AJA YA https://web.facebook.com/adityayudhihanafi/
# BUAT TUGAS KAMPUS ATAU PEMBELAJARN SILAHKAN FREEEEEEEEEE TOH SAYA JUGA CUMAN PAKAI LIBRARY ATAU PACKAGE ORANG, TAPI KALAU MAU DONASI ITU LEBIH BAIK 
# KARENA DIDALAMNYA ADA CODINGAN MURNI DARI SAYA JUGA HEHE
# --------- DISHARE , KALAU BISA PESANNYA JANGAN DIUBAH, BIAR SAYA TERKENAL WKWKWK , CANDA TERKENAL --------
# DAH AH CAPEK, MO BOBOK DULU wkwk TERIMAKASIH

import os, cv2, face_recognition, numpy as np, PySimpleGUI as sg, datetime as dt, json, base64, io, sys, face_recognition as fr
from blink_detector import is_blinking
from datetime import datetime
from PIL import Image
from multiprocessing import Process, Value, Manager
from ctypes import c_char_p

JSON_FILE = 'data-absen.json'
WAKTU_PULANG = '13:07:00'
WAKTU_DATANG = '12:42:00'

def rescale_img(image):
    src = image
    scale_percent = 40

    width = int(src.shape[1] * scale_percent / 100)
    height = int(src.shape[0] * scale_percent / 100)

    dsize = (width, height)

    output = cv2.resize(src, dsize)
    return output

def get_encoded_faces():
    encoded = {}

    for dirpath, dnames, fnames in os.walk("./faces"):
        for f in fnames:
            if f.endswith(".jpg") or f.endswith(".png"):
                face = fr.load_image_file("faces/" + f)
                encoding = fr.face_encodings(face)[0]
                encoded[f.split(".")[0]] = encoding

    return encoded

def unknown_image_encoded(img):
    face = fr.load_image_file("faces/" + img)
    encoding = fr.face_encodings(face)[0]

    return encoding

def deteksi_wajah(n, b, c):
    faces = get_encoded_faces()
    faces_encoded = list(faces.values())
    known_face_names = list(faces.keys())
    
    while True:
        # xx = deteksi_wajah_(faces, faces_encoded, known_face_names)
        gambar_ = n.value.encode()
        gambar_ = Image.open(io.BytesIO(base64.b64decode(gambar_)))
        
        gambar_ = np.array(gambar_)
        gambar_ = cv2.cvtColor(gambar_, cv2.COLOR_BGR2RGB)
        try:
            name = ""
            img = gambar_
            face_locations = face_recognition.face_locations(img)
            unknown_face_encodings = face_recognition.face_encodings(img, face_locations)
            
            for face_encoding in unknown_face_encodings:
                matches = face_recognition.compare_faces(faces_encoded, face_encoding)
                

                face_distances = face_recognition.face_distance(faces_encoded, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
            b.value = name
            c.status_deteksi = True
        except Exception as e:
            pass

class Gui:
    def __init__(self):
        self.cc = 0
        
    def gui(self):
        sg.ChangeLookAndFeel('GreenTan')
        citra_cctv1 = [[
                        sg.Frame(layout=[[sg.Image(filename="", key="-IMAGECCTV1-")]], title='Citra Kamera',title_color='black', relief=sg.RELIEF_SUNKEN, tooltip='Citra Kamera')
                      ]]

        headings = ['NAMA', 'WAKTU MASUK', 'WAKTU KELUAR']
        header =  [[sg.Text('  ')] + [sg.Text(h, size=(14,1)) for h in headings]]

        input_rows = [[sg.Input(size=(15,1), pad=(0,0)) for col in range(3)] for row in range(10)]

        font=("Helvetica", 25)

        status_pegawai = [[
                        sg.Frame(layout=[
                        [sg.Text("Nama Pegawai", size=(12,2), font=font), sg.Text(":", size=(1,2), font=font), sg.Text("-", key="-namapegawai-", size=(30,2), font=font)],
                        [sg.Text("Waktu Masuk", size=(12,2), font=font), sg.Text(":", size=(1,2), font=font), sg.Text("-",key="-waktuin-", size=(30,2), font=font)],
                        [sg.Text("Waktu Keluar", size=(12,2), font=font), sg.Text(":", size=(1,2), font=font), sg.Text("-",key="-waktuout-", size=(30,2), font=font)],], title='Data Pegawai',title_color='black', relief=sg.RELIEF_SUNKEN, tooltip='Data Pegawai', size=(1000, 720))
                    ]]
        table_pegawai = [[
                        sg.Frame(layout=[
                        [sg.Text("Nama Pegawai", size=(12,2), font=font), sg.Text(":", size=(1,2), font=font), sg.Text("-", key="-namapegawai-", size=(30,2), font=font)],
                        [sg.Text("Waktu Masuk", size=(12,2), font=font), sg.Text(":", size=(1,2), font=font), sg.Text("-",key="-waktuin-", size=(30,2), font=font)],
                        [sg.Text("Waktu Keluar", size=(12,2), font=font), sg.Text(":", size=(1,2), font=font), sg.Text("-",key="-waktuout-", size=(30,2), font=font)],], title='Data Pegawai',title_color='black', relief=sg.RELIEF_SUNKEN, tooltip='Data Pegawai', size=(1000, 720))
                    ]]


        layout = [[sg.Column(citra_cctv1, size=(720, 420)), sg.Column(status_pegawai, size=(1000, 420))],
                [sg.Text("", size=(50,2), font=("Helvetica", 15), key="-labelpegawai-")],
                [sg.Text("- PLEASE WAIT -", size=(60,2), font=("Helvetica", 15), key="-labelstatus-")]]

        window = sg.Window('Absensi Dengan Citra Wajah', layout, grab_anywhere=False).Finalize()
        # window.Maximize()

        cap = cv2.VideoCapture(0)

        # VAR TAMBAHAN
        data_absen = []
        COUNTER = 0
        TOTAL = 0
        STATUS = False
        nama_pegawai = ''
        list_pegawai = []
        y = ''
        
        while True:
            event, values = window.read(timeout=20)
            if event == 'cancel' or event == None:
                cctv1_run = False
                break
            status, img = cap.read()
            STATUS, COUNTER, TOTAL = is_blinking(img, STATUS, COUNTER, TOTAL)

            retval, buffer1_ = cv2.imencode('.jpg', img)
            gambar_ = base64.b64encode(buffer1_)
            gambar_ = gambar_.decode('utf-8')

            if status_deteksi.value:
                window["-labelstatus-"].update(value='- Ready -')

            string_image.value = gambar_
            nama_pegawai = string_pegawai.value
            if nama_pegawai != '':
                window["-labelpegawai-"].update(value='Terdeteksi Sebagai {}'.format(nama_pegawai.upper()))
                if STATUS:
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")

                    if nama_pegawai not in get_absen_user_json(current_date):                
                        if datetime.strptime(current_time, "%H:%M:%S") <= datetime.strptime(WAKTU_PULANG, "%H:%M:%S"):
                            write_user(current_date, nama_pegawai, img, current_time, 'IN')

                            window["-labelstatus-"].update(value='- SELAMAT DATANG {} -'.format(nama_pegawai.upper()))
                            window["-namapegawai-"].update(value=nama_pegawai)
                            window["-waktuin-"].update(value=current_time)
                            window["-waktuout-"].update(value='-')

                        elif datetime.strptime(current_time, "%H:%M:%S") >= datetime.strptime(WAKTU_PULANG, "%H:%M:%S"):
                            write_user(current_date, nama_pegawai, img, current_time, 'OUT')
                            window["-labelstatus-"].update(value='- HATI-HATI DIJALAN {} -'.format(nama_pegawai.upper()))

                            in_, out_ = get_waktu_in_pegawai(current_date, nama_pegawai)
                            window["-namapegawai-"].update(value=nama_pegawai)
                            window["-waktuin-"].update(value=in_)
                            window["-waktuout-"].update(value=out_)
                        x= datetime.now()
                        y = x + dt.timedelta(0,5)
                        
                    else:
                        if datetime.strptime(current_time, "%H:%M:%S") <= datetime.strptime(WAKTU_PULANG, "%H:%M:%S"):
                            in_, _ = get_waktu_in_pegawai(current_date, nama_pegawai)
                            window["-labelstatus-"].update(value='- {}, ANDA SUDAH ABSEN PADA JAM {} -'.format(nama_pegawai, in_))
                        elif datetime.strptime(current_time, "%H:%M:%S") >= datetime.strptime(WAKTU_PULANG, "%H:%M:%S"):
                            write_user(current_date, nama_pegawai, img, current_time, 'OUT')
                            window["-labelstatus-"].update(value='- HATI-HATI DIJALAN {} -'.format(nama_pegawai.upper()))

                            in_, out_ = get_waktu_in_pegawai(current_date, nama_pegawai)
                            window["-namapegawai-"].update(value=nama_pegawai)
                            window["-waktuin-"].update(value=in_)
                            window["-waktuout-"].update(value=out_)
                        x= datetime.now()
                        y = x + dt.timedelta(0,5)
            else:
                window["-labelpegawai-"].update(value='')

            now = datetime.now()
            current_date = now.strftime("%d/%m/%Y")
            if current_date not in get_tgl_json():
                write_tgl(current_date)
                
            STATUS = False
            if y != '':
                if now.strftime("%H:%M:%S") == y.strftime("%H:%M:%S"):
                    window["-namapegawai-"].update(value='-')
                    window["-waktuin-"].update(value='-')
                    window["-waktuout-"].update(value='-')
                    window["-labelstatus-"].update(value='- Waiting -')
                    y = ''
            img = cv2.resize(img, (580, 420))
            imgbytes1 = cv2.imencode(".png", img)[1].tobytes()
            
            window["-IMAGECCTV1-"].update(data=imgbytes1)
            
        sys.exit()
        window.close()
        cv2.destroyAllWindows()

def get_tgl_json():
    array_tgl = []
    with open(JSON_FILE, 'r') as openfile:
        json_object = json.load(openfile)
    for key,value in json_object.items():
        array_tgl.append(key)
    return array_tgl

def get_waktu_in_pegawai(tgl, pegawai):
    waktuIN = '00:00:00'
    waktuOUT = '00:00:00'
    with open(JSON_FILE, "r") as jsonFile:
        data = json.load(jsonFile)
    try:
        for x in data[tgl]:
            if pegawai in x:
                waktuIN = x[pegawai]['waktu-in'] if x[pegawai]['waktu-in'] != '' else waktuIN
                waktuOUT = x[pegawai]['waktu-out'] if x[pegawai]['waktu-out'] != '' else waktuOUT
    except Exception as e:
        print('Error waktu pegawai, ', pegawai)
        pass
    
    return waktuIN, waktuOUT

def get_absen_user_json(tgl):
    array_user = []
    with open(JSON_FILE, 'r') as openfile:
        json_object = json.load(openfile)
    
    for x in json_object[tgl]:
        for key,value in x.items():
            array_user.append(key)
    return array_user

def write_tgl(tgl):
    with open(JSON_FILE, "r") as jsonFile:
        data = json.load(jsonFile)
        data[tgl] = []

    with open(JSON_FILE, 'r+') as writeFile:
        json.dump(data, writeFile, indent=2)
    
    return ''

def write_user(tgl, pegawai, gambar, waktu, tipe):
    retval, buffer1 = cv2.imencode('.jpg', gambar)
    gambar = base64.b64encode(buffer1)
    gambar = gambar.decode('utf-8')
    is_ok = False

    with open(JSON_FILE, "r") as jsonFile:
        data = json.load(jsonFile)
    
    if tipe == 'IN':
        data[tgl].append({pegawai:{"waktu-in":waktu, "waktu-out":"", "pict-in":gambar,"pict-out":""}})
        is_ok = True
        # if len(data[tgl]) != 0:
            
        #     for x in data[tgl]:
        #         # if pegawai not in x:
        #         #     data[tgl].append({pegawai:{"waktu-in":waktu, "waktu-out":"", "pict-in":gambar,"pict-out":""}})
        #         # else:
        #         #     
        #         if x[pegawai]['waktu-in'] == '':
        #             x[pegawai]['waktu-in'] = waktu
        #             x[pegawai]['pict-in'] = gambar
        #     is_ok = True
        # else:
        #     data[tgl].append({pegawai:{"waktu-in":waktu, "waktu-out":"", "pict-in":gambar,"pict-out":""}})
        #     is_ok = True
        
    elif tipe == 'OUT':
        try:
            if len(data[tgl]) != 0:
                for x in data[tgl]:
                    if pegawai in x:
                        if x[pegawai]['waktu-out'] == '':
                            x[pegawai]['waktu-out'] = waktu
                            x[pegawai]['pict-out'] = gambar
                is_ok = True
            else:
                data[tgl].append({pegawai:{"waktu-in":"", "waktu-out":waktu, "pict-in":"","pict-out":gambar}})
                is_ok = True

        except Exception as e:
            print('Error Out', e)
            pass
    
    if is_ok:
        with open(JSON_FILE, 'r+') as writeFile:
            json.dump(data, writeFile, indent=2)
    
    return ''

if __name__ == "__main__":
    manager = Manager()
    string_image = manager.Value(c_char_p, '')
    string_pegawai = manager.Value(c_char_p, '')
    status_deteksi = Value('i', False)

    now = datetime.now()
    current_date = now.strftime("%d/%m/%Y")
    if current_date not in get_tgl_json():
        write_tgl(current_date)
    g = Gui()
    
    t2 = Process(target=deteksi_wajah, args=[string_image, string_pegawai, status_deteksi])
    t2.daemon = True
    t2.start()
    g.gui()

