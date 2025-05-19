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
Các thuật toán chính bao gồm: BFS, DFS, UCS, IDS

**Đầu tiên là BFS (Breath-First Search) - Tìm kiếm theo chiều rộng.**

_Cách hoạt động:_ BFS khám phá tất cả các trạng thái theo từng lớp (level) bắt đầu từ trạng thái ban đầu. Nó mở rộng tất cả các trạng thái cách gốc 1 bước, sau đó là 2 bước, và tiếp tục cho đến khi tìm thấy trạng thái đích hoặc hết không gian tìm kiếm. Trong 8-puzzle, mỗi bước là một nước đi hợp lệ của ô trống (lên, xuống, trái, phải).

_Đặc điểm:_

Luôn đảm bảo tìm ra đường đi ngắn nhất (ít bước nhất) đến trạng thái đích ((1, 2, 3), (4, 5, 6), (7, 8, 0)) nếu lời giải tồn tại, nhờ duyệt theo thứ tự lớp.

Sử dụng hàng đợi (queue) để lưu trữ các trạng thái cần khám phá.

_Ưu điểm:_

Tối ưu về số bước, rất phù hợp khi yêu cầu đường đi ngắn nhất.

Hoàn chỉnh (complete) trong không gian hữu hạn như 8-puzzle (~181,440 trạng thái).

_Nhược điểm:_

Tốn rất nhiều bộ nhớ vì phải lưu trữ tất cả các trạng thái của từng lớp. Với 8-puzzle, số trạng thái tăng theo cấp số nhân (4 trạng thái con cho mỗi trạng thái, trừ biên), dẫn đến bộ nhớ vượt quá khả năng thực tế khi độ sâu lớn.

Không hiệu quả với các trạng thái cách xa đích (nhiều bước), vì phải duyệt toàn bộ không gian trước khi đạt giải.

