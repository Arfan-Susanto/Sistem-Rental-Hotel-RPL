from utils.constants import DISCOUNT_AMOUNT
from abc import ABC, abstractmethod


class PaymentService(ABC):
    """
    Abstract Base Class untuk menangani perhitungan pembayaran.
    Terpisah dari booking agar mengikuti prinsip Single Responsibility.
    Mendefinisikan interface untuk semua payment methods yang tersedia.
    Menggunakan pola Abstract Factory untuk extensibility.
    """

    def __init__(self):
        """
        Inisialisasi PaymentService dengan history dan fee percentage.
        """
        self.__transaction_history = []
        self.__fee_percentage = 0

    @property
    def transaction_history(self):
        """
        Getter untuk history semua transaksi pembayaran.
        
        Returns:
            list: List dictionary berisi history transaksi
        """
        return self.__transaction_history

    @property
    def fee_percentage(self):
        """
        Getter untuk persentase fee dari payment method.
        
        Returns:
            float: Persentase fee (0.03 = 3%)
        """
        return self.__fee_percentage

    @fee_percentage.setter
    def fee_percentage(self, value: float):
        """
        Setter untuk persentase fee dengan validasi non-negatif.
        
        Args:
            value (float): Persentase fee baru dalam bentuk desimal
            
        Raises:
            ValueError: Jika fee percentage negatif
        """
        if value < 0:
            raise ValueError("Fee percentage cannot be negative")
        self.__fee_percentage = value

    def calculate_total(self, price: int, use_discount: bool = False) -> int:
        """
        Menghitung total pembayaran dengan aplikasi diskon dan fee.
        
        Args:
            price (int): Harga awal dalam Rupiah
            use_discount (bool): Apakah diskon akan diaplikasikan
            
        Returns:
            int: Total harga yang harus dibayar (dengan fee)
        """
        total = price
        if use_discount:
            total -= DISCOUNT_AMOUNT
        total = self.__apply_fee(total)
        return total

    def __apply_fee(self, amount: int) -> int:
        """
        Private method untuk mengaplikasikan fee berdasarkan payment method.
        
        Args:
            amount (int): Jumlah yang akan dikenai fee
            
        Returns:
            int: Jumlah setelah ditambah fee
        """
        return self._apply_fee(amount)

    @abstractmethod
    def _apply_fee(self, amount: int) -> int:
        """
        Abstract method yang harus diimplementasi oleh child class.
        Menentukan cara aplikasi fee untuk payment method spesifik.
        
        Args:
            amount (int): Jumlah yang akan dikenai fee
            
        Returns:
            int: Jumlah setelah ditambah fee
        """
        pass

    @abstractmethod
    def process_payment(self, amount: int, reference_id: str = None) -> dict:
        """
        Abstract method untuk proses pembayaran dengan method spesifik.
        Harus diimplementasi oleh setiap child class.
        
        Args:
            amount (int): Jumlah pembayaran dalam Rupiah
            reference_id (str): Reference ID untuk tracking pembayaran
            
        Returns:
            dict: Dictionary berisi detail transaksi
        """
        pass


class CashPayment(PaymentService):
    """
    Child class untuk pembayaran tunai/cash.
    Method pembayaran paling sederhana tanpa fee tambahan.
    Cocok untuk transaksi langsung di lokasi hotel.
    """

    def __init__(self):
        """
        Inisialisasi CashPayment dengan fee 0% karena tidak ada biaya proses.
        """
        super().__init__()
        self._PaymentService__fee_percentage = 0

    def _apply_fee(self, amount: int) -> int:
        """
        Tidak menerapkan fee untuk pembayaran tunai.
        
        Args:
            amount (int): Jumlah pembayaran
            
        Returns:
            int: Jumlah yang sama tanpa penambahan fee
        """
        return amount

    def process_payment(self, amount: int, reference_id: str = None) -> dict:
        """
        Proses pembayaran tunai dan catat dalam transaction history.
        
        Args:
            amount (int): Jumlah pembayaran dalam Rupiah
            reference_id (str): Reference ID untuk tracking (optional)
            
        Returns:
            dict: Dictionary berisi detail transaksi cash
        """
        payment_data = {
            "method": "CASH",
            "amount": amount,
            "fee": 0,
            "total": amount,
            "status": "COMPLETED",
            "timestamp": None
        }
        self._PaymentService__transaction_history.append(payment_data)
        return payment_data


