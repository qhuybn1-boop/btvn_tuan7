# Yêu cầu chức năng

## Mục tiêu
Triển khai phép nhân hai đa thức trong các trường hữu hạn GF(2^4) và GF(2^8), sử dụng đa thức tối giản đã chọn.

## Đa thức tối giản
- GF(2^4): p(x) = x^4 + x + 1
- GF(2^8): p(x) = x^8 + x^4 + x^3 + x + 1

## Yêu cầu
1. Mỗi đa thức hệ số 0/1 được biểu diễn bằng một số nguyên.
2. Cộng đa thức thực hiện bằng XOR.
3. Nhân đa thức thực hiện bằng phép nhân carry-less, sau đó rút gọn modulo p(x).
4. Chỉ chấp nhận đa thức tối giản để tạo trường GF(2^n).
5. Không cho phép các giá trị ngoài phạm vi của từng trường.
6. Cần hỗ trợ:
   - `mul()`
   - `mul_schoolbook()`
   - `add()`
   - `inv()`
   - `pow()`

## Tiêu chí nghiệm thu
- Kết quả của `mul()` và `mul_schoolbook()` phải giống nhau với mọi cặp phần tử hợp lệ.
- Phép nhân phải thỏa các tính chất giao hoán, kết hợp và phân phối.
- Mọi phần tử khác 0 đều phải có nghịch đảo.
- Đa thức không tối giản phải bị từ chối khi tạo trường.
- Ví dụ chuẩn AES phải cho kết quả 0x57 × 0x83 = 0xC1.