![bfs1](https://github.com/user-attachments/assets/b7699676-b4cc-4edb-845a-25c4bee2e614)

**Thứ hai là DFS (Depth-First Search) – Tìm kiếm theo chiều sâu**

_Cách hoạt động:_ DFS đi sâu vào một nhánh bất kỳ, khám phá hết các trạng thái con của nhánh đó trước khi quay lại nhánh khác. Sử dụng ngăn xếp (stack) để theo dõi các trạng thái cần khám phá. Trong 8-puzzle, nó có thể chọn ngẫu nhiên một nước đi (ví dụ: lên) và tiếp tục sâu xuống đến khi không còn nước đi hợp lệ.

_Đặc điểm:_

Có thể nhanh nếu may mắn chọn nhánh chứa lời giải, nhưng không đảm bảo tìm đường đi ngắn nhất.
Rất dễ rơi vào vòng lặp nếu không kiểm tra trạng thái đã thăm (trạng thái lặp lại trong không gian chu trình).

_Ưu điểm:_

Tốn ít bộ nhớ hơn BFS vì chỉ lưu một nhánh duy nhất tại một thời điểm.

Đơn giản để triển khai, phù hợp với các bài toán nhỏ hoặc khi không cần tối ưu.

_Nhược điểm:_

Không tối ưu về số bước, thường dẫn đến đường đi dài hơn (ví dụ: 50+ bước so với 19 bước của BFS).

Không đáng tin cậy cho 8-puzzle nếu không giới hạn độ sâu, vì có thể đi sâu mãi mà không tìm thấy giải hoặc bị kẹt trong nhánh sai.

Thời gian cao hơn nếu nhánh chọn không dẫn đến đích.
  
![dfs1](https://github.com/user-attachments/assets/0dcb5b80-4cb7-477d-95a6-b9eb68a5a7df)

**Thứ ba là UCS (Uniform-Cost Search) – Tìm kiếm theo chi phí đều**

_Cách hoạt động:_ UCS mở rộng các trạng thái theo thứ tự chi phí tổng cộng từ trạng thái ban đầu, sử dụng hàng đợi ưu tiên (priority queue). Trong 8-puzzle, nếu chi phí di chuyển giữa các ô bằng nhau (thường là 1), UCS hoạt động giống BFS. Nếu chi phí không đồng đều (ví dụ: di chuyển lên tốn 1, xuống tốn 2), UCS sẽ ưu tiên trạng thái có chi phí thấp nhất.

_Đặc điểm:_

Tìm được lời giải tối ưu cả về số bước và chi phí nếu chi phí từng bước khác nhau.

Sử dụng hàm đánh giá g(n) (chi phí từ gốc đến nút hiện tại) để sắp xếp thứ tự mở rộng.

_Ưu điểm:_

Linh hoạt với các bài toán có chi phí không đồng đều, đảm bảo giải pháp tối ưu.

Hoàn chỉnh trong không gian hữu hạn.

_Nhược điểm:_

Tốn thời gian và bộ nhớ hơn BFS khi có nhiều nhánh với chi phí giống nhau, vì phải duy trì hàng đợi ưu tiên.

Với 8-puzzle tiêu chuẩn (chi phí bằng 1), UCS không vượt trội hơn BFS mà còn chậm hơn do chi phí tính toán sắp xếp.
  
![ucs1](https://github.com/user-attachments/assets/35f16454-3954-425d-8326-5327e783c49f)

**Thứ tư là IDS (Iterative Deepening Search) – Tìm kiếm sâu dần**

__Cách hoạt động: IDS thực hiện DFS nhiều lần, mỗi lần với giới hạn độ sâu tăng dần (0, 1, 2, ...). Nếu không tìm thấy giải ở độ sâu hiện tại, tăng giới hạn và lặp lại. Trong 8-puzzle, nó kiểm tra từng tầng trạng thái theo độ sâu cho đến khi đạt đích.

_Đặc điểm:_

Kết hợp ưu điểm của DFS (tiết kiệm bộ nhớ) và BFS (tối ưu số bước).

Mỗi lần lặp lại, các trạng thái đầu tiên được duyệt lại, nhưng chỉ một lần duy nhất ở độ sâu tối ưu.

_Ưu điểm:_

Giải quyết nhược điểm của DFS (vượt quá sâu) và BFS (tốn bộ nhớ).

Đảm bảo tìm đường đi ngắn nhất như BFS, với bộ nhớ giới hạn như DFS.

_Nhược điểm:_

Tốn thời gian hơn một chút do lặp lại duyệt các trạng thái ở tầng thấp, đặc biệt khi độ sâu lớn.

Hiệu suất giảm nếu bài toán có nhiều trạng thái ở các tầng đầu.
  
![ids (1)](https://github.com/user-attachments/assets/2ab0d5d6-6df4-475e-a5ee-a6357f585a9b)

**Kết luận:**
BFS và UCS cho kết quả nhanh và tối ưu nhất trong ví dụ này (chỉ 19 bước, dưới 0.1s).
DFS tuy đơn giản nhưng hiệu suất kém, dẫn đến số bước lớn và thời gian cao hơn.
IDS đạt lời giải đúng (19 bước) nhưng phải hy sinh thời gian do lặp lại theo tầng, phù hợp khi cần giới hạn bộ nhớ.

**Biểu đồ so sánh trực quan 4 thuật toán**
![Screenshot 2025-05-19 030747](https://github.com/user-attachments/assets/feb0883f-b43b-4e08-b123-6fef7e7036fe)

### 2.2. Nhóm tìm kiếm có thông tin (Informed Search)

Các thuật toán chính bao gồm: Greedy Search, A*, và IDA*. Nhóm này nổi bật với việc sử dụng hàm lượng giá (heuristic) để định hướng quá trình tìm kiếm về trạng thái đích, cải thiện hiệu quả so với các thuật toán không thông tin như BFS hay DFS.

- Đặc điểm: Sử dụng hàm lượng giá (heuristic) để định hướng quá trình tím kiếm về trạng thái đích.
- Ưu điểm: Tìm kiếm hiệu quả hơn, giảm không gian trạng thái duyệt so với các thuật toán mù như BFS/DFS.
- Hàm đánh giá tổng quát: f(n) = g(n) + h(n)
  Trong đó: g(n) là chi phí từ trạng thái ban đầu đến n. h(n) là chi phí ước lượng từ n đến trạng thái đích (heuristic)

**Greedy:**

_Cách hoạt động:_ Chỉ quan tâm đến h(n) (ước lượng chi phí đến đích), bỏ qua g(n) (chi phí đã đi). Luôn chọn trạng thái có h(n) nhỏ nhất để mở rộng.

_Đặc điểm:_

Sử dụng heuristic như Manhattan Distance (tổng khoảng cách Manhattan của các ô đến vị trí mục tiêu).

Không đảm bảo tìm đường đi ngắn nhất, vì chỉ ưu tiên hướng đến đích mà không cân nhắc chi phí đã đi.

_Ưu điểm:_

Rất nhanh do duyệt ít trạng thái, phù hợp khi cần kết quả gần đúng nhanh chóng.

Bộ nhớ thấp vì không cần lưu toàn bộ không gian đã duyệt.

_Nhược điểm:_

Dễ bị kẹt ở cực trị cục bộ (local optima) hoặc chọn nhánh sai, dẫn đến lời giải không tối ưu.

Không hoàn chỉnh nếu heuristic dẫn đến vòng lặp không kiểm soát.

![greedy](https://github.com/user-attachments/assets/2671ad88-83c4-4e06-85b1-461a1b6e31d1)

**A Star:**

_Cách hoạt động:_
  Duyệt lặp sâu theo giới hạn của hàm f(n) = g(n) + h(n)
  
  Tăng giới hạn dần cho đến khi tìm ra lời giải

_Đặc điểm:_

Tính chất: Tìm lời giải tối ưu nếu h(n) là admissible (luôn nhỏ hơn hoặc bằng chi phí thực tế đến đích) và consistent (khác biệt h(n) - h(n') <= c(n, n'), với c là chi phí di chuyển).

Duy trì hai tập: open list (chờ xử lý) và closed list (đã xử lý), đảm bảo không bỏ sót trạng thái tốt.

_Ưu điểm:_

Đảm bảo tìm đường đi ngắn nhất nếu heuristic phù hợp.

Hiệu quả trong không gian vừa phải, đặc biệt khi heuristic chính xác.

_Nhược điểm:_

Tốn nhiều bộ nhớ do phải lưu toàn bộ open và closed list, đặc biệt trong 8-puzzle với ~181,440 trạng thái.

Thời gian thực thi tăng khi không gian trạng thái lớn hoặc heuristic không tối ưu.
![a](https://github.com/user-attachments/assets/6fe7140e-2ac3-43ac-8da3-fc63034535a3)

**IDA Star:**

_Cách hoạt động:_ Kết hợp ưu điểm của A* và IDS, sử dụng f(n) = g(n) + h(n) làm giới hạn. Duyệt sâu dần theo giá trị f(n) tăng dần (từ nhỏ đến lớn) cho đến khi tìm ra lời giải.

_Đặc điểm:_

Giống IDS, lặp lại DFS với giới hạn f(n) thay vì độ sâu.

Tiết kiệm bộ nhớ bằng cách không lưu toàn bộ open list, chỉ giữ trạng thái hiện tại.

_Ưu điểm:_

Tìm lời giải tối ưu nếu h(n) admissible, giống A*.

Tiết kiệm bộ nhớ đáng kể so với A*, phù hợp khi tài nguyên hạn chế.

_Nhược điểm:_

Chậm hơn A* trong không gian nhỏ do lặp lại duyệt nhiều trạng thái.

Có thể lặp lại trạng thái nhiều lần nếu heuristic không consistent, làm tăng thời gian.

![ida](https://github.com/user-attachments/assets/4cbb21ee-16f9-46d9-ae57-00699017aeb9)

**Kết luận:**
| Tiêu chí                  | **Greedy**                           | **A\***                                | **IDA\***                             |
| ------------------------- | ------------------------------------ | -------------------------------------- | ------------------------------------- |
| **Không gian trạng thái** | Duyệt ít, chỉ theo hướng heuristic   | Duyệt rộng và có tổ chức               | Duyệt theo tầng sâu (vòng lặp)        |
| **Bộ nhớ sử dụng**        | Thấp (không lưu toàn bộ trạng thái)  | Rất cao (duy trì toàn bộ open/closed)  | Thấp (dùng ít bộ nhớ nhờ DFS lặp lại) |
| **Thời gian thực thi**    | Nhanh nhưng dễ lệch hướng            | Tốt (nhanh và chính xác)               | Chậm hơn do phải lặp lại nhiều lần    |
| **Lời giải**              | Không tối ưu                         | Tối ưu (nếu h(n) phù hợp)              | Tối ưu                                |
| **Độ phù hợp**            | Khi cần kết quả nhanh, chấp nhận sai | Khi cần lời giải chính xác & bộ nhớ đủ | Khi không đủ bộ nhớ, cần tối ưu       |

**Biểu đồ so sánh:**

![Screenshot 2025-05-19 031420](https://github.com/user-attachments/assets/fcfbae4b-7ca8-4d80-a216-233358084899)

### 2.3. Nhóm thuật toán tìm kiếm cục bộ (Local Search)

Các thuật toán chính bao gồm: Simple Hill Climbing, Steepest Ascent Hill Climbing, Stochastic Hill Climbing, Simulated Annealing, Beam Search, và Genetic Algorithm. Nhóm này tập trung vào việc cải thiện trạng thái hiện tại dựa trên heuristic (thường là Manhattan Distance trong 8-puzzle) mà không cần duyệt toàn bộ không gian trạng thái.

**Simple Hill Climbing**

_Nguyên lý:_ Tại mỗi bước, chọn trạng thái kề có giá trị heuristic (thường là -Manhattan Distance) tốt hơn trạng thái hiện tại. Quá trình dừng khi không còn trạng thái kề nào cải thiện.

_Áp dụng trong 8-puzzle:_

    Di chuyển ô trống theo hướng làm giảm tổng khoảng cách đến goal.
    
    Dừng nếu không còn bước nào cải thiện.
    
_Ưu điểm:_ dễ cài đặt, nhanh, ít bộ nhớ

_Nhược điểm:_ 

Dễ kẹt ở local maximum, plateau (cao nguyên), hoặc ridge (đỉnh giả), bỏ qua lời giải toàn cục dù gần đích.

Không đảm bảo tìm được lời giải nếu không gian trạng thái phức tạp.

![SHC](https://github.com/user-attachments/assets/dc872d72-ab62-4100-b40c-d1a6470794c3)

**Steepest Ascent Hill Climbing**

- Nguyên lý: Ở mỗi bước, duyệt tất cả trạng thái kề, chọn trạng thái có heuristic cải thiện nhiều nhất.
- Áp dụng trong 8-puzzle: So sánh mọi bước đi từ trạng thái hiện tại, chọn tốt nhất.
- Ưu điểm: Tốt hơn SImple Hill, Ít rơi vào local minima hơn
- Nhược điểm:Không đmả bảo lời giải tối ưu. Có theer đứng yên nếu tất cả con đều có giá trị bằng nhau.
- Hiệu quả: Tốt hơn Simple Hill những vẫn có rủi ro không đến goal
  
![SAHC](https://github.com/user-attachments/assets/7823cbb3-2ad3-447c-960d-e2aa52288bdd)

**Stochastic Hill Climbing**

- Nguyên lý: Từ các bước đi tốt hơn hiện tại, chọn ngẫu nhiên một bước.
- Áp dụng trong 8-puzzle: Trong các bước làm giảm heuristic, lấy random một bước.
- Ưu điểm: Tránh được local maximum do tính ngẫu nhiên.
- Nhược điểm:
    Không ổn định (kết quả khác nhau giữa các lần chạy).
    Có thể đi vòng vèo dù gần đích.
- Hiệu quả: Thích hợp nếu chạy nhiều lần để lấy giải tốt nhất.

![STOHC](https://github.com/user-attachments/assets/47aed033-63b3-4f14-9fbc-41e4d5249f5b)

**Simulated Annealing**

- Nguyên lý: Cho phép di chuyển tới trạng thái kém hơn hiện tại với xác suất phụ thuộc vào “nhiệt độ” T. Xác suất này giảm dần theo thời gian.
 Áp dụng trong 8-puzzle: Có thể tạm thời đi lùi để tránh mắc kẹt tại local minimum.
- Ưu điểm:
    Có khả năng tìm được lời giải toàn cục.
    Tránh được local trap.
- Nhược điểm:
    Phụ thuộc nhiều vào hàm làm nguội (cooling schedule).
    Có thể chậm hoặc không hội tụ nếu T giảm quá nhanh.
- Hiệu quả: Hiệu quả cao nếu cấu hình đúng.

![SA](https://github.com/user-attachments/assets/81ee14f3-4590-48fc-8a2c-9d2bb81e3603)

**Beam Search**

- Nguyên lý: Tại mỗi bước chỉ giữ lại k trạng thái tốt nhất theo heuristic (beam width).
- Áp dụng trong 8-puzzle: Từ trạng thái hiện tại, sinh ra tất cả con, chỉ giữ lại top-k có h(n) tốt nhất.
- Ưu điểm: Tiết kiệm bộ nhớ và thời gian so với Best-First Search.
- Nhược điểm:
    Có thể loại bỏ trạng thái tốt do giới hạn beam width.
    Không đảm bảo tìm được goal.
- Hiệu quả: Cần chọn beam width phù hợp; width nhỏ có thể thất bại, width lớn giống greedy.

![beam](https://github.com/user-attachments/assets/de8585b2-a30a-4a02-a06b-458153ff0e71)

**Genetic Algorithm**
- Nguyên lý: Duy trì quần thể các lời giải, lặp lại:
    Chọn lọc cá thể tốt.
    Lai ghép (crossover).
    Đột biến (mutation).
- Áp dụng trong 8-puzzle:
    Mỗi cá thể là một trạng thái.
    Fitness = -heuristic (càng gần goal càng tốt).
    Crossover = trao đổi phần trạng thái giữa 2 cá thể.
- Ưu điểm:
    Thám hiểm không gian rộng lớn, dễ mở rộng.
    Có thể tìm lời giải tốt sau nhiều thế hệ.
- Nhược điểm:
    Chậm, tốn tài nguyên.
    Cần tinh chỉnh tỉ lệ mutation/crossover.
- Hiệu quả: Tốt khi không cần kết quả ngay, nhưng cần nhiều vòng lặp.

![GA](https://github.com/user-attachments/assets/fdd3f4e6-cc9d-469b-897e-5dc817277052)

Dưới đây là bảng tổng kết lại các thuật toán trong nhóm local, bao gồm ưu, nhược điểm của mỗi thuật toán trong bài toán 8 puzzle
| Thuật toán                   | Mô tả                                                          | Ưu điểm                         | Nhược điểm                                              |
| ---------------------------- | -------------------------------------------------------------- | ------------------------------- | ------------------------------------------------------- |
| **Simple Hill Climbing**     | Luôn chọn trạng thái cải thiện heuristic.                      | Nhanh; đơn giản.                | Dễ rơi vào cực đại cục bộ.                              |
| **Steepest Ascent**          | Chọn trạng thái có cải thiện nhiều nhất.                       | Chính xác hơn Simple Hill.      | Vẫn có thể kẹt tại local maxima.                        |
| **Stochastic Hill Climbing** | Chọn ngẫu nhiên trong số các bước cải thiện.                   | Tránh local maxima tốt hơn.     | Kết quả không ổn định.                                  |
| **Simulated Annealing**      | Cho phép đi lùi với xác suất, giảm dần nhiệt độ.               | Thoát local maxima tốt.         | Chậm; phụ thuộc vào tham số T.                          |
| **Beam Search**              | Giới hạn số node mở rộng dựa vào heuristic.                    | Tối ưu tài nguyên.              | Có thể bỏ sót lời giải nếu không nằm trong beam.        |
| **Genetic Algorithm**        | Dựa vào quần thể giải pháp; tiến hóa qua lai ghép và đột biến. | Thích nghi và đa dạng lời giải. | Phụ thuộc mạnh vào thiết kế fitness và cơ chế chọn lọc. |

**Tính chất không ổn định của tìm kiếm cục bộ**
Khác với các thuật toán tìm kiếm có hệ thống (như BFS, A*...), các thuật toán cục bộ thường không duyệt toàn bộ không gian trạng thái, mà chỉ tìm lời giải bằng cách cải thiện trạng thái hiện tại, nên:
- Kết quả phụ thuộc rất lớn vào trạng thái khởi đầu.
Không đảm bảo tìm ra lời giải, ngay cả khi có lời giải tồn tại.
- Cùng một thuật toán, cùng một bài toán, chạy nhiều lần có thể ra kết quả khác nhau (ví dụ: Stochastic Hill Climbing, Simulated Annealing, Genetic Algorithm do có yếu tố ngẫu nhiên).
- Do đó, không nên đánh giá các thuật toán này qua biểu đồ cột tĩnh như thời gian chạy hoặc số bước đi ở một lần duy nhất — vì kết quả mỗi lần có thể dao động đáng kể.

**So sánh hiệu quả các thuật toán tìm kiếm cục bộ:** 

_Hiệu quả thực tế:_

Simple Hill và Steepest Ascent nhanh nhưng dễ kẹt, phù hợp cho thử nghiệm nhanh.

Stochastic Hill và Simulated Annealing tốt hơn trong việc thoát local maxima, với Simulated Annealing vượt trội nếu tinh chỉnh tốt.

Beam Search cân bằng giữa hiệu quả và tài nguyên, nhưng phụ thuộc vào k.

Genetic Algorithm mạnh trong thám hiểm không gian lớn, nhưng chậm và cần nhiều tài nguyên.

_Ứng dụng trong 8-puzzle:_ Nhóm này phù hợp khi không cần đường đi chính xác mà chỉ cần trạng thái đích, hoặc khi không gian trạng thái quá lớn để áp dụng tìm kiếm có hệ thống.

**Nhận xét:** Tìm kiếm cục bộ có ưu điểm nổi bật là không gian trạng thái hữu hạn, tốc độ chạy nhanh, và ít tiêu tốn bộ nhớ. Tuy nhiên, nó dễ gặp các vấn đề như kẹt ở cực trị cục bộ, cao nguyên, đỉnh giả, hoặc lặp vô nghĩa, làm giảm độ tin cậy. Tính không ổn định (do ngẫu nhiên hoặc phụ thuộc trạng thái khởi đầu) khiến nó không đảm bảo luôn tìm ra lời giải, ngay cả khi lời giải tồn tại. Để cải thiện, cần kết hợp với các chiến lược như khởi tạo đa điểm, tinh chỉnh tham số (như T trong Simulated Annealing hoặc k trong Beam Search), hoặc chạy nhiều lần để lấy kết quả tốt nhất.

### 2.4. Tìm kiếm trong môi trường phức tạp (Search in Complex Environment)

Các thuật toán chính: And-Or Search, Partially Observable Search, Belief State

**Bài toán 8-puzzle trong môi trường phức tạp**

Trong bài toán 8-puzzle, ta có bảng 3x3 với các số từ 0 đến 8, 0 là ô trống. Mục tiêu là di chuyển ô trống để đạt trạng thái đích (ví dụ: ((1, 2, 3), (4, 5, 6), (7, 8, 0))). Trong môi trường phức tạp:

- Không xác định (Non-deterministic): Một hành động có thể dẫn đến nhiều kết quả khác nhau (ví dụ: di chuyển ô trống lên có thể thành công hoặc thất bại do yếu tố ngẫu nhiên).
- Quan sát không đầy đủ (Partially Observable): Người chơi không biết toàn bộ trạng thái của bảng (ví dụ: chỉ biết một phần bảng, phần còn lại là ẩn).
- Niềm tin (Belief States): Người chơi duy trì một tập hợp các trạng thái có thể xảy ra (belief states) dựa trên quan sát.
  
**And-Or Search**

_Mô tả thuật toán_

And-Or Search được sử dụng trong môi trường không xác định, nơi một hành động có thể dẫn đến nhiều kết quả khác nhau:
  
Cây And-Or:
- Or-nodes: Đại diện cho các lựa chọn của tác nhân (ví dụ: chọn hành động nào: lên, xuống, trái, phải).
- And-nodes: Đại diện cho các kết quả không xác định của một hành động (ví dụ: di chuyển lên có thể thành công hoặc thất bại).
  
Mục tiêu: Tìm một cây giải pháp (solution tree) mà từ trạng thái ban đầu, tác nhân có thể đạt được mục tiêu bất kể kết quả không xác định nào xảy ra.

Cách hoạt động:
- Bắt đầu từ trạng thái ban đầu, mở rộng cây And-Or.
- Tại mỗi Or-node, chọn một hành động và tạo And-node cho các kết quả có thể.
- Tại mỗi And-node, tìm đường dẫn đến mục tiêu cho mọi nhánh (kết quả).
- Nếu một nhánh không dẫn đến mục tiêu, quay lui và thử hành động khác.
  
_Áp dụng vào 8-puzzle_

- Môi trường không xác định: Giả sử hành động di chuyển ô trống có xác suất thất bại (ví dụ: di chuyển lên có 70% thành công, 30% thất bại và giữ nguyên trạng thái).
- Trạng thái ban đầu: ((1, 2, 3), (4, 5, 6), (0, 7, 8)).
- Mục tiêu: ((1, 2, 3), (4, 5, 6), (7, 8, 0)).
- Bước thực hiện:
  
  Or-node (Trạng thái ban đầu): Ô trống ở (2,0), các hành động: lên, phải.
  
  Chọn hành động "lên" → And-node với 2 nhánh:
  
  - Nhánh 1 (70%): Thành công, ô trống di chuyển lên (1,0) → Trạng thái: ((1, 2, 3), (0, 5, 6), (4, 7, 8)).
  - Nhánh 2 (30%): Thất bại, trạng thái không đổi: ((1, 2, 3), (4, 5, 6), (0, 7, 8)).
    
  Tiếp tục mở rộng:

  -  Từ nhánh 1: Ô trống ở (1,0), hành động: xuống, phải.
  -  Từ nhánh 2: Thử lại hành động khác (ví dụ: "phải").
    
  Xây dựng cây giải pháp:

  -  Mỗi And-node phải có đường dẫn đến mục tiêu cho cả 2 nhánh (thành công và thất bại).
  -  Nếu một hành động không dẫn đến mục tiêu ở cả 2 nhánh, quay lui và thử hành động khác.
    
- Kết quả: Cây giải pháp có thể là: "Thử di chuyển phải → Nếu thành công, tiếp tục di chuyển xuống → Nếu thất bại, thử lại di chuyển phải."

_Ưu điểm:_ Xử lý được môi trường không xác định, đảm bảo tìm được lời giải nếu có.

_Nhược điểm:_ Phức tạp, cần xây dựng toàn bộ cây giải pháp, tốn tài nguyên nếu số nhánh lớn.

![andor](https://github.com/user-attachments/assets/be281d41-4f5a-4102-ba90-4e808d20ef0d)

**Partially Observable Search**

_Mô tả thuật toán_

Partially Observable Search được sử dụng trong môi trường quan sát không đầy đủ, nơi tác nhân chỉ biết một phần của trạng thái:

- Tác nhân duy trì một belief state (tập hợp các trạng thái có thể xảy ra) dựa trên quan sát.
- Mỗi hành động cập nhật belief state dựa trên quan sát mới.
- Tìm kiếm đường đi từ belief state ban đầu đến belief state đích (chứa trạng thái mục tiêu).
  
_Áp dụng vào 8-puzzle_

Quan sát không đầy đủ:
- Giả sử chỉ hàng đầu tiên của bảng là nhìn thấy: ((1, 2, 3), (-1, -1, -1), (-1, -1, -1)).
- Tác nhân không biết trạng thái đầy đủ, chỉ biết ô trống nằm đâu đó ở 2 hàng dưới.
  
Belief State ban đầu:

- Tập hợp các trạng thái có thể:
  
    State 1: ((1, 2, 3), (4, 5, 6), (0, 7, 8)).
  
    State 2: ((1, 2, 3), (5, 6, 7), (4, 0, 8)).
  
    State 3: ((1, 2, 3), (5, 6, 8), (0, 4, 7)).
  
Mục tiêu:

- Belief State đích: Chứa trạng thái ((1, 2, 3), (4, 5, 6), (7, 8, 0)).
Bước thực hiện:
- Quan sát ban đầu: Chỉ biết hàng đầu 1, 2, 3, tạo belief state gồm 3 trạng thái trên.
- Thực hiện hành động:
  
    Hành động "di chuyển ô trống xuống" (giả sử tác nhân đoán ô trống ở (2,0)).
    Cập nhật belief state dựa trên quan sát mới:
  
      State 1: Ô trống từ (2,0) xuống → Không thể (đã ở hàng cuối) → Loại bỏ.
  
      State 2: Ô trống từ (2,1) xuống → Không thể → Loại bỏ.
  
      State 3: Ô trống từ (2,0) xuống → Không thể → Loại bỏ.
  
    Nếu không còn trạng thái nào trong belief state → Thất bại, quay lui.
  
- Thử hành động khác:

    Hành động "di chuyển ô trống phải":
  
      State 1: (2,0) → (2,1): ((1, 2, 3), (4, 5, 6), (7, 0, 8)).
  
      State 2: (2,1) → (2,2): ((1, 2, 3), (5, 6, 7), (4, 8, 0)).
  
      State 3: (2,0) → (2,1): ((1, 2, 3), (5, 6, 8), (4, 0, 7)).
  
    Quan sát mới (giả sử thấy ô trống ở (2,2)): Chỉ giữ State 2, loại bỏ State 1 và State 3.
  
- Tiếp tục: Từ State 2, tiếp tục di chuyển đến trạng thái đích.

_Ưu điểm:_ Xử lý được môi trường quan sát không đầy đủ, duy trì belief state linh hoạt.

_Nhược điểm:_ Tốn tài nguyên nếu belief state lớn, cần quan sát chính xác để thu hẹp belief state.

![par](https://github.com/user-attachments/assets/a2d00540-efd4-4209-9896-a110562f330a)

**Belief State**

_Mô tả thuật toán_

Belief State Search là một phương pháp mở rộng của Partially Observable Search, tập trung vào việc tìm kiếm trên không gian niềm tin:

- Belief State là tập hợp các trạng thái có thể xảy ra tại một thời điểm.
- Mỗi hành động chuyển belief state sang một belief state mới.
- Tìm kiếm (thường dùng BFS, A*) trên không gian niềm tin để đạt belief state đích (chứa trạng thái mục tiêu).

_Áp dụng vào 8-puzzle_

Belief State ban đầu: Như trên: 3 trạng thái có thể ((1, 2, 3), (4, 5, 6), (0, 7, 8)), ((1, 2, 3), (5, 6, 7), (4, 0, 8)), ((1, 2, 3), (5, 6, 8), (0, 4, 7)).

Belief State đích: Chứa trạng thái mục tiêu: ((1, 2, 3), (4, 5, 6), (7, 8, 0)).

Bước thực hiện:

  Xây dựng không gian niềm tin:
  
  - Mỗi node là một belief state.
  - Mỗi hành động (lên, xuống, trái, phải) chuyển belief state hiện tại sang belief state mới.
  - 
Tìm kiếm:

  Dùng BFS hoặc A* trên không gian niềm tin.
  
  Hàm heuristic (nếu dùng A*): Số ô sai vị trí trung bình trong belief state.
  
Cập nhật belief state:

  Hành động "phải":
  
    State 1: (2,0) → (2,1): ((1, 2, 3), (4, 5, 6), (7, 0, 8)).
    
    State 2: (2,1) → (2,2): ((1, 2, 3), (5, 6, 7), (4, 8, 0)).
    
    State 3: (2,0) → (2,1): ((1, 2, 3), (5, 6, 8), (4, 0, 7)).
    
  Belief State mới: Tập hợp 3 trạng thái này.
  
Tiếp tục: Lặp lại cho đến khi belief state chỉ chứa trạng thái đích.

_Ưu điểm:_ Tổng quát, có thể kết hợp với các thuật toán tìm kiếm khác (BFS, A*).

_Nhược điểm:_ Không gian niềm tin có thể rất lớn, dẫn đến chi phí tính toán cao.

![Belief_BFS](https://github.com/user-attachments/assets/0ab8915d-c2f3-4beb-90d4-a6d66776967f)

![belief_a](https://github.com/user-attachments/assets/b5c3f510-ae0f-4682-b8ee-47eee378759e)

**So sánh 3 thuật toán trong nhóm**
| Tiêu chí                    | And-Or Search                               | Partially Observable Search                | Belief State Search                         |
|----------------------------|---------------------------------------------|--------------------------------------------|---------------------------------------------|
| Môi trường áp dụng         | Không xác định                              | Quan sát không đầy đủ                      | Quan sát không đầy đủ                        |
| Phạm vi áp dụng            | Bài toán có hành động phụ thuộc             | Môi trường thiếu thông tin                 | Quản lý belief trong môi trường thiếu thông tin |
| Cách hoạt động             | Xây dựng cây giải pháp                      | Cập nhật belief state qua quan sát         | Tìm kiếm trên không gian niềm tin            |
| Hiệu quả                   | Thấp, không gian lớn                        | Trung bình, phụ thuộc vào quan sát         | Cao hơn nếu quan sát tốt                     |
| Độ phức tạp                | O(b^d) với b là nhánh, d là độ sâu          | O(b^s) với s là số trạng thái belief       | O(b^s * n) với n là số bước                  |
| Bộ nhớ                     | Cao, lưu cây And-Or                         | Trung bình, lưu belief states              | Cao, lưu và cập nhật belief                  |
| Ưu điểm                    | Linh hoạt với hành động phức tạp            | Xử lý tốt môi trường không quan sát        | Tối ưu hóa belief states                     |
| Nhược điểm                 | Không tối ưu cho 8-puzzle đơn thuần         | Phụ thuộc vào chất lượng quan sát          | Chi phí tính toán lớn với belief nhiều       |
| Phức tạp triển khai        | Cao (quản lý cây And-Or)                    | Trung bình (quản lý belief state)          | Cao (không gian niềm tin lớn)                |


**Kết luận**
And-Or Search không tối ưu cho 8-puzzle tiêu chuẩn, nhưng có thể hữu ích nếu bài toán mở rộng thành chuỗi hành động phức tạp.
Partially Observable Search phù hợp khi thông tin không đầy đủ, đặc biệt trong các kịch bản thực tế (ví dụ: robot giải puzzle với cảm biến hạn chế).
Belief State Search là lựa chọn mạnh mẽ nhất trong môi trường phức tạp, nhưng đòi hỏi cơ chế quan sát và xử lý belief hiệu quả.

### 2.5. Tìm kiếm trong môi trường không có ràng buộc (Constraint Satisfaction Problem)

Các thuật toán chính: Backtracking, AC-3 Search Algorithm, Forward Checking

**Bài toán 8-puzzle dưới dạng CSP**
  
Trong bài toán 8-puzzle, ta có một bảng 3x3 với 9 ô, chứa các số từ 0 đến 8, trong đó 0 là ô trống. Mục tiêu là sắp xếp bảng về trạng thái đích (ví dụ: ((1, 2, 3), (4, 5, 6), (7, 8, 0))).

Khi mô hình hóa dưới dạng CSP:

- Biến (Variables): Mỗi ô (r, c) trên bảng là một biến, tổng cộng 9 biến (ô (0,0), (0,1), ..., (2,2)).
- Miền giá trị (Domains): Mỗi biến có thể nhận giá trị từ 0 đến 8, nhưng vì đây là bài 8-puzzle, mỗi số chỉ được xuất hiện đúng một lần.
- Ràng buộc (Constraints):
  - Ràng buộc All-Different: Mỗi số từ 0 đến 8 phải xuất hiện đúng một lần trên bảng (không có số nào trùng lặp).
  - Ràng buộc trạng thái đích: Trạng thái cuối cùng phải khớp với trạng thái đích (ví dụ: ô (0,0) = 1, ô (0,1) = 2, ..., ô (2,2) = 0).
  
Mục tiêu của các thuật toán CSP là gán giá trị cho từng ô sao cho thỏa mãn tất cả các ràng buộc.
  
**Backtracking**

_Mô tả thuật toán_

Backtracking là một phương pháp tìm kiếm dựa trên thử-và-sai (trial-and-error), thường được sử dụng trong CSP. Ý tưởng chính là:

- Bắt đầu từ trạng thái ban đầu và thử từng nước đi hợp lệ.
- Nếu nước đi hiện tại không dẫn đến lời giải, quay lại (backtrack) trạng thái trước đó và thử nước đi khác.
- Tiếp tục cho đến khi tìm được trạng thái mục tiêu (goal state) hoặc xác định không có lời giải.

_Áp dụng cho 8-Puzzle_

Bước khởi tạo:

- Bảng 3x3 ban đầu: [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]] (-1 nghĩa là chưa gán).
- Cố định ô (2,2) = 0 (theo trạng thái đích).
- Mảng used để theo dõi số nào đã được sử dụng: used = [True, False, ..., False] (0 đã dùng).
  
Gán giá trị:

- Bắt đầu từ ô (0,0) (idx = 0), gán một số từ 1 đến 8 chưa được dùng.
- Tiếp tục với ô (0,1), (0,2), ..., (2,1), bỏ qua (2,2).
  
Kiểm tra ràng buộc:

- Ràng buộc All-Different: Đảm bảo không có số nào trùng lặp (dùng mảng used).
- Khi điền đủ 8 ô, kiểm tra trạng thái có khả thi (is_solvable) và có khớp với GOAL_STATE không.
  
Quay lui:

- Nếu trạng thái không thỏa mãn (không khả thi hoặc không khớp GOAL_STATE), quay lui: bỏ số vừa gán, thử số khác.
- Nếu thử hết số tại một ô mà không thành công, quay lui lên ô trước đó.

_Ưu điểm:_ Đơn giản, đảm bảo tìm được lời giải nếu có.

_Nhược điểm:_ Không hiệu quả vì phải thử tất cả khả năng, không tối ưu hóa miền giá trị trước khi gán.

![back](https://github.com/user-attachments/assets/100e083f-e42c-4f11-b2a2-2e8eab401839)

**AC-3 Search Algorithm**

_Mô tả thuật toán_

AC-3 (Arc Consistency Algorithm #3) là một thuật toán tiền xử lý trong CSP, dùng để giảm miền giá trị của các biến trước khi tìm kiếm. Sau đó, nó thường kết hợp với Backtracking để tìm lời giải. 

Cách hoạt động:
- Tính nhất quán cung (Arc Consistency): Với mỗi ràng buộc (cung) giữa 2 biến, loại bỏ các giá trị không phù hợp trong miền của biến.
- Hàng đợi cung: Duy trì một hàng đợi các cung cần kiểm tra, lặp lại cho đến khi không còn thay đổi hoặc phát hiện không có lời giải. Sau khi chạy AC-3, nếu miền của biến nào đó rỗng → Không có lời giải. Nếu không, kết hợp Backtracking để gán giá trị.

_Áp dụng vào 8-puzzle_

Biến và miền:

- 9 biến: Ô (0,0) đến (2,2).
- Miền ban đầu: Mỗi ô có thể nhận giá trị từ 0 đến 8.
  
Ràng buộc:

- All-Different giữa tất cả các ô.
- Ô (r, c) phải có giá trị đúng theo GOAL_STATE (ví dụ: (0,0) = 1, (2,2) = 0).
Bước thực hiện AC-3:

  Khởi tạo miền:
  
  - Ô (2,2) cố định là 0 → Miền: {0}.
  - Các ô khác: Miền ban đầu là {0, 1, ..., 8}.
  - Vì (2,2) = 0, loại 0 khỏi miền của tất cả ô khác → Miền các ô khác: {1, 2, ..., 8}.
    
  Hàng đợi cung:
  
  - Xem xét các cung giữa các biến (ô (i,j) và (p,q) phải khác nhau).
  - Với mỗi cung, kiểm tra và loại bỏ giá trị không thỏa mãn ràng buộc All-Different.
    
  Tính nhất quán:

  - Ví dụ: Ô (0,0) = 1 (theo GOAL_STATE), loại 1 khỏi miền của các ô khác.
  - Tiếp tục với (0,1) = 2, loại 2 khỏi miền của các ô còn lại, v.v.
  - Lặp lại cho đến khi không còn giá trị nào bị loại hoặc miền của một ô rỗng (thất bại).
    
Kết hợp Backtracking:

- Sau khi AC-3 chạy, miền của mỗi ô đã được thu hẹp.
- Dùng Backtracking để gán giá trị từ các miền đã thu hẹp, kiểm tra ràng buộc All-Different và GOAL_STATE.

_Ưu điểm:_ Giảm miền giá trị trước khi tìm kiếm, giúp Backtracking nhanh hơn.

_Nhược điểm:_ AC-3 chỉ đảm bảo nhất quán cung, không đảm bảo có lời giải. Vẫn cần Backtracking.

![ac3](https://github.com/user-attachments/assets/d746759d-0207-4ca4-8a45-4bc289b9de04)

**Forward Checking**

_Mô tả thuật toán_

Forward Checking là một cải tiến của Backtracking, kết hợp kiểm tra ràng buộc ngay trong quá trình gán giá trị:
- Khi gán giá trị cho một biến, ngay lập tức kiểm tra và loại bỏ các giá trị không hợp lệ khỏi miền của các biến liên quan (các biến chưa gán).
- Nếu miền của một biến trở thành rỗng, quay lui ngay lập tức.

_Áp dụng vào 8-puzzle_

Biến và miền:
- 9 biến: Ô (0,0) đến (2,2).
- Miền: Ban đầu {0, 1, ..., 8} cho mỗi ô.
  
Ràng buộc:
- All-Different.
- Trạng thái cuối phải khớp GOAL_STATE.
  
Bước thực hiện:

Khởi tạo:
- (2,2) = 0 → Loại 0 khỏi miền của các ô khác.
  
Gán và kiểm tra:

- Ô (0,0): Gán 1 (theo GOAL_STATE), loại 1 khỏi miền của các ô khác.
- Ô (0,1): Miền còn lại là {2, 3, ..., 8}, gán 2, loại 2 khỏi các ô còn lại.
- Nếu miền của một ô trở thành rỗng (ví dụ: không còn số nào để gán), quay lui ngay.
  
Tiếp tục:
- Lặp lại cho đến khi điền hết 8 ô, kiểm tra is_solvable và GOAL_STATE.
- Nếu không thỏa mãn, quay lui.

_Ưu điểm:_ Phát hiện sớm các nhánh không khả thi, nhanh hơn Backtracking đơn thuần.

_Nhược điểm:_ Vẫn chậm hơn AC-3 trong trường hợp miền giá trị lớn, vì không thu hẹp miền trước.

![forward](https://github.com/user-attachments/assets/dffd010c-d445-4d22-8fca-6ecb1a6636d8)

**So sánh 3 thuật toán trong 8-puzzle**
| **Tiêu chí**            | **Backtracking**                       | **AC-3**                                                | **Forward Checking**                               |
| ----------------------- | -------------------------------------- | ------------------------------------------------------- | -------------------------------------------------- |
| **Cách hoạt động**      | Gán giá trị, quay lui khi thất bại     | Thu hẹp miền giá trị trước, sau đó kết hợp với tìm kiếm | Gán và kiểm tra miền giá trị ngay khi gán          |
| **Hiệu quả**            | Thấp, thử tất cả khả năng              | Cao hơn Backtracking nhờ thu hẹp miền                   | Cao hơn Backtracking, thấp hơn AC-3                |
| **Phát hiện thất bại**  | Muộn, sau khi thử hết                  | Sớm, nếu miền giá trị bị rỗng sau thu hẹp               | Sớm, nếu miền giá trị bị rỗng ngay khi gán         |
| **Phức tạp triển khai** | Đơn giản                               | Phức tạp hơn (cần quản lý cung và cập nhật)             | Trung bình (quản lý miền giá trị động)             |
| **Độ phức tạp**         | `O(4^d)` (d là độ sâu), không gian lớn | `O(n^3)` để kiểm tra cung, không phù hợp trực tiếp      | `O(4^d)`, nhưng giảm nhánh nhờ kiểm tra sớm        |
| **Bộ nhớ sử dụng**      | Thấp, chỉ lưu đường đi hiện tại        | Cao, cần lưu toàn bộ đồ thị ràng buộc                   | Trung bình, lưu miền và trạng thái                 |
| **Áp dụng thực tế**     | Dễ triển khai, nhưng chậm              | Không áp dụng trực tiếp cho 8-Puzzle                    | Hiệu quả hơn Backtracking, dễ áp dụng cho 8-Puzzle |
| **Tính hoàn chỉnh**     | Có – nếu tồn tại lời giải sẽ tìm ra    | Không – chỉ là bước tiền xử lý cho thuật toán khác      | Có – nếu tồn tại lời giải sẽ tìm ra                |

**Kết luận**
Backtracking là phương pháp đơn giản nhất để triển khai cho 8-puzzle, nhưng hiệu suất thấp do không gian trạng thái lớn.
AC-3 không phù hợp trực tiếp cho 8-puzzle vì bài toán là động, nhưng có thể hữu ích trong bước tiền xử lý nếu định nghĩa lại bài toán dưới dạng CSP tĩnh.
Forward Checking là lựa chọn tốt hơn Backtracking, vì nó giảm số nhánh cần thử, nhưng vẫn không thể cạnh tranh với các thuật toán heuristic như A* trong 8-puzzle.

### 2.6. Học tăng cường (Reinforcement Learning)

Q-Learning là một thuật toán học tăng cường (Reinforcement Learning - RL) thuộc nhóm không cần mô hình (model-free), dựa trên kinh nghiệm thử-và-sai để học chính sách tối ưu mà không cần biết trước mô hình môi trường.

**Tổng quan về Q-Learning**

_Khái niệm cơ bản_

Q-Learning học một hàm giá trị hành động (Q-function) để ước lượng phần thưởng kỳ vọng trong tương lai cho mỗi cặp trạng thái-hành động (state-action pair). Mục tiêu là tìm chính sách tối ưu (policy) giúp tối đa hóa tổng phần thưởng dài hạn.

_Môi trường:_ Một tập trạng thái S, hành động A, và phần thưởng R

_Hàm Q:_ Q(s,a) biểu thị giá trị kỳ vọng của việc thực hiện hành động a trong trạng thái s, sau đó tuân theo chính sách tối ưu.

_Công thức cập nhật Q:_ 

![image](https://github.com/user-attachments/assets/738d8ff1-ce76-47b6-b582-90348946c4b0)
![image](https://github.com/user-attachments/assets/161cad31-128c-4c81-8400-e618056fb462)

_Chính sách hành động_

Q-Learning sử dụng chiến lược khám phá-khai thác (exploration-exploitation), thường thông qua chính sách <math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi>ϵ</mi></mrow><annotation encoding="application/x-tex"> \epsilon </annotation></semantics></math>-greedy:

- Với xác suất <math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi>ϵ</mi></mrow><annotation encoding="application/x-tex"></annotation></semantics></math>, chọn hành động ngẫu nhiên (khám phá).

- Với xác suất <math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mn>1</mn><mo>−</mo><mi>ϵ</mi></mrow><annotation encoding="application/x-tex"> </annotation></semantics></math>, chọn hành động có giá trị Q cao nhất (khai thác).

**Áp dụng Q-Learning cho 8-Puzzle**

_Định nghĩa bài toán:_ Trong 8-puzzle

- Trạng thái (S): Mỗi cấu hình của bảng 3x3 là một trạng thái
- Hành động A: Các nước đi hợp lệ của ô trống ( lên xuống trái phải)
- Phần thưởng R: Định nghĩa phần thưởng để khuyến khích đạt mục tiêu
  - +100 nếu đạt goal
  - -1 cho mỗi bước di chuyển
- Mục tiêu: Tìm chính sách tối ưu để từ trạng thái ban đầu đạt trạng thái mục tiêu với tổng phần thưởng cao nhất.

_Quy trình hoạt động_

Khởi tạo bảng Q: Khởi tạo Q)s,a) = 0 cho tất cả các cặp trạng thái-hành động.

Lặp qua các episode (vòng lặp thử-và-sai):
- Bắt đầu từ trạng thái ban đầu (ví dụ: ((1, 2, 3), (4, 5, 6), (0, 7, 8))).
- Sử dụng chính sách <math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi>ϵ</mi></mrow><annotation encoding="application/x-tex"> </annotation></semantics></math>-greedy để chọn hành động:
    - Nếu ngẫu nhiên: chọn một trong các nước đi (lên, xuống, trái, phải).
    - Nếu khai thác: chọn hành động Q(s,a) cao nhất
- Thực hiện hành động, nhân phần thưởng r, và chuyển sang trạng thái mới s(t+1)
- Cập nhật giá trị Q theo công thức trên

Lặp lại: Tiếp tục cho đến khi đạt trạng thái mục tiêu hoặc hết số bước tối đa trong episode. Lặp lại nhiều episode để bảng Q hội tụ.

Sử dụng chính sách: Sau khi học, chọn hành động có giá trị Q cao nhất ở mỗi trạng thái để đạt mục tiêu.

**Ưu điểm của Q-Learning trong 8-Puzzle**
Không cần mô hình: Q-Learning không yêu cầu biết trước mô hình môi trường (chuyển trạng thái 
hay phần thưởng), phù hợp với các bài toán phức tạp như 8-puzzle.

Học từ kinh nghiệm: Thuật toán tự học thông qua thử-và-sai, không cần dữ liệu huấn luyện.

Hội tụ: Với số episode đủ lớn và tham số hợp lý, Q-Learning đảm bảo hội tụ về chính sách tối ưu.
Linh hoạt: Có thể áp dụng cho các môi trường ngẫu nhiên hoặc không xác định.

Nhược điểm của Q-Learning trong 8-Puzzle

Không gian trạng thái lớn: 8-puzzle có khoảng 181,440 trạng thái khả thi (9!/2). Lưu trữ bảng Q cho tất cả cặp trạng thái-hành động (mỗi trạng thái có tối đa 4 hành động) đòi hỏi bộ nhớ lớn (~725,760 giá trị Q).

Tốc độ học chậm: Do không sử dụng heuristic, Q-Learning cần nhiều episode để học đường đi tối ưu, đặc biệt với bài toán phức tạp như 8-puzzle.

Khám phá không hiệu quả: Chính sách epsilon-greedy có thể dẫn đến việc thử nhiều hành động không cần thiết, làm tăng thời gian học.
Phần thưởng thưa thớt: Nếu phần thưởng chỉ được trao khi đạt mục tiêu (+100), thuật toán có thể gặp khó khăn trong việc học vì phần thưởng thưa thớt (sparse reward).

![Q](https://github.com/user-attachments/assets/c1df615e-9599-4ab5-84a6-f4e0945817f6)

**Cải tiến để áp dụng hiệu quả hơn trong 8-Puzzle**

Sử dụng phần thưởng thông minh hơn: Thay vì chỉ thưởng khi đạt mục tiêu, có thể thưởng dựa trên khoảng cách heuristic (như Manhattan Distance) để giảm vấn đề phần thưởng thưa thớt.

Giảm không gian trạng thái: Sử dụng các kỹ thuật như bảng Q gần đúng (approximation) hoặc mạng nơ-ron (Deep Q-Learning) để xử lý không gian trạng thái lớn.

Tăng tốc khám phá: Sử dụng chiến lược khám phá thông minh hơn, như UCB (Upper Confidence Bound), thay vì epsilon-greedy

Kết hợp với heuristic: Dùng heuristic (như Manhattan Distance) để khởi tạo bảng Q hoặc hướng dẫn quá trình học.

**Kết luận:**

Q-Learning là một thuật toán mạnh mẽ trong học tăng cường, phù hợp với các bài toán không cần mô hình môi trường. Tuy nhiên, trong 8-puzzle, nó không phải là lựa chọn tối ưu do không gian trạng thái lớn và tốc độ học chậm. Các thuật toán như A* (sử dụng heuristic) thường hiệu quả hơn trong bài toán này. Tuy nhiên, nếu môi trường thay đổi hoặc không xác định (ví dụ: phần thưởng ngẫu nhiên), Q-Learning có thể là lựa chọn tốt nhờ tính linh hoạt của nó.

---

## 3. Kết luận

Ứng dụng hỗ trợ học và so sánh trực quan các nhóm thuật toán AI đã cung cấp một nền tảng hiệu quả để đánh giá và phân tích hiệu suất của các phương pháp giải quyết bài toán 8-puzzle.

**Tìm kiếm có thông tin (Informed Search):** Bao gồm A*, IDA*, và Greedy. Nhóm này nổi bật với khả năng sử dụng heuristic để hướng dẫn tìm kiếm, mang lại kết quả tốt và ổn định. A* tối ưu hóa đường đi ngắn nhất bằng cách cân bằng chi phí đã đi và ước lượng chi phí còn lại (thường dùng Manhattan Distance), phù hợp với các bài toán yêu cầu hiệu quả cao. IDA* cải thiện bộ nhớ bằng cách giới hạn độ sâu tìm kiếm, trong khi Greedy nhanh nhưng có thể không đảm bảo đường đi tối ưu do chỉ tập trung vào heuristic. Nhóm này đặc biệt hiệu quả trong không gian trạng thái lớn như 8-puzzle khi cần kết quả chính xác.

**Tìm kiếm không thông tin (Uninformed Search):** Bao gồm BFS, IDS, DFS, và UCS. Nhóm này không sử dụng heuristic, dẫn đến hiệu suất phụ thuộc vào cách duyệt không gian trạng thái. BFS đảm bảo tìm đường ngắn nhất nhưng tiêu tốn nhiều bộ nhớ do lưu trữ toàn bộ không gian. IDS kết hợp ưu điểm của DFS và BFS, giảm bộ nhớ nhưng chậm hơn do lặp lại tìm kiếm. DFS tiết kiệm bộ nhớ nhưng dễ mắc kẹt trong nhánh sâu, trong khi UCS ưu tiên chi phí thấp nhưng hiệu quả giảm trong không gian lớn. Nhóm này phù hợp với bài toán nhỏ hoặc khi không có thông tin heuristic.

**Tìm kiếm cục bộ (Local Search):** Bao gồm các thuật toán như Simple Hill Climbing, Steepest Ascent Hill Climbing, Stochastic Hill Climbing, Simulated Annealing, Genetic Algorithm, và Beam Search. Nhóm này tập trung vào tối ưu hóa cục bộ hoặc toàn cục, phù hợp với bài toán không cần đường đi chính xác mà chỉ cần trạng thái mục tiêu. Hill Climbing các loại nhanh nhưng dễ mắc cục bộ (local optima), trong khi Simulated Annealing vượt qua hạn chế này nhờ cơ chế nhiệt độ ngẫu nhiên. Genetic Algorithm mạnh mẽ trong tìm kiếm toàn cục thông qua tiến hóa, nhưng tốn kém về tính toán. Beam Search cân bằng giữa hiệu quả và bộ nhớ bằng cách giữ lại số lượng hạn chế trạng thái tốt nhất. Nhóm này lý tưởng cho các bài toán phức tạp hoặc khi cần giải nhanh.

**Học tăng cường (Reinforcement Learning):** Q-Learning mở rộng khả năng giải quyết khi không cần mô hình môi trường rõ ràng, dựa trên kinh nghiệm thử-và-sai để học chính sách tối ưu. Dù hiệu quả trong các môi trường không xác định, nó gặp hạn chế do không gian trạng thái lớn và tốc độ học chậm trong 8-puzzle. Các cải tiến như phần thưởng heuristic hoặc Deep Q-Learning có thể nâng cao hiệu quả.

**Tìm kiếm trong môi trường có ràng buộc (Constraint Satisfaction Problem - CSP):** Các thuật toán như Backtracking, AC-3, và Forward Checking thích hợp để tạo và xác nhận trạng thái ban đầu hợp lệ. Backtracking cung cấp cách tiếp cận cơ bản nhưng chậm, trong khi Forward Checking cải thiện bằng cách loại bỏ sớm các nhánh không khả thi. AC-3, dù không tối ưu trực tiếp, hữu ích trong tiền xử lý để giảm miền giá trị, đặc biệt khi định nghĩa lại bài toán dưới dạng CSP tĩnh.

**Tìm kiếm trong môi trường phức tạp (Search in Complex Environment):** Các phương pháp như And-Or Search, Partially Observable Search, và Belief State Search hỗ trợ thử nghiệm thuật toán trong điều kiện bất định và thiếu thông tin. And-Or Search phù hợp với hành động phụ thuộc, trong khi Partially Observable Search và Belief State Search xử lý tốt môi trường không quan sát hoàn chỉnh bằng cách duy trì tập belief states. Chúng đặc biệt hữu ích trong các kịch bản thực tế như robot giải puzzle với cảm biến hạn chế.
