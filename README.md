# Sistem Rental Hotel RPL (Rekayasa Perangkat Lunak)

---

## Analisis Pelanggaran Kode Sebelum Perbaikan

### 1.1 Analisis File: `SistemRentalHotelMonolith.py`

#### **Pelanggaran 1: NAMING (Penamaan Tidak Jelas)**

```python
a = []
def x(y, z):
def yyy(a1, b1):
```

**Masalah:**
- Variabel `a` tidak menjelaskan tujuannya (guest list? bookings? transactions?)
- Fungsi `x()` dan `yyy()` tidak deskriptif sama sekali
- Parameter `y`, `z`, `a1`, `b1` tidak jelas maknanya
- Developer baru akan kesulitan memahami intent dari kode

**Dampak:** Readability score sangat rendah, maintenance cost tinggi

---

#### **Pelanggaran 2: SPAGHETTI CODE (Kode Tidak Terstruktur)**

```python
def proses():
    print("Sistem Hotel")
    nama = input("nama: ")
    tipe = input("tipe kamar (A/B): ")
    aksi = input("aksi (1 pesan / 2 cek): ")
    
    hasil = x(tipe, aksi)
    
    if aksi == "1":
        diskon = input("pakai diskon? YA/TIDAK: ")
        total = yyy("VIP" if tipe == "A" else "B", diskon)
    
    if tipe == "C":
    
    for i in range(3):
        print("processing", i)
    
    if nama == "":
        print("nama kosong tapi lanjut aja")
```

**Masalah:**
- Semua logic tercampur dalam satu function
- Perpaduan UI, business logic, dan data storage
- Multiple responsibilities dalam satu place
- If-else statements yang berkelindan
- Loop yang tidak clear purpose-nya

**Dampak:** Sulit untuk testing, reusability minimum, high bug risk

---

#### **Pelanggaran 3: DRY (Code Duplication)**

```python
def proses():

def proses2():
    print("Sistem Hotel")
    nama = input("nama: ")
    tipe = input("tipe kamar (A/B): ")
    aksi = input("aksi (1 pesan / 2 cek): ")
    
    hasil = x(tipe, aksi)
    
    if aksi == "1":
        diskon = input("pakai diskon? YA/TIDAK: ")
        total = yyy("VIP" if tipe == "A" else "B", diskon)
```

**Masalah:**
- Duplikasi kode dari `proses()` ke `proses2()`
- Maintenance nightmare (bug di satu harus diperbaiki di dua tempat)
- Perubahan logika harus dilakukan di multiple locations

**Dampak:** Maintenance burden, inconsistency risk, development time waste

---

#### **Pelanggaran 4: MAGIC STRINGS/NUMBERS**

```python
if y == "A":
    if z == "1":
        print("kamar VIP dipesan")
        return 500000  # Magic number!
    elif z == "2":
        print("kamar VIP kosong")
        return 0

if a1 == "VIP":
    harga = 500000
else:
    harga = 200000

if b1 == "YA":
    harga = harga - 10000
```

**Masalah:**
- Konstanta hardcoded di berbagai tempat
- Tidak ada single source of truth
- Jika harga berubah, harus update di multiple places
- Tidak jelas apa arti angka-angka tersebut

**Dampak:** Rentan error, sulit untuk di-maintain, fleksibilitas rendah

---

#### **Pelanggaran 5: TIDAK ADA ERROR HANDLING**

```python
def proses():
    nama = input("nama: ")
    tipe = input("tipe kamar (A/B): ")
    aksi = input("aksi (1 pesan / 2 cek): ")
    
    hasil = x(tipe, aksi)
    
    if nama == "":
        print("nama kosong tapi lanjut aja")
```

**Masalah:**
- Input tidak divalidasi
- Tidak ada try-catch blocks
- Program bisa crash dengan input unexpected
- No graceful error recovery

**Dampak:** Pengalaman pengguna buruk, masalah integritas data, risiko crash

---

