from vietnamese import Vietnamese
import re

def separate_words(paragraph):
    # Define the regular expression pattern to split the paragraph into words
    pattern = r'\b\w+\b'  # This pattern matches word boundaries (\b), followed by one or more word characters (\w+), and another word boundary (\b)

    # Use re.findall to extract all matching words from the paragraph
    words = re.findall(pattern, paragraph)

    return words


corpus = "chỉnh sửa lại những kí tự lỗi khi chuyển từ html sang dạng text gì gìn giữ"
corpus = """
Hàng chục ngàn phương tiện bị ghi hình vi phạm luật giao thông ở TP.HCM, bị 'bêu tên' nhưng chủ vẫn không chịu nộp phạt.
Trên cổng thông tin điện tử của Công an TP.HCM (CATP), mục thông tin về phương tiện vi phạm hành chính qua hình ảnh (từ ngày 4.1.2017 - 4.1.2018), có ghi nhận biển số xe, lỗi vi phạm, ngày vi phạm của 34.118 phương tiện (ô tô) chưa nộp phạt.
Đây là các phương tiện vi phạm được camera (di động hoặc cố định) của CATP ghi hình phạt nguội .
Điều đáng nói, dù Phòng CSGT đường bộ - đường sắt (PC67), CATP nhiều lần gửi giấy thông báo vi phạm về công an địa phương nhưng chủ hoặc người điều khiển phương tiện vẫn chưa thực hiện quyết định xử phạt hành chính.
Phổ biến nhất là lỗi đỗ không đúng nơi quy định.
Chẳng hạn từ tháng 1 - 7.2017, ô tô BS: 14A-130... 23 lần đỗ không đúng nơi quy định trên đường Hàm Nghi, Q.1; từ tháng 3 - 10.2017, ô tô BS: 30S-087... 34 lần đỗ trên đường Nguyễn Cư Trinh, Q.1; từ tháng 4 - 10.2017, ô tô BS: 86B-0066... 34 lần đỗ trên đường Nguyễn Cư Trinh, Q.1; từ tháng 5 - 12.2017, ô tô BS: 86B-0074... 27 lần đỗ trên đường Nguyễn Cư Trinh, Q.1; từ tháng 4 - 10.2017, ô tô BS: 84B-0023... 9 lần đỗ trên đường Trần Phú, Q.5... Từ đầu năm 2017 đến nay, PC67 nhiều lần gửi thông báo vi phạm, thậm chí bêu tên trên Cổng thông tin điện tử của CATP nhưng phương tiện vẫn tái phạm.
Cần có biện pháp mạnh Theo trung tá Phạm Công Danh, Đội trưởng Đội chỉ huy giao thông và điều khiển đèn tín hiệu giao thông (PC67), khi hoàn tất thủ tục xe vi phạm, CSGT sẽ in thông báo vi phạm thể hiện đầy đủ nội dung vi phạm gửi về công an phường, xã, thị trấn và chuyển qua đường bưu điện với các xe biển số tỉnh thành khác.
Công an địa phương sẽ chuyển thông báo vi phạm đến chủ phương tiện và mời chủ phương tiện đến trụ sở đội (số 52 - 54 Nguyễn Khắc Nhu, P.Cô Giang, Q.1) để giải quyết vụ việc.
Ghi hình xe đậu đỗ vi phạm ở trung tâm thành phố Tuy nhiên, việc cưỡng chế người vi phạm nộp phạt vẫn chưa hiệu quả, chưa đủ sức răn đe.
Từ năm 2017 đến nay, PC67 trích xuất 49.704 trường hợp vi phạm nhưng mới chỉ xử phạt được 16.106 trường hợp (đạt tỷ lệ 32,4%).
Việc cưỡng chế nộp phạt này chưa hiệu quả.
Lý giải về việc này, thượng tá Phạm Công Danh nhìn nhận: Người vi phạm không đến đóng phạt là do: chủ xe mua bán không sang tên đổi chủ nên việc chuyển thông báo vi phạm đến tay chủ phương tiện còn chậm hoặc không thể đến được; chủ phương tiện thường xuyên thay đổi chỗ ở, doanh nghiệp (DN) giải thể hoặc chủ phương tiện đã qua đời, xuất cảnh; chủ phương tiện né tránh không chấp hành... .
Theo một trưởng công an phường của CATP, khi cảnh sát khu vực gửi thông báo vi phạm, nếu xác định địa chỉ không có tên người vi phạm thì chuyển lại cho PC67.
Công an phường không có thời gian xác minh tiếp.
Trường hợp có yêu cầu của cơ quan tố tụng thì công an phường mới truy tìm đến cùng.
Điều này có thể thấy, nguyên nhân chính vẫn là do công an địa phương chưa quyết tâm làm đến cùng.
Bởi với quy định hiện hành, nếu cơ quan công an làm hết trách nhiệm thì cũng dễ dàng tìm ra chủ phương tiện, người điều khiển phương tiện vi phạm.
Khi người dân có nhu cầu chuyển hộ khẩu đi nơi khác thì đến phường, quận xin phiếu thay đổi hộ khẩu, có ghi rõ địa chỉ đi - đến; sau đó nộp cho quận xin cắt khẩu (nơi đi), nhập vào nơi đến.
Trường hợp nếu bán nhà, mua nhà mới nhưng không cắt khẩu thì khi đến nơi mới phải đăng ký tạm trú tạm vắng, trong vòng 12 tháng, nếu đủ điều kiện nhập khẩu mà không nhập sẽ bị xử phạt , một lãnh đạo Phòng Cảnh sát quản lý hành chính về trật tự xã hội (PC64), CATP, cho biết.
Để hiệu quả hơn trong cưỡng chế người vi phạm nộp phạt, trung tá Nguyễn Văn Bình, Đội trưởng Đội tham mưu (PC67), CATP, khẳng định: Thời gian tới, phương tiện của DN vận tải, PC67 sẽ mời DN đến nhận thông báo vi phạm, yêu cầu chuyển đến tận tay tài xế vi phạm và có trách nhiệm đôn đốc tài xế vi phạm chấp hành đóng phạt.
PC67 tuần tra, kiểm soát phối hợp tra cứu trực tiếp trên máy tính để phát hiện phương tiện vi phạm qua hình ảnh mà đã có thông báo chưa đến nộp phạt thì tổ tra cứu sẽ thông báo cho tổ CSGT tuần tra cho dừng xe kiểm tra, lập biên bản yêu cầu chủ phương tiện đến trụ sở CSGT để giải quyết vụ việc.
Thông qua các vụ vi phạm hành chính thông thường, khi người vi phạm đến nộp phạt, cán bộ làm công tác xử lý vi phạm (thuộc tất cả các đơn vị đội, trạm CSGT thuộc PC67) sẽ tra cứu trên máy tính để phát hiện có vi phạm qua hình ảnh trước đó mà chưa nộp phạt hay không, CSGT sẽ yêu cầu người vi phạm hiện hữu thông báo cho chủ phương tiện biết và đến trụ sở CSGT để giải quyết vụ việc .
Ngoài ra, một cán bộ của CATP, đề nghị: Nên quy định khi người dân đăng ký xe bắt buộc phải mở tài khoản, ký quỹ nhất định, sau đó trừ vào tài khoản nếu vi phạm.
PC67 tìm không ra chủ xe, người điều khiển phương tiện vi phạm thì không thể ra quyết định xử phạt, rồi bỏ qua, cứ lòng vòng hoài là không được .
Theo trung tá Nguyễn Văn Bình, hiện trang điện tử của PC67 đang nâng cấp nên mục thông tin về phương tiện vi phạm hành chính qua hình ảnh được đưa lên Cổng thông tin điện tử của CATP (http://catphcm.bocongan.gov.vn).
Người dân có thể vào địa chỉ này để xem biển số xe, lỗi vi phạm, địa chỉ đến giải quyết... Theo trung tá Bình, hiện nay hằng ngày, PC67 còn bố trí một tổ công tác trên đường Mai Chí Thọ, Q.2 (bên kia hầm vượt sông Sài Gòn) để phạt nguội các phương tiện vi phạm qua hình ảnh mà chưa nộp phạt bên cạnh việc xử lý các phương tiện tham gia lưu thông qua hầm vi phạm luật giao thông.
Với các trường hợp chây ì nộp phạt, trung tá Huỳnh Trung Phong, Trưởng PC67 khẳng định sẽ nghiên cứu để áp dụng: Đối với các tình tiết tăng nặng như tái phạm nhiều lần... thì sẽ tăng khung hình phạt lên mức cao nhất .
Chặn xe vi phạm chưa nộp phạt nguội để xử lý Ảnh: Nguyên Bảo Về tình trạng này PC67 (Công an Hà Nội) cũng cho biết các chủ phương tiện cố ý chây ì không chấp hành phạt nguội, PC67 sẽ đưa vào danh sách gửi sang Cục Đăng kiểm để phối hợp xử lý.
Chưa làm hết trách nhiệm Theo tiến sĩ Phạm Sanh (chuyên gia lĩnh vực GTVT tại TP.HCM), nhiều nước áp dụng phương tiện kỹ thuật (trong đó có camera - PV) hơn 20 năm nay nhưng đa phần phạt nguội (tức phạt qua camera), ít phạt nóng; phạt nóng đối với những trường hợp nghiêm trọng.
Họ sử dụng công nghệ hiện đại từ lâu để giảm lực lượng xử phạt tại chỗ.
"""
corpus = "kiểm soát phối hợp tra cứu trực tiếp trên máy tính để phát hiện phương tiện vi phạm qua hình ảnh mà đã có thông báo chưa đến nộp phạt thì tổ tra cứu sẽ thông báo"
print(corpus.lower())

for word in corpus.split():
    print(Vietnamese.CRT(word))