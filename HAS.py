import string as st
import hashlib
class HASHash:
    """
        Hashing . Algorithm. Simple
        ---------------------------
    """
    def __init__(self, value):
        self.value = value

    def hexdigest(self, b=None):
        if b is None:
            return hex(self.value).strip("0x")
        return hex(self.value).strip("0x")[0:b]


    def digest(self):
        return self.value

    @staticmethod
    def HASS(message):
        chars = st.ascii_letters + st.digits + st.punctuation + ' '
        shuffled = ['9', 'n', '5', '<', '0', 'W', '_', '\\', '2', 'e', '(', 'u', "'", 'f', '~', 'y', 'v', 'U', 'O', 'N', 'm', 'F', '[', '+', 'i', 'Y', 'T', ':', 'B', 'Q', 'R', 'I', 'z', '?', 'L', 'j', '1', '*', ' ', 'J', 'q', 'r', 'X', '%', 'Z', '{', '7', 'h', 's', ';', '-', '!', 'b', 'M', 'k', 'c', '|', 'd', '&', 'V', 'l', 'P', '"', 'C', '@', 'H', 'a', '4', 'w', '=', 'x', '.', ',', '8', '6', 'G', 'g', 'A', '`', 't', ')', '#', '^', '/', '3', 'E', '$', '}', 'o', 'p', '>', 'D', 'S', 'K', ']']
        return_str = ''
        for ch in message:
            if ch not in shuffled or ch not in chars: continue
            index = chars.index(ch)
            return_str += shuffled[index]
            for i in range(0, ord(ch)):
                first = shuffled.pop(0)
                shuffled.append(first)
        s = ''
        for c in return_str:
            s += str(ord(c)**ord(c))
        if len(s) > 0:
            last = int(s)
        else:
            last = 1
        return HASHash(last)

    @staticmethod
    def HAS(message: str):
        """
            The HAS function takes a string and returns a HASHash object.
        """
        en = st.ascii_letters + st.digits + st.punctuation
        padding = '01110011 00110011 11000110 10001101 01100111 00010001 00001110 11100100 11111100 11010111 10010111 00001111 01100111 10010100 11100101 00010100 00010110 11101011 00111110 01110000 00010000 00010100 11111110 11000101 11000011 00000100 01011011 01100010 01101000 10001001 00110000 11100000 00000100 00000010 01001111 00110011 11110101 01010101 11011111 00011010 01010101 01100110 10110110 11110110 00000000 11011111 11101100 01011100 11111110 11111011 11011100 00010001 00100100 00101100 11101100 11000111 10110111 11000100 10001010 11101111 00010010 00101011 11000111'
        padding_list = padding.split(" ")
        om = []
        shaffle_list = ['p', 'P', '{', 'D', '=', 'F', 'l', 'f', '@', 'b', 'k', '5', 'M', 'H', ':', 'U', '[', 'A', 'u', '`', 'w', "'", '1', 'S', '~', '^', '"', 'L', '3', '#', 'C', '!', '\\', 'a', 'y', 'Q', 'X', 'v', '4', '2', 'V', 'g', 'h', 'n', 'R', 'B', 'I', '|', 'O', 'W', 'd', ' ', 'T', 'G', '/', 'o', '&', ']', 'Y', 'E', '<', 'z', '?', '$', '9', 't', '}', '7', 'm', ';', '.', 's', '-', '0', 'r', ')', '8', '+', 'Z', ',', '%', 'e', 'q', '6', 'N', '>', 'x', 'c', '*', 'K', 'J', 'i', '(', 'j', '_']
        for c in message:
            try:
                index = en.index(c)
                om.append(shaffle_list[index])
            except ValueError:
                om.append(c)
            for i in range(0, ord(c)**2):
                first = shaffle_list.pop(0)
                shaffle_list.append(first)
        bm = [format(ord(c), 'b') for c in om]
        amount_to_shift = len(padding_list) - len(bm)
        if amount_to_shift <= 0: amount_to_shift *= -1
        shift_must = ord(om[0]) if len(om) > 0 else 153
        amount_to_shift += shift_must
        for i, b in enumerate(padding_list):
            bm.append(b)
        key = bm.copy()
        for i in range(0, amount_to_shift):
            first = key.pop(0)
            key.append(first)
        if key == bm:
            first = key.pop(0)
            key.append(first)
        bm = list(int(c, 2) for c in bm)
        key = list(int(c, 2) for c in key)
        xored = []
        for i in range(len(bm)):
            xored.append(bm[i] ^ key[i])
        s_xored = [str(n) for n in xored]
        s = ''
        for string in s_xored:
            s += string.strip("-")
        last_int = int(s)
        return HASHash(last_int)

if __name__ == '__main__':
    while True:
        m = input("Message\n")
        n_bits = input('You can put the length that you want in hexdigest(n_bits), for 512 put 128, 1/4:\n')
        if n_bits.isspace() or n_bits == '': n_bits = 128
        n_bits = int(n_bits)
        h = HASHash.HAS(m).hexdigest(n_bits)
        h1 = HASHash.HASS(m).hexdigest(n_bits)
        print(f"HAS:\n{h}")
        print(f"HASS:\n{h1}")
        h2 = hashlib.sha512(m.encode()).hexdigest()
        print(f"Sha512:\n{h2}")
