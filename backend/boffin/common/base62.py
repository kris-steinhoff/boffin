class Base62:
    base_alphabet = tuple(
        "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    )
    base_dict = dict((c, v) for v, c in enumerate(base_alphabet))
    base_len = len(base_alphabet)

    @classmethod
    def decode(cls, string: str) -> int:
        num = 0
        for char in string:
            num = num * cls.base_len + cls.base_dict[char]
        return num

    @classmethod
    def encode(cls, num: int) -> str:
        if not num:
            return cls.base_alphabet[0]

        encoding = ""
        while num:
            num, rem = divmod(num, cls.base_len)
            encoding = cls.base_alphabet[rem] + encoding
        return encoding