#### **Pelanggaran 6: NO ENCAPSULATION (Tidak Ada Enkapsulasi)**

```python
a = []
def proses():
    a.append(nama)
    a.append(total)
```

**Masalah:**
- Data disimpan dalam list global `a`
- No protection atau validation ketika data ditambahkan
- Any function bisa langsung modify data
- Tight coupling

**Dampak:** Masalah integritas data, perilaku tidak dapat diprediksi, sulit untuk debug

---

#### **Pelanggaran 7: LOW COHESION (Kohesi Rendah)**

**Masalah:**
- `proses()` function bercampur UI logic, business logic, dan data persistence
- Setiap concern tidak terisolasi
- Function memiliki multiple reasons to change

**Dampak:** Sulit untuk di-maintain, sulit untuk di-test, pemisahan concerns yang buruk

---

#### **Pelanggaran 8: COMMENTS TIDAK SESUAI**

```python
# Struktur data linear untuk menyimpan entitas tamu dan atribut finansial terkait
a = []

# Fungsi ini merepresentasikan proses deterministik dalam pemetaan tipe kamar 
# terhadap status reservasi
def x(y, z):
```

**Masalah:**
- Comments yang terlalu verbose dan tidak memberikan value
- Comments yang dalam bahasa terlalu formal/academic
- Ada comments yang misleading atau tidak helpful

**Dampak:** Berantakan, membingungkan, tidak membantu pemahaman

---

#### **Pelanggaran 9: YAGNI (Fitur yang Tidak Dibutuhkan)**

```python
if tipe == "C":
    print("fitur masa depan mungkin")

for i in range(3):
    print("processing", i)
```

**Masalah:**
- Kode yang tidak clear purposenya
- Placeholder yang tidak pernah diimplementasi
- Loop yang tidak contribute ke business logic

**Dampak:** Code bloat, kebingungan, beban maintenance

---

#### **Pelanggaran 10: SOLID PRINCIPLE VIOLATIONS**

**Pelanggaran SRP (Single Responsibility):**
- `proses()` bertanggung jawab untuk: input, booking, calculation, storage, output

**Pelanggaran OCP (Open/Closed):**
- Menambah tipe kamar baru memerlukan modifikasi `x()` dan `yyy()`

**Pelanggaran DIP (Dependency Inversion):**
- Function langsung bergantung pada data structure `a` yang concrete

---

#### **Pelanggaran 11: KISS PRINCIPLE**

**Masalah:**
- Multiple nested if-else statements
- Kompleks logic untuk task yang sederhana
- Overly verbose comments
- Unnecessary loops

**Dampak:** Terlalu rumit, sulit diikuti, sulit untuk di-maintain

---

## Analisis Resolusi Kode Sesudah Perbaikan

### 2.1 Struktur Folder dan File

```
Sesudah_Perbaikan_Code/
├── main.py                      # UI/Entry point
├── models/
│   └── room.py                  # Entity layer
├── repositories/
│   └── room_repository.py       # Data access layer
├── services/
│   ├── booking_service.py       # Business logic untuk booking
│   └── payment_service.py       # Business logic untuk payment
└── utils/
    └── constants.py             # Global constants
```

---

### 2.2 Resolusi Pelanggaran

#### **RESOLUSI 1: NAMING (Penamaan Jelas dan Deskriptif)**

**Sebelum:**
```python
a = []
def x(y, z):
def yyy(a1, b1):
```

**Sesudah:**
```python
# models/room.py
class Room:
    def __init__(self, room_type: str, price: int):
        self.__room_type = room_type
        self.__price = price
        self.__is_available = True
    
    @property
    def room_type(self):
        return self.__room_type
    
    @property
    def price(self):
        return self.__price

# services/booking_service.py
def book_room(self, room_type: str) -> int:
    """Melakukan booking kamar dan mengembalikan harga kamar."""
    room = self.__repository.get_room(room_type)
    room.book()
    return room.price

# services/payment_service.py
def calculate_total(self, price: int, use_discount: bool = False) -> int:
    """Menghitung total pembayaran dengan aplikasi diskon dan fee."""
    total = price
    if use_discount:
        total -= DISCOUNT_AMOUNT
    total = self.__apply_fee(total)
    return total
```

