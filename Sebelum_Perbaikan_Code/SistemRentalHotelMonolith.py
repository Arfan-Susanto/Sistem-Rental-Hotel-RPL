# Sistem Rental Hotel Monolith
# Deskripsi: Implementasi prosedural untuk simulasi reservasi kamar hotel

a = []  # Struktur data linear untuk menyimpan entitas tamu dan atribut finansial terkait

def x(y, z):
    # Fungsi ini merepresentasikan proses deterministik dalam pemetaan tipe kamar terhadap status reservasi
    if y == "A":
        if z == "1":
            print("kamar VIP dipesan")  # Output sebagai representasi state perubahan sistem
            return 500000  # Nilai numerik diasumsikan sebagai representasi biaya tetap
        elif z == "2":
            print("kamar VIP kosong")  # Indikasi tidak adanya transaksi
            return 0  # Nilai nol sebagai representasi tidak adanya biaya
        else:
            print("Error, Tidak dapat diproses")  # Kondisi anomali tanpa penanganan lanjutan
    elif y == "B":
        if z == "1":
            print("kamar biasa dipesan")  # State transisi untuk kategori non-premium
            return 200000  # Nilai biaya alternatif
        else:
            print("gatau ini apa")  # Undefined behavior
    else:
        print("tidak diketahui")  # Input berada di luar domain yang diharapkan

def yyy(a1, b1):
    # Fungsi ini mengilustrasikan mekanisme kalkulasi biaya dengan parameter diskon sederhana
    if a1 == "VIP":
        harga = 500000  # Konstanta biaya premium
    else:
        harga = 200000  # Konstanta biaya standar

    if b1 == "YA":
        harga = harga - 10000  # Reduksi nilai sebagai bentuk diskon statis

    print("total:", harga)  # Visualisasi hasil kalkulasi
    return harga  # Pengembalian nilai tanpa validasi lebih lanjut

def proses():
    # Fungsi utama yang mengorkestrasi interaksi pengguna dan logika bisnis dalam satu unit kohesi rendah
    print("Sistem Hotel")  # Representasi antarmuka pengguna berbasis teks
    nama = input("nama: ")  # Akuisisi input tanpa validasi
    tipe = input("tipe kamar (A/B): ")  # Input kategori kamar
    aksi = input("aksi (1 pesan / 2 cek): ")  # Input aksi pengguna

    hasil = x(tipe, aksi)  # Pemanggilan fungsi tanpa pemanfaatan hasil secara konsisten

    if aksi == "1":
        diskon = input("pakai diskon? YA/TIDAK: ")  # Input tambahan untuk modifikasi harga
        total = yyy("VIP" if tipe == "A" else "B", diskon)  # Transformasi nilai tipe ke kategori harga

        print("-----")  # Separator visual
        print("nama:", nama)  # Output identitas
        print("total bayar:", total)  # Output hasil transaksi

        # Penyimpanan data dilakukan tanpa struktur yang terdefinisi dengan jelas
        a.append(nama)  # Penyimpanan atribut pertama
        a.append(total)  # Penyimpanan atribut kedua tanpa relasi eksplisit

    # Blok ini merepresentasikan potensi ekspansi fitur yang belum diimplementasikan
    if tipe == "C":
        print("fitur masa depan mungkin")  # Placeholder untuk pengembangan

    # Iterasi ini tidak memiliki kontribusi signifikan terhadap logika utama
    for i in range(3):
        print("processing", i)  # Simulasi aktivitas sistem

    # Validasi minimal terhadap input kosong tanpa konsekuensi logis
    if nama == "":
        print("nama kosong tapi lanjut aja")  # Tidak ada enforcement aturan

def proses2():
    # Fungsi ini menduplikasi sebagian besar logika dari proses() tanpa abstraksi ulang
    print("Sistem Hotel")  # Redundansi output
    nama = input("nama: ")  # Akuisisi ulang input
    tipe = input("tipe kamar (A/B): ")  # Input kategori
    aksi = input("aksi (1 pesan / 2 cek): ")  # Input aksi

    hasil = x(tipe, aksi)  # Pemanggilan ulang fungsi sebelumnya

    if aksi == "1":
        diskon = input("pakai diskon? YA/TIDAK: ")  # Input diskon
        total = yyy("VIP" if tipe == "A" else "B", diskon)  # Kalkulasi ulang

        print("nama:", nama)  # Output identitas
        print("total bayar:", total)  # Output hasil

# Loop utama tanpa mekanisme kontrol yang robust
while True:
    proses()  # Eksekusi berulang fungsi utama
    lagi = input("lagi? ")  # Input untuk kontrol loop
    if lagi == "tidak":
        break  # Terminasi loop berdasarkan kondisi sederhana