class CreditCardPayment(PaymentService):
    """
    Child class untuk pembayaran dengan Kartu Kredit.
    Mendukung berbagai bank dengan fee processing 3%.
    Proses pembayaran lebih lama karena verifikasi dari issuer bank.
    """

    def __init__(self):
        """
        Inisialisasi CreditCardPayment dengan fee 3% dan supported banks.
        """
        super().__init__()
        self._PaymentService__fee_percentage = 0.03
        self.__supported_banks = ["BCA", "Mandiri", "BNI", "CIMB"]

    @property
    def supported_banks(self):
        """
        Getter untuk daftar bank yang didukung.
        
        Returns:
            list: Daftar nama bank yang support pembayaran
        """
        return self.__supported_banks

    def _apply_fee(self, amount: int) -> int:
        """
        Mengaplikasikan fee 3% untuk pembayaran credit card.
        
        Args:
            amount (int): Jumlah pembayaran
            
        Returns:
            int: Jumlah setelah ditambah fee 3%
        """
        fee = int(amount * self._PaymentService__fee_percentage)
        return amount + fee

    def process_payment(self, amount: int, bank_name: str = None, reference_id: str = None) -> dict:
        """
        Proses pembayaran credit card dengan validasi bank support.
        
        Args:
            amount (int): Jumlah pembayaran dalam Rupiah
            bank_name (str): Nama bank issuer kartu kredit
            reference_id (str): Reference ID untuk tracking
            
        Returns:
            dict: Dictionary berisi detail transaksi credit card
            
        Raises:
            ValueError: Jika bank tidak didukung
        """
        if bank_name and bank_name not in self.__supported_banks:
            raise ValueError(f"Bank not supported. Supported: {self.__supported_banks}")

        fee = int(amount * self._PaymentService__fee_percentage)
        total = amount + fee

        payment_data = {
            "method": "CREDIT_CARD",
            "bank": bank_name or "UNKNOWN",
            "amount": amount,
            "fee": fee,
            "total": total,
            "status": "PROCESSING",
            "reference_id": reference_id or "CC" + str(len(self._PaymentService__transaction_history) + 1),
            "timestamp": None
        }
        self._PaymentService__transaction_history.append(payment_data)
        return payment_data


class QRISPayment(PaymentService):
    """
    Child class untuk pembayaran dengan QRIS (Quick Response Code Indonesian Standard).
    Standard pembayaran digital Indonesia yang cepat dan aman.
    Biaya rendah (1%) membuat QRIS sangat kompetitif untuk e-commerce.
    """

    def __init__(self):
        """
        Inisialisasi QRISPayment dengan fee 1% dan default QRIS code length.
        """
        super().__init__()
        self._PaymentService__fee_percentage = 0.01
        self.__qris_code_length = 32

    def _apply_fee(self, amount: int) -> int:
        """
        Mengaplikasikan fee 1% untuk pembayaran QRIS.
        
        Args:
            amount (int): Jumlah pembayaran
            
        Returns:
            int: Jumlah setelah ditambah fee 1%
        """
        fee = int(amount * self._PaymentService__fee_percentage)
        return amount + fee

    def generate_qris_code(self, amount: int) -> str:
        """
        Generate QRIS code unik untuk transaksi pembayaran.
        QRIS code berisi informasi pembayaran yang bisa di-scan.
        
        Args:
            amount (int): Jumlah pembayaran dalam Rupiah
            
        Returns:
            str: QRIS code dalam format hexadecimal
        """
        import hashlib
        code_str = f"QRIS{amount}{len(self._PaymentService__transaction_history)}"
        qris_code = hashlib.md5(code_str.encode()).hexdigest()[:self.__qris_code_length]
        return qris_code

    def process_payment(self, amount: int, reference_id: str = None) -> dict:
        """
        Proses pembayaran QRIS dan generate QRIS code untuk scan.
        
        Args:
            amount (int): Jumlah pembayaran dalam Rupiah
            reference_id (str): Reference ID untuk tracking
            
        Returns:
            dict: Dictionary berisi detail transaksi QRIS dan QRIS code
        """
        fee = int(amount * self._PaymentService__fee_percentage)
        total = amount + fee
        qris_code = self.generate_qris_code(amount)

        payment_data = {
            "method": "QRIS",
            "amount": amount,
            "fee": fee,
            "total": total,
            "qris_code": qris_code,
            "status": "PENDING",
            "reference_id": reference_id or "QR" + str(len(self._PaymentService__transaction_history) + 1),
            "timestamp": None
        }
        self._PaymentService__transaction_history.append(payment_data)
        return payment_data