**Pembaruan:**
- Nama class yang deskriptif: `Room`, `BookingService`, `PaymentService`
- Nama method yang jelas: `book_room()`, `calculate_total()`, `check_availability()`
- Nama variabel yang meaningful: `room_type`, `price`, `booking_id`
- Type hints untuk clarity: `room_type: str`, `price: int`, `-> int`

**Dampak:** Keterbacaan tinggi, kode yang self-documenting, mudah dipahami

---

#### **RESOLUSI 2: MAGIC STRINGS/NUMBERS (Menggunakan Constants)**

**Sebelum:**
```python
if y == "A":
    return 500000
elif y == "B":
    return 200000
```

**Sesudah:**
```python
# utils/constants.py
VIP = "VIP"
STANDARD = "STANDARD"
DISCOUNT_AMOUNT = 10000

# models/room.py
class VIPRoom(Room):
    def __init__(self):
        super().__init__("VIP", 500000)

class StandardRoom(Room):
    def __init__(self):
        super().__init__("STANDARD", 200000)

# main.py
if room_type not in [VIP, STANDARD]:
    print("Invalid room type. Please use VIP or STANDARD")
```

**Pembaruan:**
- Single source of truth untuk constants
- Nama semantik untuk constants
- Konfigurasi terpusat
- Mudah mengubah nilai

**Dampak:** Maintainability tinggi, konsistensi, fleksibilitas

---

#### **RESOLUSI 3: SEPARATION OF CONCERNS (SRP - Single Responsibility)**

**Sebelum:**
```python
def proses():
    nama = input("nama: ")
    hasil = x(tipe, aksi)
    total = yyy("VIP" if tipe == "A" else "B", diskon)
    a.append(nama)
    a.append(total)
```

**Sesudah:**
```python
# models/room.py
class Room:
    def book(self):
        if not self.__is_available:
            raise Exception("Room is not available")
        self.__is_available = False

# services/booking_service.py
def book_room(self, room_type: str) -> int:
    room = self.__repository.get_room(room_type)
    room.book()
    return room.price

# services/payment_service.py
def calculate_total(self, price: int, use_discount: bool = False) -> int:
    total = price
    if use_discount:
        total -= DISCOUNT_AMOUNT
    total = self.__apply_fee(total)
    return total

# repositories/room_repository.py
def get_room(self, room_type: str) -> Room:
    if room_type not in self.__rooms:
        raise ValueError("Invalid room type")
    return self.__rooms[room_type]

# main.py
def main():
    try:
        name = input("Name: ").strip()
        room_type = input("Room type (VIP/STANDARD): ").upper()
    except Exception as error:
        print("Error:", error)
```

**Pembaruan:**
- `Room` class: Hanya manage state dan behavior kamar
- `BookingService`: Hanya handle booking logic
- `PaymentService`: Hanya handle payment calculation
- `RoomRepository`: Hanya handle data access
- `main()`: Hanya orchestrate dan UI

**Dampak:** Kohesi tinggi, coupling rendah, dapat di-test, mudah di-maintain

---

#### **RESOLUSI 4: ENCAPSULATION (Enkapsulasi Data)**

**Sebelum:**
```python
a = []
def proses():
    a.append(nama)
    a.append(total)
```

