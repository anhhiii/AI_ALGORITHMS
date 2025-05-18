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

-IDS thực hiện DFS nhiều lần, với giới hạn độ sâu tăng dần.
-Mỗi lần tăng giới hạn, thuật toán tìm đến độ sâu đó rồi quay lại tìm tiếp.
-Trong 8-puzzle, IDS giải quyết được nhược điểm của DFS (vượt quá sâu, không tối ưu) và khắc phục được hạn chế bộ nhớ của BFS.
-Tuy nhiên, tốn thời gian hơn một chút, vì các trạng thái đầu tiên bị duyệt lặp lại nhiều lần.
![ids (1)](https://github.com/user-attachments/assets/2ab0d5d6-6df4-475e-a5ee-a6357f585a9b)

Kết luận:
Có thể thấy BFS đưa ra lời giải chính xác, tuy nhiên lại tốn nhiều thời gian hơn vì phải duyệt nhiều trạng thái.
DFS thì thời gian nhanh hơn nhưng lời giải không tối ưu, dễ rơi vào vòng lặp đệ quy, không đảm bảo sẽ tìm được đường đi tốt nhất.
UCS nhanh hơn BFS nhưng chậm hơn DFS và đáng tin cậy hơn DFS.
IDS ít tốn bộ nhớ, thời gian nhanh, lời giải chính xác
---

## 3. Kết luận
Ứng dụng hỗ trợ học và so sánh trực quan hiệu quả các nhóm thuật toán AI.

A*, IDA*, Beam Search cho kết quả tốt và ổn định.

Q-learning mở rộng khả năng giải khi không cần mô hình rõ ràng.

CSP thích hợp để tạo và xác nhận trạng thái ban đầu hợp lệ.

Môi trường niềm tin giúp thử nghiệm thuật toán trong điều kiện bất định và không đầy đủ thông tin.