class EWalletPayment(PaymentService):
    """
    Child class untuk pembayaran dengan E-Wallet (dompet digital).
    Mendukung berbagai e-wallet populer di Indonesia dan Asia Tenggara.
    Pembayaran instant dengan fee kompetitif 1.5%.
    """

    def __init__(self):
        """
        Inisialisasi EWalletPayment dengan fee 1.5% dan daftar e-wallet support.
        """
        super().__init__()
        self._PaymentService__fee_percentage = 0.015
        self.__supported_wallets = ["GCash", "OVO", "Dana", "LinkAja", "iPaymu"]
        self.__wallet_balance = {}

    @property
    def supported_wallets(self):
        """
        Getter untuk daftar e-wallet yang didukung.
        
        Returns:
            list: Daftar nama e-wallet yang support pembayaran
        """
        return self.__supported_wallets

    @property
    def wallet_balance(self):
        """
        Getter untuk melihat balance semua wallet.
        
        Returns:
            dict: Dictionary berisi balance setiap e-wallet
        """
        return self.__wallet_balance

    def set_wallet_balance(self, wallet_name: str, balance: int) -> None:
        """
        Set balance untuk e-wallet dengan validasi.
        Memastikan balance positif dan wallet supported.
        
        Args:
            wallet_name (str): Nama e-wallet (GCash/OVO/Dana/LinkAja/iPaymu)
            balance (int): Balance dalam Rupiah
            
        Raises:
            ValueError: Jika wallet tidak supported atau balance negatif
        """
        if wallet_name not in self.__supported_wallets:
            raise ValueError(f"Wallet not supported. Supported: {self.__supported_wallets}")
        if balance < 0:
            raise ValueError("Balance cannot be negative")
        self.__wallet_balance[wallet_name] = balance

    def _apply_fee(self, amount: int) -> int:
        """
        Mengaplikasikan fee 1.5% untuk pembayaran e-wallet.
        
        Args:
            amount (int): Jumlah pembayaran
            
        Returns:
            int: Jumlah setelah ditambah fee 1.5%
        """
        fee = int(amount * self._PaymentService__fee_percentage)
        return amount + fee

    def process_payment(self, amount: int, wallet_name: str = None, reference_id: str = None) -> dict:
        """
        Proses pembayaran e-wallet dengan validasi balance.
        Mengurangi balance wallet setelah pembayaran berhasil.
        
        Args:
            amount (int): Jumlah pembayaran dalam Rupiah
            wallet_name (str): Nama e-wallet yang digunakan
            reference_id (str): Reference ID untuk tracking
            
        Returns:
            dict: Dictionary berisi detail transaksi e-wallet
            
        Raises:
            ValueError: Jika wallet tidak supported atau balance kurang
        """
        if not wallet_name or wallet_name not in self.__supported_wallets:
            raise ValueError(f"Wallet not supported. Supported: {self.__supported_wallets}")

        balance = self.__wallet_balance.get(wallet_name, 0)
        fee = int(amount * self._PaymentService__fee_percentage)
        total = amount + fee

        if balance < total:
            raise ValueError(f"Insufficient balance. Required: {total}, Available: {balance}")

        self.__wallet_balance[wallet_name] -= total

        payment_data = {
            "method": "E_WALLET",
            "wallet": wallet_name,
            "amount": amount,
            "fee": fee,
            "total": total,
            "remaining_balance": self.__wallet_balance[wallet_name],
            "status": "COMPLETED",
            "reference_id": reference_id or "EW" + str(len(self._PaymentService__transaction_history) + 1),
            "timestamp": None
        }
        self._PaymentService__transaction_history.append(payment_data)
        return payment_data


