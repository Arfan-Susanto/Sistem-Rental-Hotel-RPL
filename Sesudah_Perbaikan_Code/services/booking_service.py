from repositories.room_repository import RoomRepository
from utils.constants import VIP, STANDARD

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
        self.__booking_id_counter = 1000
        self.__bookings_history = []

    @property
    def repository(self):
        """
        Getter untuk repository yang digunakan service.
        
        Returns:
            RoomRepository: Repository instance yang digunakan
        """
        return self.__repository

    @property
    def bookings_history(self):
        """
        Getter untuk history semua booking yang telah dilakukan.
        
        Returns:
            list: List dictionary berisi history booking
        """
        return self.__bookings_history

    @property
    def booking_id_counter(self):
        """
        Getter untuk counter ID booking terkini.
        
        Returns:
            int: Nilai counter ID booking saat ini
        """
        return self.__booking_id_counter

    @repository.setter
    def repository(self, new_repository: RoomRepository):
        """
        Setter untuk mengubah repository yang digunakan service.
        Melakukan validasi untuk memastikan repository valid.
        
        Args:
            new_repository (RoomRepository): Repository baru yang akan digunakan
            
        Raises:
            TypeError: Jika parameter bukan instance RoomRepository
        """
        if not isinstance(new_repository, RoomRepository):
            raise TypeError("Repository must be instance of RoomRepository")
        self.__repository = new_repository

    def check_availability(self, room_type: str) -> bool:
        """
        Mengecek apakah kamar dengan tipe tertentu tersedia untuk dipesan.
        Berinteraksi dengan repository untuk mendapatkan status kamar.
        
        Args:
            room_type (str): Tipe kamar yang akan dicek (VIP/STANDARD)
            
        Returns:
            bool: True jika kamar tersedia, False jika sudah dipesan
        """
        room = self.__repository.get_room(room_type)
        return room.is_available

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
        self.__booking_id_counter += 1
        self.__bookings_history.append({
            "booking_id": self.__booking_id_counter,
            "room_type": room_type,
            "price": room.price
        })
        return room.price

    def cancel_booking(self, room_type: str) -> bool:
        """
        Membatalkan booking kamar dan membebaskan kamar untuk dipesan kembali.
        Mencatat history pembatalan booking.
        
        Args:
            room_type (str): Tipe kamar yang booking-nya akan dibatalkan
            
        Returns:
            bool: True jika pembatalan berhasil, False jika gagal
        """
        try:
            room = self.__repository.get_room(room_type)
            room.release()
            self.__bookings_history.append({
                "booking_id": self.__booking_id_counter,
                "room_type": room_type,
                "action": "CANCELLED"
            })
            return True
        except Exception:
            return False


class VIPBookingService(BookingService):
    """
    Child class untuk handling booking kamar VIP dengan fitur premium.
    Menyediakan layanan khusus dan diskon loyalty untuk member VIP.
    """

    def __init__(self, repository: RoomRepository):
        """
        Inisialisasi VIPBookingService dengan memanggil parent constructor.
        
        Args:
            repository (RoomRepository): Repository untuk akses data kamar
        """
        super().__init__(repository)

    def book_vip_room_with_concierge(self, guest_name: str, special_requests: list = None) -> dict:
        """
        Book kamar VIP dengan layanan concierge dan special requests.
        Memberikan pengalaman premium dengan fasilitas concierge service.
        
        Args:
            guest_name (str): Nama tamu yang melakukan booking
            special_requests (list): List permintaan khusus dari tamu
            
        Returns:
            dict: Dictionary berisi informasi booking VIP lengkap
            
        Raises:
            Exception: Jika kamar VIP tidak tersedia
        """
        if not self.check_availability(VIP):
            raise Exception("VIP room not available")

        price = self.book_room(VIP)
        booking_info = {
            "booking_id": self.booking_id_counter,
            "room_type": VIP,
            "guest_name": guest_name,
            "price": price,
            "concierge_service": True,
            "special_requests": special_requests or []
        }
        return booking_info

    def apply_vip_loyalty_discount(self, price: int, loyalty_points: int) -> int:
        """
        Apply loyalty discount untuk VIP member berdasarkan poin loyalitas.
        Semakin banyak poin, semakin besar diskon (max 20% dari harga).
        
        Args:
            price (int): Harga awal dalam Rupiah
            loyalty_points (int): Poin loyalitas member VIP
            
        Returns:
            int: Harga setelah diskon loyalitas diterapkan
        """
        discount = min(loyalty_points // 100, int(price * 0.2))
        return price - discount


class StandardBookingService(BookingService):
    """
    Child class untuk handling booking kamar Standard dengan berbagai paket.
    Menyediakan pilihan paket booking yang beragam untuk customer.
    """

    def __init__(self, repository: RoomRepository):
        """
        Inisialisasi StandardBookingService dengan memanggil parent constructor.
        
        Args:
            repository (RoomRepository): Repository untuk akses data kamar
        """
        super().__init__(repository)

    def book_standard_room_with_package(self, package_type: str = "BASIC") -> dict:
        """
        Book kamar Standard dengan berbagai pilihan paket (BASIC/BREAKFAST/FULL).
        Memberikan fleksibilitas memilih amenities sesuai kebutuhan budget.
        
        Args:
            package_type (str): Tipe paket (BASIC/BREAKFAST/FULL), default BASIC
            
        Returns:
            dict: Dictionary berisi informasi booking Standard dengan paket
            
        Raises:
            Exception: Jika kamar Standard tidak tersedia
        """
        if not self.check_availability(STANDARD):
            raise Exception("Standard room not available")

        price = self.book_room(STANDARD)
        packages = {
            "BASIC": {"amenities": ["Room Only"]},
            "BREAKFAST": {"amenities": ["Room + Breakfast"]},
            "FULL": {"amenities": ["Room + Breakfast + Dinner"]}
        }

        booking_info = {
            "booking_id": self.booking_id_counter,
            "room_type": STANDARD,
            "package": package_type,
            "amenities": packages.get(package_type, packages["BASIC"])["amenities"],
            "price": price
        }
        return booking_info

    def apply_group_booking_discount(self, num_rooms: int, price_per_room: int) -> int:
        """
        Apply group booking discount untuk multiple rooms (3+ rooms).
        Memberikan harga spesial ketika ada booking untuk grup.
        - 2 rooms: 5% diskon
        - 3-4 rooms: 10% diskon
        - 5+ rooms: 15% diskon
        
        Args:
            num_rooms (int): Jumlah kamar yang akan dipesan
            price_per_room (int): Harga per kamar dalam Rupiah
            
        Returns:
            int: Total harga setelah diskon grup diterapkan
        """
        if num_rooms >= 5:
            discount_rate = 0.15
        elif num_rooms >= 3:
            discount_rate = 0.10
        else:
            discount_rate = 0.05

        total_price = price_per_room * num_rooms
        return int(total_price * (1 - discount_rate))