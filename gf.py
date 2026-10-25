"""
Nhân hai đa thức trong trường hữu hạn GF(2^n), n = 4 và n = 8.

Quy ước biểu diễn: một đa thức hệ số trong {0,1} được lưu bằng MỘT SỐ NGUYÊN,
bit thứ i của số đó là hệ số của x^i.
    Ví dụ: x^3 + x + 1  <->  0b1011  = 11
"""


# ---------------------------------------------------------------------------
# 1. Các phép toán cơ bản trên đa thức hệ số GF(2)
# ---------------------------------------------------------------------------
def degree(p: int) -> int:
    """Bậc của đa thức (đa thức 0 trả về -1)."""
    return p.bit_length() - 1


def poly_str(p: int) -> str:
    """In đa thức dạng chữ, ví dụ 0b1011 -> 'x^3 + x + 1'."""
    if p == 0:
        return "0"
    terms = []
    for i in range(degree(p), -1, -1):
        if (p >> i) & 1:
            terms.append("1" if i == 0 else "x" if i == 1 else f"x^{i}")
    return " + ".join(terms)


def poly_add(a: int, b: int) -> int:
    """Cộng đa thức trong GF(2): cộng hệ số mod 2 = XOR."""
    return a ^ b


def clmul(a: int, b: int) -> int:
    """
    Nhân đa thức "thuần" (chưa rút gọn), còn gọi là carry-less multiplication.
    Với mỗi bit 1 ở vị trí i của b, ta cộng (XOR) vào kết quả a dịch trái i bit
    (nhân a với x^i). Kết quả có bậc tối đa deg(a) + deg(b).
    """
    result = 0
    while b:
        if b & 1:
            result ^= a
        a <<= 1
        b >>= 1
    return result


def poly_divmod(a: int, m: int):
    """Chia đa thức a cho m trong GF(2)[x], trả về (thương, dư)."""
    if m == 0:
        raise ZeroDivisionError("chia cho đa thức 0")
    dm = degree(m)
    quotient = 0
    while a and degree(a) >= dm:
        shift = degree(a) - dm
        quotient ^= 1 << shift
        a ^= m << shift  # trừ (= cộng = XOR) m * x^shift
    return quotient, a


def poly_mod(a: int, m: int) -> int:
    """Phần dư của a khi chia cho m."""
    return poly_divmod(a, m)[1]


def is_irreducible(p: int) -> bool:
    """
    Kiểm tra đa thức p có tối giản trên GF(2) không bằng cách thử chia
    cho mọi đa thức bậc từ 1 đến deg(p)//2. Nếu không chia hết cho cái nào
    thì p tối giản (đủ nhanh với bậc 4, 8).
    """
    n = degree(p)
    if n < 1:
        return False
    for d in range(1, n // 2 + 1):
        for c in range(1 << d, 1 << (d + 1)):  # mọi đa thức bậc đúng d
            if poly_mod(p, c) == 0:
                return False
    return True


# ---------------------------------------------------------------------------
# 2. Trường GF(2^n)
# ---------------------------------------------------------------------------
class GF2n:
    """
    GF(2^n) = các đa thức bậc < n, phép nhân lấy mod đa thức tối giản `irr`.
    """

    def __init__(self, n: int, irr: int):
        if degree(irr) != n:
            raise ValueError(f"Đa thức tối giản phải có bậc {n}")
        if not is_irreducible(irr):
            raise ValueError(f"'{poly_str(irr)}' KHÔNG tối giản -> không tạo thành trường")
        self.n = n
        self.irr = irr
        self.size = 1 << n

    def _check(self, a: int):
        if not 0 <= a < self.size:
            raise ValueError(f"{a} không thuộc GF(2^{self.n})")

    # Cách 1: nhân đầy đủ rồi mới chia lấy dư (đúng theo định nghĩa toán học)
    def mul_schoolbook(self, a: int, b: int) -> int:
        self._check(a)
        self._check(b)
        return poly_mod(clmul(a, b), self.irr)

    # Cách 2: dịch-và-cộng, rút gọn ngay từng bước (kiểu "xtime" của AES)
    def mul(self, a: int, b: int) -> int:
        self._check(a)
        self._check(b)
        result = 0
        while b:
            if b & 1:
                result ^= a
            b >>= 1
            a <<= 1                  # a = a * x
            if (a >> self.n) & 1:    # bậc đạt n -> tràn, trừ bớt đa thức tối giản
                a ^= self.irr
        return result

    def add(self, a: int, b: int) -> int:
        self._check(a)
        self._check(b)
        return a ^ b

    def pow(self, a: int, e: int) -> int:
        result, base = 1, a
        while e:
            if e & 1:
                result = self.mul(result, base)
            base = self.mul(base, base)
            e >>= 1
        return result

    def inv(self, a: int) -> int:
        """Nghịch đảo: a^(2^n - 2), vì a^(2^n - 1) = 1 với a != 0."""
        if a == 0:
            raise ZeroDivisionError("0 không có nghịch đảo")
        return self.pow(a, self.size - 2)

    def trace_mul(self, a: int, b: int) -> int:
        """Nhân và in từng bước để dễ hiểu / đưa vào báo cáo."""
        print(f"a = {poly_str(a)}  ({a:0{self.n}b})")
        print(f"b = {poly_str(b)}  ({b:0{self.n}b})")
        full = clmul(a, b)
        print(f"a*b (chưa rút gọn) = {poly_str(full)}  ({full:b})")
        q, r = poly_divmod(full, self.irr)
        print(f"chia cho {poly_str(self.irr)}: thương = {poly_str(q)}, dư = {poly_str(r)}")
        print(f"==> a*b mod p = {poly_str(r)}  ({r:0{self.n}b})\n")
        return r


# Đa thức tối giản được chọn
IRR_GF16 = 0b10011        # x^4 + x + 1
IRR_GF256 = 0b100011011   # x^8 + x^4 + x^3 + x + 1 (đa thức của AES)

GF16 = GF2n(4, IRR_GF16)
GF256 = GF2n(8, IRR_GF256)


def main():
    print("=== GF(2^4), p(x) = x^4 + x + 1 ===")
    GF16.trace_mul(0b1011, 0b0101)       # (x^3+x+1)(x^2+1)

    print("=== GF(2^8), p(x) = x^8 + x^4 + x^3 + x + 1 ===")
    GF256.trace_mul(0x57, 0x83)          # ví dụ chuẩn của AES, kết quả 0xC1

    print("Bảng nhân GF(2^4) (hex):")
    print("    " + " ".join(f"{j:X}" for j in range(16)))
    for i in range(16):
        print(f"{i:X} | " + " ".join(f"{GF16.mul(i, j):X}" for j in range(16)))


if __name__ == "__main__":
    main()
