# BÀI TOÁN 8 PUZZLE SOLVE

---

## 1. Mục tiêu

Xây dựng một ứng dụng giao diện trực quan giải quyết bài toán 8-Puzzle, cho phép so sánh nhiều thuật toán tìm kiếm và học tập, bao gồm các nhóm: tìm kiếm không thông tin, có thông tin, local search, CSP, reinforcement learning, và tìm kiếm trong môi trường phức tạp.

### 1.1. Các nhóm thuật toán
Trong bài gồm có 6 nhóm thuật toán
- Tìm kiếm không có thông tin( Uninformed Search): BFS, DFS, IDS, UCS
- Tím kiếm có thông tin (Informed Search): Greedy Best_First Search, A*, IDA*
- Tìm kiếm cục bộ (local): Simple Hill Climbing, Steepest Ascent Hill Climbing, Stochastic Hill Climbing, Beam Search, Genetic Algorithm
- Tìm kiếm trong môi trường phức tạp (Search in Complex Environment): And-Or Search, Belief state, Partially Search
- Tìm kiếm trong môi trường không có ràng buộc (Constraint Satisfaction Problem): Backtracking, AC-3 Algorithms Search, Forward Checking
- Học tăng cường (Reinforcement Learning): Q-Learning

Các nhóm thuật toán dùng để giải bài toán 8 - Puzzle, mỗi nhóm đều có điểm mạnh, điểm yếu và điểm chung giữa các thuật toán chung 1 nhóm.

### 1.2. Mục tiêu của bài tập

Hiểu bản chất của từng nhóm thuật toán, điểm chung, điểm mạnh, điểm yếu của từng nhóm. So sánh hiệu năng và tính phù hợp

Hiểu sự khác biệt về:
- Hiệu quả thời gian và bộ nhớ
- Độ chính xác của lời giải (tối ưu hoặc gần tối ưu)
- Khả năng áp dụng với không gian trạng thái lớn

Áp dụng thực tế:
- Triển khai các thuật toán để giải bài toán 8-puzzle
- So sánh kết quả về số bước, thời gian giải và độ tối ưu giữa các thuật toán

Củng cố kỹ năng lập trình và tư duy giải quyết vấn đề. Hiểu và hiện thực các thuật toán.

Thực hành cài đặt cấu trúc dữ liệu, hàng đợi, cây tìm kiếm...
Đánh giá khả năng mở rộng và cải tiến thuật toán.

---

## 2. Nội dung
### 2.1. Nhóm tìm kiếm không thông tin (Uninformed Search)
- Các thuật toán chính bao gồm: BFS, DFS, UCS, IDS

Đầu tiên là BFS (Breath-First Search) - Tìm kiếm theo chiều rộng.

