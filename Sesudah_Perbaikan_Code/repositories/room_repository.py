from models.room import Room, VIPRoom, StandardRoom
from utils.constants import VIP, STANDARD

class RoomRepository:
    """
    Repository bertanggung jawab untuk penyimpanan & akses data Room.
    Mengimplementasikan pola Repository untuk memisahkan data access logic.
    Saat ini menggunakan in-memory storage (dictionary).
    Bisa diganti ke database tanpa mengubah business logic.
    Base class untuk berbagai tipe repository.
    """

    def __init__(self):
        """
        Inisialisasi repository dengan mengisi data kamar default.
        Membuat instance VIPRoom dan StandardRoom yang akan dikelola.
        """
        self.__rooms = {
            VIP: VIPRoom(),
            STANDARD: StandardRoom()
        }

    @property
    def rooms(self):
        """
        Getter untuk mendapatkan semua rooms yang tersimpan.
        
        Returns:
            dict: Dictionary berisi semua room objects
        """
        return self.__rooms

    def get_room(self, room_type: str) -> Room:
        """
        Mengambil objek Room berdasarkan tipe yang diminta.
        Validasi dilakukan untuk mencegah akses data tidak valid.
        
        Args:
            room_type (str): Tipe kamar yang dicari (VIP/STANDARD)
            
        Returns:
            Room: Objek kamar yang diminta
            
        Raises:
            ValueError: Jika tipe kamar tidak valid/tidak ditemukan
        """
        if room_type not in self.__rooms:
            raise ValueError("Invalid room type")
        return self.__rooms[room_type]

    def set_room_availability(self, room_type: str, is_available: bool) -> None:
        """
        Set ketersediaan kamar secara manual melalui repository.
        Memungkinkan perubahan status kamar dari luar.
        
        Args:
            room_type (str): Tipe kamar yang akan diubah statusnya
            is_available (bool): Status ketersediaan baru
        """
        room = self.get_room(room_type)
        room.is_available = is_available

    def update_room_price(self, room_type: str, new_price: int) -> None:
        """
        Update harga kamar melalui repository.
        Memungkinkan perubahan harga dinamis untuk pricing strategy.
        
        Args:
            room_type (str): Tipe kamar yang akan diubah harganya
            new_price (int): Harga baru dalam Rupiah
        """
        room = self.get_room(room_type)
        room.price = new_price

    def get_available_rooms(self):
        """
        Mendapatkan list semua kamar yang saat ini tersedia.
        Berguna untuk menampilkan pilihan kamar kepada customer.
        
        Returns:
            list: Daftar objek Room yang tersedia
        """
        return [room for room in self.__rooms.values() if room.is_available]

    def reset_all_rooms(self) -> None:
        """
        Reset semua kamar menjadi tersedia.
        Biasanya digunakan untuk reset sistem atau maintenance.
        """  
        for room in self.__rooms.values():
            room.release()

class VIPRoomRepository(RoomRepository):
    """
    Child class repository khusus untuk mengelola kamar VIP.
    Menyediakan interface spesifik dengan fitur premium untuk kamar VIP.
    Mengimplementasikan business logic khusus VIP seperti surge pricing.
    """

    def __init__(self):
        """
        Inisialisasi VIPRoomRepository dengan memanggil parent constructor.
        """
        super().__init__()

    def get_vip_facilities(self):
        """
        Mendapatkan daftar fasilitas kamar VIP.
        Menampilkan semua amenities premium yang tersedia di kamar VIP.
        
        Returns:
            list: Daftar fasilitas premium kamar VIP
        """
        vip_room = self.get_room(VIP)
        return vip_room.facilities if hasattr(vip_room, 'facilities') else []

    def update_vip_price_with_surge(self, surge_percentage: float) -> None:
        """
        Update harga VIP dengan surge pricing untuk periode high demand.
        Menerapkan strategi pricing dinamis ketika permintaan tinggi.
        
        Args:
            surge_percentage (float): Persentase kenaikan harga (0.1 = 10%)
        """
        vip_room = self.get_room(VIP)
        original_price = vip_room.price
        surged_price = int(original_price * (1 + surge_percentage))
        vip_room.price = surged_price

class StandardRoomRepository(RoomRepository):
    """
    Child class repository khusus untuk mengelola kamar Standard.
    Menyediakan interface spesifik dengan fitur ekonomis untuk kamar Standard.
    Mengimplementasikan business logic khusus Standard seperti promotional discount.
    """

    def __init__(self):
        """
        Inisialisasi StandardRoomRepository dengan memanggil parent constructor.
        """
        super().__init__()

    def get_standard_facilities(self):
        """
        Mendapatkan daftar fasilitas kamar Standard.
        Menampilkan semua amenities dasar yang tersedia di kamar Standard.
        
        Returns:
            list: Daftar fasilitas dasar kamar Standard
        """
        standard_room = self.get_room(STANDARD)
        return standard_room.facilities if hasattr(standard_room, 'facilities') else []

    def apply_promotional_discount(self, discount_percentage: float) -> None:
        """
        Apply promo diskon pada harga Standard untuk periode promosi.
        Menerapkan strategi pricing yang kompetitif untuk room Standard.
        
        Args:
            discount_percentage (float): Persentase diskon (0.1 = 10%)
        """
        standard_room = self.get_room(STANDARD)
        original_price = standard_room.price
        discounted_price = int(original_price * (1 - discount_percentage))
        standard_room.price = discounted_price