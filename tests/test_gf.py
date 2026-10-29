"""Kiểm thử: chạy bằng `python tests/test_gf.py` (không cần cài thêm thư viện)."""
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from gf import GF16, GF256, GF2n, is_irreducible, clmul, poly_mod


def test_known_values():
    # Ví dụ chuẩn trong tài liệu AES (FIPS-197): {57} * {83} = {c1}
    assert GF256.mul(0x57, 0x83) == 0xC1
    assert GF256.mul(0x57, 0x13) == 0xFE
    # GF(16), x^4+x+1: (x^3+x+1)(x^2+1) = x^5+x^3+x^2+x^3+x+1 ... tự tính bằng tay
    assert GF16.mul(0b0010, 0b1000) == 0b0011   # x * x^3 = x^4 = x + 1


def test_two_algorithms_agree():
    for field in (GF16, GF256):
        for a in range(field.size):
            for b in range(field.size):
                assert field.mul(a, b) == field.mul_schoolbook(a, b)


def test_field_axioms():
    for field in (GF16, GF256):
        rnd = random.Random(1)
        for _ in range(2000):
            a, b, c = (rnd.randrange(field.size) for _ in range(3))
            assert field.mul(a, b) == field.mul(b, a)                          # giao hoán
            assert field.mul(field.mul(a, b), c) == field.mul(a, field.mul(b, c))  # kết hợp
            assert field.mul(a, field.add(b, c)) == field.add(field.mul(a, b), field.mul(a, c))  # phân phối
            assert field.mul(a, 1) == a
            assert field.mul(a, 0) == 0
        # mọi phần tử khác 0 đều có nghịch đảo -> đây thực sự là một TRƯỜNG
        for a in range(1, field.size):
            assert field.mul(a, field.inv(a)) == 1


def test_irreducibility_checker():
    assert is_irreducible(0b10011)        # x^4+x+1
    assert is_irreducible(0b11001)        # x^4+x^3+1
    assert not is_irreducible(0b10001)    # x^4+1 = (x+1)^4
    assert not is_irreducible(0b10101)    # x^4+x^2+1 = (x^2+x+1)^2
    assert is_irreducible(0x11B)          # x^8+x^4+x^3+x+1
    assert is_irreducible(0x11D)          # x^8+x^4+x^3+x^2+1 (đa thức khác cũng được)
    assert not is_irreducible(0x101)      # x^8+1
    # Đếm: có đúng 3 đa thức tối giản bậc 4 và 30 đa thức tối giản bậc 8
    assert sum(is_irreducible(p) for p in range(1 << 4, 1 << 5)) == 3
    assert sum(is_irreducible(p) for p in range(1 << 8, 1 << 9)) == 30


def test_reducible_is_not_a_field():
    # Nếu dùng đa thức KHÔNG tối giản thì xuất hiện ước của 0: a*b = 0 với a,b != 0
    irr = 0b10101  # x^4+x^2+1 = (x^2+x+1)^2
    a = 0b0111     # x^2+x+1
    assert poly_mod(clmul(a, a), irr) == 0
    try:
        GF2n(4, irr)
        raise AssertionError("lẽ ra phải báo lỗi")
    except ValueError:
        pass


def test_other_irreducible_gives_isomorphic_but_different_table():
    other = GF2n(8, 0x11D)
    assert other.mul(0x57, 0x83) != GF256.mul(0x57, 0x83)  # kết quả phụ thuộc đa thức!


if __name__ == "__main__":
    tests = [v for k, v in dict(globals()).items() if k.startswith("test_")]
    for t in tests:
        t()
        print("OK ", t.__name__)
    print(f"\nTất cả {len(tests)} test đều đạt.")
