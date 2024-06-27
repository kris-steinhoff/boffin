class Base62:
    base_alphabet = tuple(
        "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    )
    base_dict = dict((c, v) for v, c in enumerate(base_alphabet))
    base_len = len(base_alphabet)

    def decode(self, string: str) -> int:
        num = 0
        for char in string:
            num = num * self.base_len + self.base_dict[char]
        return num

    def encode(self, num: int) -> str:
        if not num:
            return self.base_alphabet[0]

        encoding = ""
        while num:
            num, rem = divmod(num, self.base_len)
            encoding = self.base_alphabet[rem] + encoding
        return encoding