**Sesudah:**
```python
# models/room.py
class Room:
    def __init__(self, room_type: str, price: int):
        self.__room_type = room_type
        self.__price = price
        self.__is_available = True
    
    @property
    def room_type(self):
        """Getter - read-only access"""
        return self.__room_type
    
    @property
    def price(self):
        """Getter - read-only access"""
        return self.__price
    
    @price.setter
    def price(self, value: int):
        """Setter - dengan validasi"""
        if value < 0:
            raise ValueError("Price cannot be negative")
        self.__price = value
    
    def book(self):
        """Controlled modification"""
        if not self.__is_available:
            raise Exception("Room is not available")
        self.__is_available = False

# services/booking_service.py
class BookingService:
    def __init__(self, repository: RoomRepository):
        self.__repository = repository
        self.__bookings_history = []
        self.__booking_id_counter = 1000
    
    def book_room(self, room_type: str) -> int:
        """Controlled access to internal history"""
        room = self.__repository.get_room(room_type)
        room.book()
        self.__bookings_history.append({...})
        return room.price
```

**Pembaruan:**
- Private attributes dengan `__` prefix
- Properties untuk read-only access
- Setters dengan validation
- Methods untuk controlled modification
- No direct state modification from outside

**Dampak:** Integritas data, keamanan, akses terkontrol, refactoring lebih mudah

---

#### **RESOLUSI 5: ERROR HANDLING (Penanganan Error)**

**Sebelum:**
```python
def proses():
    nama = input("nama: ")
    tipe = input("tipe kamar (A/B): ")
    
    if nama == "":
        print("nama kosong tapi lanjut aja")
```

**Sesudah:**
```python
# main.py
def main():
    """Entry point aplikasi dengan comprehensive error handling."""
    try:
        name = input("Name: ").strip()
        room_type = input("Room type (VIP/STANDARD): ").upper()
        
        if room_type not in [VIP, STANDARD]:
            print("Invalid room type. Please use VIP or STANDARD")
            return
        
        if not booking_service.check_availability(room_type):
            print("Room not available")
            return
        
        price = booking_service.book_room(room_type)
        
        payment_choice = display_payment_methods()
        payment_service = get_payment_service(payment_choice)
        
        use_discount = input("Use discount? (y/n): ").lower() == "y"
        total = payment_service.calculate_total(price, use_discount)
        
    except Exception as error:
        print("Error:", error)

# models/room.py
@price.setter
def price(self, value: int):
    """Setter dengan validasi."""
    if value < 0:
        raise ValueError("Price cannot be negative")
    self.__price = value

def book(self):
    """Dengan error checking."""
    if not self.__is_available:
        raise Exception("Room is not available")
    self.__is_available = False

# services/payment_service.py
@fee_percentage.setter
def fee_percentage(self, value: float):
    """Setter dengan validasi non-negatif."""
    if value < 0:
        raise ValueError("Fee percentage cannot be negative")
    self.__fee_percentage = value
```

**Pembaruan:**
- Try-catch blocks untuk error handling
- Input validation di critical points
- Custom exceptions dengan meaningful messages
- Graceful error recovery
- Validation di setters

**Dampak:** Aplikasi yang robust, pengalaman pengguna lebih baik, integritas data

---

#### **RESOLUSI 6: DRY (Don't Repeat Yourself)**

**Sebelum:**
```python
def proses():
    print("Sistem Hotel")
    nama = input("nama: ")

def proses2():
    print("Sistem Hotel")
    nama = input("nama: ")
```

**Sesudah:**
```python
def main():
    """Entry point aplikasi."""
    repository = RoomRepository()
    
    print("=== Hotel Rental System ===")
    
    try:
        name = input("Name: ").strip()
        room_type = input("Room type (VIP/STANDARD): ").upper()
        
        if room_type == VIP:
            booking_service = VIPBookingService(repository)
        else:
            booking_service = StandardBookingService(repository)

# Reusable BookingService classes
class BookingService:
    def book_room(self, room_type: str) -> int:
        """Reusable logic"""
        room = self.__repository.get_room(room_type)
        room.book()
        return room.price

class VIPBookingService(BookingService):
    """Extends base dengan VIP-specific behavior"""
    def book_vip_room_with_concierge(self, guest_name: str, special_requests: list = None) -> dict:
        """VIP-specific method"""
        pass

class StandardBookingService(BookingService):
    """Extends base dengan Standard-specific behavior"""
    pass
```