- Trong 8-puzzle, BFS tìm tất cả các trạng thái theo từng lớp, từ trạng thái ban đầu đến các trạng thái sau 1 bước, 2 bước, v.v.
- Luôn đảm bảo tìm ra đường đi ngắn nhất (ít bước nhất) đến trạng thái đích nếu tồn tại.
- Tuy nhiên, nhược điểm lớn là tốn rất nhiều bộ nhớ, vì phải lưu trữ nhiều trạng thái ở mỗi lớp.
- Không hiệu quả với các trạng thái cách xa đích (nhiều bước).
![bfs1](https://github.com/user-attachments/assets/b7699676-b4cc-4edb-845a-25c4bee2e614)

Thứ hai là DFS (Depth-First Search) – Tìm kiếm theo chiều sâu

- DFS ưu tiên đi sâu xuống một nhánh bất kỳ, đến khi chạm đích hoặc không thể đi tiếp.
- Có thể nhanh nếu may mắn chọn đúng nhánh gần lời giải, nhưng không đảm bảo tìm được lời giải ngắn nhất.
- Rất dễ rơi vào vòng lặp nếu không kiểm tra trạng thái đã thăm.
- Tốn ít bộ nhớ, nhưng không đáng tin cậy cho bài toán 8-puzzle nếu không giới hạn độ sâu.
![dfs1](https://github.com/user-attachments/assets/0dcb5b80-4cb7-477d-95a6-b9eb68a5a7df)

Thứ ba là UCS (Uniform-Cost Search) – Tìm kiếm theo chi phí đều

- Trong 8-puzzle, UCS hoạt động giống BFS nếu chi phí di chuyển giữa các ô bằng nhau.
- Tuy nhiên, UCS ưu tiên mở rộng các trạng thái có tổng chi phí nhỏ nhất từ gốc đến hiện tại.
- Tìm được lời giải tối ưu cả về số bước và chi phí nếu chi phí từng bước không đồng đều.
- Thường tốn thời gian và bộ nhớ hơn BFS, đặc biệt với nhiều nhánh có cùng chi phí.
![ucs1](https://github.com/user-attachments/assets/35f16454-3954-425d-8326-5327e783c49f)

Thứ tư là IDS (Iterative Deepening Search) – Tìm kiếm sâu dần

- IDS thực hiện DFS nhiều lần, với giới hạn độ sâu tăng dần.
- Mỗi lần tăng giới hạn, thuật toán tìm đến độ sâu đó rồi quay lại tìm tiếp.
- Trong 8-puzzle, IDS giải quyết được nhược điểm của DFS (vượt quá sâu, không tối ưu) và khắc phục được hạn chế bộ nhớ của BFS.
- Tuy nhiên, tốn thời gian hơn một chút, vì các trạng thái đầu tiên bị duyệt lặp lại nhiều lần.
![ids (1)](https://github.com/user-attachments/assets/2ab0d5d6-6df4-475e-a5ee-a6357f585a9b)

Kết luận:
BFS và UCS cho kết quả nhanh và tối ưu nhất trong ví dụ này (chỉ 19 bước, dưới 0.1s).
DFS tuy đơn giản nhưng hiệu suất kém, dẫn đến số bước lớn và thời gian cao hơn.
IDS đạt lời giải đúng (19 bước) nhưng phải hy sinh thời gian do lặp lại theo tầng, phù hợp khi cần giới hạn bộ nhớ.

Biểu đồ so sánh trực quan 4 thuật toán
![Screenshot 2025-05-19 030747](https://github.com/user-attachments/assets/feb0883f-b43b-4e08-b123-6fef7e7036fe)

### 2.2. Nhóm tìm kiếm có thông tin (Informed Search)

- Các thuật toán chính bao gồm: Greedy, IDA*, A*
- Đặc điểm: Sử dụng hàm lượng giá (heuristic) để định hướng quá trình tím kiếm về trạng thái đích.
- Ưu điểm: Tìm kiếm hiệu quả hơn, giảm không gian trạng thái duyệt so với các thuật toán mù như BFS/DFS.
- Hàm đánh giá tổng quát: f(n) = g(n) + h(n)
  Trong đó: g(n) là chi phí từ trạng thái ban đầu đến n. h(n) là chi phí ước lượng từ n đến trạng thái đích (heuristic)

Greedy: Chỉ quan tâm ước lượng đến đích, không tối ưu nhưng rất nhanh
![greedy](https://github.com/user-attachments/assets/2671ad88-83c4-4e06-85b1-461a1b6e31d1)

A*: 

- Hàm đánh giá: f(n) = g(n) + h(n)
- Tính toán chi phí bằng Manhattan Distance
- Tính chất: Tìm lời giải tối ưu nếu h(n) là admissible ( không đánh giá vượt chi phí thật)
- Hiệu quả trong bài: Tìm ra lời giải ngắn nhất nhưng tốn bộ nhớ nhiều nếu không gian trạng thái lớn.
![a](https://github.com/user-attachments/assets/6fe7140e-2ac3-43ac-8da3-fc63034535a3)

IDA*: kết hợp ưu điểm của A8 và BFS
- Cách hoạt động:
  Duyệt lặp sâu theo giới hạn của hàm f(n) = g(n) + h(n)
  Tăng giới hạn dần cho đến khi tìm ra lời giải
- Ưu điểm: tiết kiệm bộ nhớ và tìm ra lời giải tối ưu
- Nhược điểm: Có thể lặp lại nhiều trạng thái, chậm hơn A8 trong không gian nhỏ
![ida](https://github.com/user-attachments/assets/4cbb21ee-16f9-46d9-ae57-00699017aeb9)

Kết luận:
| Tiêu chí                  | **Greedy**                           | **A\***                                | **IDA\***                             |
| ------------------------- | ------------------------------------ | -------------------------------------- | ------------------------------------- |
| **Không gian trạng thái** | Duyệt ít, chỉ theo hướng heuristic   | Duyệt rộng và có tổ chức               | Duyệt theo tầng sâu (vòng lặp)        |
| **Bộ nhớ sử dụng**        | Thấp (không lưu toàn bộ trạng thái)  | Rất cao (duy trì toàn bộ open/closed)  | Thấp (dùng ít bộ nhớ nhờ DFS lặp lại) |
| **Thời gian thực thi**    | Nhanh nhưng dễ lệch hướng            | Tốt (nhanh và chính xác)               | Chậm hơn do phải lặp lại nhiều lần    |
| **Lời giải**              | Không tối ưu                         | Tối ưu (nếu h(n) phù hợp)              | Tối ưu                                |
| **Độ phù hợp**            | Khi cần kết quả nhanh, chấp nhận sai | Khi cần lời giải chính xác & bộ nhớ đủ | Khi không đủ bộ nhớ, cần tối ưu       |

Biểu đồ so sánh:

![Screenshot 2025-05-19 031420](https://github.com/user-attachments/assets/fcfbae4b-7ca8-4d80-a216-233358084899)

### 2.3. Nhóm thuật toán tìm kiếm cục bộ (Local Search)

Simple Hill Climbing

![SHC](https://github.com/user-attachments/assets/dc872d72-ab62-4100-b40c-d1a6470794c3)

Steepest Ascent Hill Climbing

![SAHC](https://github.com/user-attachments/assets/7823cbb3-2ad3-447c-960d-e2aa52288bdd)

Stochastic Hill Climbing

![STOHC](https://github.com/user-attachments/assets/47aed033-63b3-4f14-9fbc-41e4d5249f5b)

Simulated Annealing

![SA](https://github.com/user-attachments/assets/81ee14f3-4590-48fc-8a2c-9d2bb81e3603)

Beam Search

![beam](https://github.com/user-attachments/assets/de8585b2-a30a-4a02-a06b-458153ff0e71)

Genetic Algorithm

![GA](https://github.com/user-attachments/assets/fdd3f4e6-cc9d-469b-897e-5dc817277052)

### 2.4. Tìm kiếm trong môi trường phức tạp (Search in Complex Environment)

And-Or Search

![andor](https://github.com/user-attachments/assets/be281d41-4f5a-4102-ba90-4e808d20ef0d)

Partially Observable Search

![par](https://github.com/user-attachments/assets/a2d00540-efd4-4209-9896-a110562f330a)

Belief State

![Belief_BFS](https://github.com/user-attachments/assets/0ab8915d-c2f3-4beb-90d4-a6d66776967f)

![belief_a](https://github.com/user-attachments/assets/b5c3f510-ae0f-4682-b8ee-47eee378759e)

### 2.5. Tìm kiếm trong môi trường không có ràng buộc (Constraint Satisfaction Problem)

Backtracking

![back](https://github.com/user-attachments/assets/100e083f-e42c-4f11-b2a2-2e8eab401839)

AC-3 Search Algorithm

![ac3](https://github.com/user-attachments/assets/d746759d-0207-4ca4-8a45-4bc289b9de04)

Forward Checking

![forward](https://github.com/user-attachments/assets/dffd010c-d445-4d22-8fca-6ecb1a6636d8)

### 2.6. Học tăng cường (Reinforcement Learning)
Q-Learning là thuật toán học chính sách hành động dựa trên kinh nghiệm (thử - sai), không cần mô hình môi trường.
Nó học thông qua việc cập nhật bảng Q-Table với công thức:
 Q(a,a) <-- Q(s,a) + alpha[ r + gama.maxQ(a', a') - Q(s,a)]
 s: trạng thái hiện tại
 a: hành động thực hiện
 r: phần thưởng nhận được
 s': trạng thái mới
 alpha: learning rate
 gama: discount factor

 Ưu điểm của Q-Learning
 | Tiêu chí                               | Mô tả                                                                   |
| -------------------------------------- | ----------------------------------------------------------------------- |
| **Không cần mô hình**                  | Không cần biết trước hàm chuyển trạng thái, chỉ cần trải nghiệm để học. |
| **Có thể học dần dần**                 | Phù hợp với các môi trường động hoặc bài toán mở rộng dần.              |
| **Kết hợp được phần thưởng linh hoạt** | Cho phép thiết kế reward để điều chỉnh hành vi mong muốn.               |

Nhược điểm của Q-Learning trong bài 8-puzzle
| Vấn đề                        | Giải thích                                                                                |
| ----------------------------- | ----------------------------------------------------------------------------------------- |
| **Không gian trạng thái lớn** | Với 8-puzzle có 9! = 362,880 trạng thái → Q-table rất lớn (và còn lớn hơn với 15-puzzle). |
| **Học chậm**                  | Cần nhiều tập để converged → tốn thời gian nếu không có chiến lược tốt.                   |
| **Không đảm bảo tối ưu**      | Nếu chưa đủ training hoặc reward thiết kế sai → giải pháp không tối ưu hoặc sai.          |

![Q](https://github.com/user-attachments/assets/c1df615e-9599-4ab5-84a6-f4e0945817f6)

Kết luận:
- Dùng Q-Learning để huấn luyện agent giải 8-puzzle là khó khả thi với state-space lớn nếu chỉ dùng bảng Q (Q-table).
- Hiệu quả hơn nếu:
-- Áp dụng với 4x4 hoặc ít trạng thái (ví dụ huấn luyện khởi động).
-- Sử dụng Deep Q-Learning (DQN) với mạng neural thay vì bảng Q truyền thống.
- So với A*, Q-learning không ổn định, học lâu, nhưng có khả năng mở rộng cho môi trường phức tạp không xác định trước.
---

## 3. Kết luận
Ứng dụng hỗ trợ học và so sánh trực quan hiệu quả các nhóm thuật toán AI.

A*, IDA*, Beam Search cho kết quả tốt và ổn định.

Q-learning mở rộng khả năng giải khi không cần mô hình rõ ràng.

CSP thích hợp để tạo và xác nhận trạng thái ban đầu hợp lệ.

Môi trường niềm tin giúp thử nghiệm thuật toán trong điều kiện bất định và không đầy đủ thông tin.
