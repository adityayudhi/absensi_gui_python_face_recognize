# absensi_gui_python_face_recognize
Absensi Dengan Python Menggunakan Sistem Face Recognize

# INSTALASI
1. Install python3
2. git clone https://github.com/adityayudhi/absensi_gui_python_face_recognize.git
3. Install dependency -> pip install -r requirements.txt

# RUNNING
1. Letakkan foto .jpg kedalam folder faces dengan filename sesuai dengan nama yang ada difoto
2. Run face_rec.py -> python face_rec.py

# TroubleShoot
1. Apabila muncul error "can't grab frame" coba jalankan cek.py untuk melihat list kamera
  - Contoh output List Camera [1,2,3]
3. list kamera berbentuk array, silahkan coba value index satu persatu
4. replace 'cap = cv2.VideoCapture(0)' pada file 'face_rec.py' menjadi 'cap = cv2.VideoCapture(index_value)' yang didapatkan dari eksekusi cek.py tadi