class BankTransferPayment(PaymentService):
    """
    Child class untuk pembayaran dengan Transfer Bank.
    Method pembayaran tradisional dengan biaya murah (0.5%).
    Proses lebih lama karena clearing bank, tapi sangat aman dan terpercaya.
    """

    def __init__(self):
        """
        Inisialisasi BankTransferPayment dengan fee 0.5% dan supported banks.
        """
        super().__init__()
        self._PaymentService__fee_percentage = 0.005
        self.__supported_banks = ["BCA", "Mandiri", "BNI", "CIMB", "Permata"]
        self.__bank_accounts = {}

    @property
    def supported_banks(self):
        """
        Getter untuk daftar bank yang didukung untuk transfer.
        
        Returns:
            list: Daftar nama bank yang support transfer pembayaran
        """
        return self.__supported_banks

    def register_bank_account(self, bank_name: str, account_number: str) -> None:
        """
        Register rekening bank tujuan untuk menerima transfer.
        Hanya mendukung bank-bank tertentu.
        
        Args:
            bank_name (str): Nama bank tujuan (BCA/Mandiri/BNI/CIMB/Permata)
            account_number (str): Nomor rekening tujuan
            
        Raises:
            ValueError: Jika bank tidak didukung
        """
        if bank_name not in self.__supported_banks:
            raise ValueError(f"Bank not supported. Supported: {self.__supported_banks}")
        self.__bank_accounts[bank_name] = account_number

    def _apply_fee(self, amount: int) -> int:
        """
        Mengaplikasikan fee 0.5% untuk pembayaran bank transfer.
        
        Args:
            amount (int): Jumlah pembayaran
            
        Returns:
            int: Jumlah setelah ditambah fee 0.5%
        """
        fee = int(amount * self._PaymentService__fee_percentage)
        return amount + fee

    def process_payment(self, amount: int, destination_bank: str = None, reference_id: str = None) -> dict:
        """
        Proses pembayaran transfer bank ke rekening tujuan.
        Status awalnya PENDING sampai transfer selesai di clearing bank.
        
        Args:
            amount (int): Jumlah pembayaran dalam Rupiah
            destination_bank (str): Bank tujuan transfer (BCA/Mandiri/BNI/CIMB/Permata)
            reference_id (str): Reference ID untuk tracking
            
        Returns:
            dict: Dictionary berisi detail transaksi bank transfer
            
        Raises:
            ValueError: Jika bank tujuan tidak didukung
        """
        if not destination_bank or destination_bank not in self.__supported_banks:
            raise ValueError(f"Bank not supported. Supported: {self.__supported_banks}")

        fee = int(amount * self._PaymentService__fee_percentage)
        total = amount + fee

        payment_data = {
            "method": "BANK_TRANSFER",
            "destination_bank": destination_bank,
            "destination_account": self.__bank_accounts.get(destination_bank, "UNKNOWN"),
            "amount": amount,
            "fee": fee,
            "total": total,
            "status": "PENDING",
            "reference_id": reference_id or "BT" + str(len(self._PaymentService__transaction_history) + 1),
            "timestamp": None
        }
        self._PaymentService__transaction_history.append(payment_data)
        return payment_data