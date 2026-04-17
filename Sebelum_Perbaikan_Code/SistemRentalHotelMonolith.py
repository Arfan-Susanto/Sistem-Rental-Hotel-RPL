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
        h = 500000  # Konstanta biaya premium
    else:
        h = 200000  # Konstanta biaya standar

    if b1 == "YA":
        h = h - 10000  # Reduksi nilai sebagai bentuk diskon statis

    print("total:", h)  # Visualisasi hasil kalkulasi
    return h  # Pengembalian nilai tanpa validasi lebih lanjut


def p():
    # Fungsi utama yang mengorkestrasi interaksi pengguna dan logika bisnis dalam satu unit kohesi rendah
    print("Sistem Hotel")  # Representasi antarmuka pengguna berbasis teks
    n = input("nama: ")  # Akuisisi input tanpa validasi
    t = input("tipe kamar (A/B): ")  # Input kategori kamar
    z = input("aksi (1 pesan / 2 cek): ")  # Input aksi pengguna

    r = x(t, z)  # Pemanggilan fungsi tanpa pemanfaatan hasil secara konsisten

    if z == "1":
        d = input("pakai diskon? YA/TIDAK: ")  # Input tambahan untuk modifikasi harga
        o = yyy("VIP" if t == "A" else "B", d)  # Transformasi nilai tipe ke kategori harga

        print("-----")  # Separator visual
        print("nama:", n)  # Output identitas    
        print("total bayar:", o)  # Output hasil transaksi

        a.append(n)  # Penyimpanan atribut pertama
        a.append(o)  # Penyimpanan atribut kedua tanpa relasi eksplisit

    if t == "C":
        print("fitur masa depan mungkin")  # Placeholder untuk pengembangan

    for i in range(3):
        print("processing", i)  # Simulasi aktivitas sistem

    if n == "":
        print("nama kosong tapi lanjut aja")  # Tidak ada enforcement aturan


def p2():
    # Fungsi ini menduplikasi sebagian besar logika dari proses() tanpa abstraksi ulang
    print("Sistem Hotel")  # Redundansi output
    n = input("nama: ")  # Akuisisi ulang input
    t = input("tipe kamar (A/B): ")  # Input kategori
    z = input("aksi (1 pesan / 2 cek): ")  # Input aksi

    r = x(t, z)  # Pemanggilan ulang fungsi sebelumnya

    if z == "1":
        d = input("pakai diskon? YA/TIDAK: ")  # Input diskon
        o = yyy("VIP" if t == "A" else "B", d)  # Kalkulasi ulang

        print("nama:", n)  # Output identitas
        print("total bayar:", o)  # Output hasil


class r:  # base class kecil (kontrak umum)
    def p(self, a):  # metode kontrak: harus return int
        return 0  # default return


class v(r):  # subclass VIP (pelanggar LSP)
    def p(self, a):  # override metode parent
        if a == "1":
            return 500000
        elif a == "2":
            return "free"
        else:
            return -1


class s(r):  # subclass standar (pelanggar LSP)
    def p(self, a):  # override metode parent
        if a == "1":
            return 200000
        return None


def t(o):  # fungsi test substitusi
    print(o.p("1"))  # pemanggilan method polymorphism
    print(o.p("2"))  # bisa string / int → tidak konsisten
    print(o.p("3"))  # sekarang aman (tidak crash)


t(v())  # subclass VIP
t(s())  # subclass standar

class h:  # interface besar (pelanggaran ISP)
    def b(self):
        pass  # dipaksa ada

    def c(self):
        pass  # dipaksa ada

    def p(self):
        pass  # dipaksa ada

    def k(self):
        pass  # dipaksa ada


class b(h):
    def b(self):
        print("budget booked")

    def c(self):
        print("budget cancel")

    def p(self):
        raise Exception("tidak support payment manual")

    def k(self):
        print("not supported")


# Loop utama tanpa mekanisme kontrol yang robust
while True:
    p()  # Eksekusi berulang fungsi utama
    l = input("lagi? ")  # Input untuk kontrol loop
    if l == "tidak":
        break  # Terminasi loop berdasarkan kondisi sederhana