**Pembaruan:**
- Satu entry point `main()` bukan banyak variants
- Reusable service classes dengan inheritance
- Polymorphism untuk different room types
- No code duplication

**Dampak:** Lebih mudah di-maintain, konsistensi, single source of logic

---

#### **RESOLUSI 7: YAGNI (Fitur yang Benar-benar Dibutuhkan)**

**Sebelum:**
```python
if tipe == "C":
    print("fitur masa depan mungkin")

for i in range(3):
    print("processing", i)
```

**Sesudah:**
```python
def main():
    """Entry point aplikasi."""
    repository = RoomRepository()
    
    print("=== Hotel Rental System ===")
    
    try:
        name = input("Name: ").strip()
        room_type = input("Room type (VIP/STANDARD): ").upper()
        
        if room_type not in [VIP, STANDARD]:
            print("Invalid room type. Please use VIP or STANDARD")
            return
        
        if room_type == VIP:
            booking_service = VIPBookingService(repository)
        else:
            booking_service = StandardBookingService(repository)
```

**Pembaruan:**
- Kode placeholder tidak perlu sudah dihapus
- Loop yang tidak jelas tujuannya sudah dihapus
- Hanya mengimplementasikan fitur yang diperlukan
- Intent yang bersih dan terfokus

**Dampak:** Lebih sedikit code bloat, intent lebih jelas, lebih mudah dipahami

---

#### **RESOLUSI 8: SOLID PRINCIPLES (Implementasi Penuh)**

**A. Single Responsibility Principle (SRP)**
- `Room`: Represents room entity
- `BookingService`: Handles booking logic
- `PaymentService`: Handles payment logic
- `RoomRepository`: Handles data access
- `main()`: Handles UI orchestration

**B. Open/Closed Principle (OCP)**
```python
class PaymentService(ABC):
    @abstractmethod
    def _apply_fee(self, amount: int) -> int:
        pass
    
    @abstractmethod
    def process_payment(self, amount: int, reference_id: str = None) -> dict:
        pass

class CashPayment(PaymentService):
    def _apply_fee(self, amount: int) -> int:
        return amount
    
    def process_payment(self, amount: int, reference_id: str = None) -> dict:

class CreditCardPayment(PaymentService):
    def _apply_fee(self, amount: int) -> int:
        return int(amount * 1.03)
    
    def process_payment(self, amount: int, reference_id: str = None) -> dict:

```

**Pembaruan:**
- Menambah payment method baru tidak perlu modifikasi existing code
- Tinggal create subclass baru yang inherit PaymentService

**C. Liskov Substitution Principle (LSP)**
```python
class Room:
    def book(self):
        if not self.__is_available:
            raise Exception("Room is not available")
        self.__is_available = False

class VIPRoom(Room):
    """Dapat menggantikan Room tanpa mengubah behavior"""
    def get_room_info(self):
        info = super().get_room_info()
        info["facilities"] = self.__facilities
        return info

class StandardRoom(Room):
    """Dapat menggantikan Room tanpa mengubah behavior"""
    pass

booking_service = VIPBookingService(repository)
room = booking_service.repository.get_room(VIP)
room.book()
```

**D. Interface Segregation Principle (ISP)**
```python
class PaymentService(ABC):
    """Interface bahwa semua payment method harus implementasi"""
    @abstractmethod
    def calculate_total(self, price: int, use_discount: bool = False) -> int:
        pass
    
    @abstractmethod
    def process_payment(self, amount: int, reference_id: str = None) -> dict:
        pass

payment_service = get_payment_service(payment_choice)
total = payment_service.calculate_total(price, use_discount)
```

**E. Dependency Inversion Principle (DIP)**
```python
class BookingService:
    def __init__(self, repository: RoomRepository):
        self.__repository = repository
    
    def check_availability(self, room_type: str) -> bool:
        room = self.__repository.get_room(room_type)
        return room.is_available

```

