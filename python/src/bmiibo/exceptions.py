class BmiiboError(Exception):
    """所有 bmiibo 套件錯誤的基底"""
    pass

class FileTooLargeError(BmiiboError):
    """檔案超過 5MB 安全防線時觸發"""
    pass

class InvalidFormatError(BmiiboError):
    """壓縮檔結構毀損或少檔案時觸發"""
    pass

class DailyLimitExceededError(BmiiboError):
    """觸發防刷機制：當天已經讀取過該玩具"""
    pass