**Pembaruan:**
- Semua 5 prinsip SOLID terimplementasi
- Code lebih flexible dan extensible
- Mudah untuk di-test dan di-maintain

---

#### **RESOLUSI 9: COMMENTS (Dokumentasi yang Sesuai)**

**Sebelum:**
```python
a = []

def x(y, z):
```

**Sesudah:**
```python
class BookingService:
    """
    Service layer untuk menangani logika bisnis terkait booking kamar (Base Class).
    Tidak menangani input/output (UI), hanya business logic.
    Mengimplementasikan pola Service Locator untuk abstraksi repository.
    """
    
    def __init__(self, repository: RoomRepository):
        """
        Inisialisasi BookingService dengan dependency injection repository.
        
        Args:
            repository (RoomRepository): Repository untuk akses data kamar
        """
        self.__repository = repository

def book_room(self, room_type: str) -> int:
    """
    Melakukan booking kamar dan mengembalikan harga kamar.
    Mengubah status kamar menjadi tidak tersedia dan mencatat history.
    
    Args:
        room_type (str): Tipe kamar yang akan dipesan (VIP/STANDARD)
    
    Returns:
        int: Harga kamar dalam Rupiah
    """
    room = self.__repository.get_room(room_type)
    room.book()
    return room.price
```

**Pembaruan:**
- Docstrings yang meaningful
- Menjelaskan purpose, parameters, dan return values
- Type hints yang jelas
- Komentar yang explain "why" bukan "what"
- Professional dan konsisten format

**Dampak:** Kode yang self-documenting, IDE auto-completion bekerja, onboarding lebih mudah

---

#### **RESOLUSI 10: CODE ARCHITECTURE (Terstruktur)**

**Sebelum:** Monolithic - satu file besar dengan semua logic tercampur
```
SistemRentalHotelMonolith.py  (1 file, ~100 lines)
```

**Sesudah:** Layered architecture yang clean
```
main.py                    # UI/Entry point layer
models/
  └── room.py             # Entity/Domain layer
repositories/
  └── room_repository.py  # Data access layer (Repository pattern)
services/
  ├── booking_service.py  # Business logic layer
  └── payment_service.py  # Business logic layer
utils/
  └── constants.py        # Configuration/Constants
```

**Pembaruan:**
- Pemisahan concerns yang jelas
- Setiap layer punya responsibility yang jelas
- Mudah menemukan functionality spesifik
- Arsitektur yang dapat di-test
- Pola design yang scalable

---

#### **RESOLUSI 11: KISS (Keep It Simple, Stupid)**

**Sebelum:**
```python
if aksi == "1":
    diskon = input("pakai diskon? YA/TIDAK: ")
    total = yyy("VIP" if tipe == "A" else "B", diskon)

    if tipe == "C":
    
    for i in range(3):
        print("processing", i)
```

**Sesudah:**
```python
def main():
    try:
        name = input("Name: ").strip()
        room_type = input("Room type (VIP/STANDARD): ").upper()
        
        if room_type not in [VIP, STANDARD]:
            print("Invalid room type. Please use VIP or STANDARD")
            return
        
        if room_type == VIP:
            booking_service = VIPBookingService(repository)
        else:
            booking_service = StandardBookingService(repository)
        
        if not booking_service.check_availability(room_type):
            print("Room not available")
            return
        
        price = booking_service.book_room(room_type)
        
        payment_choice = display_payment_methods()
        payment_service = get_payment_service(payment_choice)
        use_discount = input("Use discount? (y/n): ").lower() == "y"
        total = payment_service.calculate_total(price, use_discount)
        
        print("\n--- RESULT ---")
        print("Name:", name)
        print("Room:", room_type)
        print("Total:", total)
        
    except Exception as error:
        print("Error:", error)
```

**Pembaruan:**
- Nesting minimal
- Method responsibility yang jelas
- Tidak ada over-engineering atau complexity
- Logika yang straightforward

**Dampak:** Kode yang readable dan lebih mudah dipahami

---