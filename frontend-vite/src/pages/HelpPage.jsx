import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

export default function HelpPage() {
  const navigate = useNavigate();
  // QUY ƯỚC:
  // - Nội dung chỉ là văn bản -> dùng chuỗi "..."
  // - Nội dung có <b> hoặc sau này sẽ là liên kết -> dùng JSX (<>...</>)
  const sections = [
    {
      icon: "🚀",
      title: "Bắt đầu",
      desc: "Giới thiệu tổng quan về FamilyTree, đối tượng sử dụng và cách bắt đầu làm quen với hệ thống.",

      goal: "Giúp người dùng hiểu FamilyTree là gì, dành cho ai và cách bắt đầu sử dụng hệ thống gia phả.",

      learnTitle: "📖 Bạn sẽ biết được",

      learnItems: [
        "FamilyTree dùng để làm gì.",
        "Ai được quyền sử dụng hệ thống.",
        "Cách sử dụng hệ thống qua các mục hướng dẫn.",
        "Có thể chọn bất cứ mục nào để xem hướng dẫn.",
        <>
          Nhưng trước hết bạn phải <b>Đăng nhập hệ thống</b>.
        </>
      ],

      nextTitle: "💡 Bước tiếp theo",
      
      nextText: (
        <>
          Tiếp tục đọc Mục 2:{" "}
          <span
            className="font-bold text-blue-600 cursor-pointer hover:underline"
            onClick={() => goToSection("Đăng nhập hệ thống")}
          >
            Đăng nhập hệ thống
          </span>{" "}
          để đăng nhập vào FamilyTree và biết quyền sử dụng của tài khoản.
        </>
      )
    },
    {
      icon: "👤",
      title: "Đăng nhập hệ thống",
      desc: "Đăng nhập để hệ thống nhận diện tài khoản của bạn và cấp đúng quyền sử dụng FamilyTree.",
    
      goal:
        "Giúp người dùng đăng nhập đúng tài khoản, biết mình được sử dụng những chức năng nào và có quyền xem, thêm hoặc sửa những thông tin nào trong FamilyTree.",
    
      learnTitle: "📖 Bạn sẽ thực hiện được",
    
      learnItems: [
        "Đăng nhập đúng tài khoản đã được cấp.",
        "Biết tài khoản của mình thuộc nhóm quyền nào.",
        "Biết mình được sử dụng những chức năng nào.",
        "Biết mình có quyền xem, thêm hoặc sửa những thông tin nào trong FamilyTree."
      ],
    
      nextTitle: "💡 Bước tiếp theo",
      nextText: (
        <>
          Tiếp tục đọc Mục 3:{" "}
          <span
            className="font-bold text-blue-600 cursor-pointer hover:underline"
            onClick={() => goToSection("Những điều cần lưu ý")}
          >
            Những điều cần lưu ý
          </span>{" "}
          để tránh những sai sót thường gặp khi sử dụng FamilyTree.
        </>
      )
    },
    {
      icon: "⚠️",
      title: "Những điều cần lưu ý",
      desc: "Đọc những lưu ý quan trọng trước khi cập nhật dữ liệu để đảm bảo tính chính xác và an toàn của gia phả.",

      goal: "Giúp người dùng hiểu những nguyên tắc cần tuân thủ khi sử dụng FamilyTree để bảo vệ dữ liệu gia phả và tránh những sai sót không đáng có.",

      learnTitle: "📖 Bạn cần lưu ý",

      learnItems: [
        "Không chia sẻ tài khoản và mật khẩu cho người ngoài gia tộc hoặc người không có trách nhiệm.",
        "Chỉ cập nhật và sửa thông tin khi bạn có quyền và bạn chắc chắn nội dung là chính xác.",
        "Kiểm tra kỹ dữ liệu trước khi lưu.",
        "Nếu không chắc chắn, hãy hỏi người quản trị hoặc người có trách nhiệm trong dòng họ.",
        "Mỗi thông tin bạn cập nhật đều góp phần giữ gìn sự chính xác của gia phả cho các thế hệ sau.",
        "Hãy sử dụng FamilyTree với tinh thần tôn trọng sự thật lịch sử và gìn giữ truyền thống của dòng họ."
      ],

      nextTitle: "💡 Bước tiếp theo", 

      nextText: (
        <>
          Tiếp tục đọc Mục 4:{" "}
          <span
            className="font-bold text-blue-600 cursor-pointer hover:underline"
            onClick={() => goToSection("Xem cây gia phả")}
          >
            Xem cây gia phả
          </span>{" "}
          để biết cách xem cây gia phả của dòng họ.
        </>
      )
    },
    {
      icon: "🌳",
      title: "Xem cây gia phả",
      desc: "Xem vị trí của bản thân, cha mẹ, ông bà, con cái và một phần cây gia phả.",

      goal: "Giúp người dùng biết cách xem cây gia phả, xác định vị trí của mình trong dòng họ và mối quan hệ giữa các thành viên.",

      learnTitle: "📖 Bạn sẽ xem được",

      learnItems: [
        "Vị trí của bạn trong cây gia phả.",
        <>
          Để xem cây gia phả của một thành viên hay chính bạn, trước hết bạn phải vào{" "}
          <span
            className="font-bold text-blue-600 cursor-pointer hover:underline"
            onClick={() => goToPage("/person")}
          >
            Danh sách thành viên
          </span>.
        </>,
        "Tìm tên thanh viên bạn muốn xem. Click vào nút cây gia phả",
        "Bạn xem được Cha mẹ, ông bà, con cháu và những người thân trong dòng họ (nếu bạn có quyền xem).",
        "Bằng cách nhấp vào ảnh đại diện (avatar) để xem các nhánh liên hệ. Nếu không mở được nghĩa là bạn không có mối quan hệ gần với người đó.",
        "Tên và ảnh đại diện (avatar) của các thành viên được hiển thị trên cây gia phả."
      ],

      nextTitle: "💡 Bước tiếp theo",

      nextText: (
        <>
          Tiếp tục đọc Mục 5:{" "}
          <span
            className="font-bold text-blue-600 cursor-pointer hover:underline"
            onClick={() => goToSection("Xem thông tin")}
          >
            Xem thông tin
          </span>{" "}
          để biết cách xem thông tin cơ bản / chi tiết của một thành viên trong FamilyTree.
        </>
      )
    },
    {
      icon: "👤",
      title: "Xem thông tin",
      desc: "Xem thông tin cơ bản hoặc thông tin chi tiết của một thành viên nếu bạn có quyền xem.",

      goal: "Giúp người dùng biết cách xem hoặc sửa thông tin của một thành viên nếu mình có quan hệ gần.",

      learnTitle: "📖 Bạn sẽ xem và thực hiện được",

      learnItems: [
        <>
          Để xem hoặc chỉnh sửa thông tin của một thành viên, trước hết bạn phải vào{" "}
          <span
            className="font-bold text-blue-600 cursor-pointer hover:underline"
            onClick={() => goToPage("/person")}
          >
            Danh sách thành viên
          </span>.
        </>,
        "Nhấn nút Sửa (biểu tượng cây bút chì) ở dòng của thành viên cần xem để mở màn hình thông tin.",
        "Bạn sẽ xem được thông tin cơ bản hoặc thông tin chi tiết của thành viên nếu bạn có quyền xem.",
        "Nếu không mở được màn hình thông tin, có nghĩa là bạn không có mối quan hệ gần hoặc không có quyền xem thành viên đó.",
        "Các thông tin hiển thị sẽ phụ thuộc vào quyền của tài khoản và mối quan hệ của bạn với thành viên đó."
      ],

      nextTitle: "💡 Bước tiếp theo",

      nextText: (
        <>
          Tiếp tục đọc Mục 6:{" "}
          <span
            className="font-bold text-blue-600 cursor-pointer hover:underline"
            onClick={() => goToSection("Thay avatar")}
          >
            Thay avatar
          </span>{" "}
          để biết cách thay đổi ảnh đại diện của thành viên.
        </>
      )
    },
    {
      icon: "🖼️",
      title: "Thay avatar",
      desc: "Cập nhật ảnh đại diện để dễ nhận biết các thành viên trong gia phả.",

      goal: "Giúp người dùng biết cách thay đổi ảnh đại diện của một thành viên để việc nhận biết các thành viên trong gia phả được dễ dàng hơn.",

      learnTitle: "📖 Bạn sẽ thực hiện được",

      learnItems: [
        <>
          Để thay ảnh đại diện, trước hết bạn phải vào{" "}
          <span
            className="font-bold text-blue-600 cursor-pointer hover:underline"
            onClick={() => goToPage("/person")}
          >
            Danh sách thành viên
          </span>.
        </>,
      
        "Nhấn nút Sửa (biểu tượng cây bút chì) ở dòng của thành viên cần thay ảnh.",
      
        'Nhấn vào ảnh đại diện (avatar) của thành viên, sau đó nhấn "Chọn ảnh". Hệ thống sẽ mở thư mục trên máy tính của bạn. Chọn ảnh mới rồi nhấn "Open". Ảnh sẽ hiển thị để bạn xem trước và có thể tiếp tục "Chọn ảnh khác" nếu chưa ưng ý. Khi đã đúng, nhấn "Upload avatar" để tải ảnh lên hệ thống.',
      
        'Nhấn "Lưu" để cập nhật ảnh đại diện. Nếu nhấn "Đóng chỉnh sửa" trước khi lưu, ảnh đại diện sẽ không được thay đổi.',
      
        "Nếu không thay được ảnh đại diện, có nghĩa là bạn không có quyền cập nhật thành viên đó."
      ],

      nextTitle: "💡 Bước tiếp theo",

      nextText: (
        <>
          Tiếp tục đọc Mục 7:{" "}
          <span
            className="font-bold text-blue-600 cursor-pointer hover:underline"
            onClick={() => goToSection("Sửa thông tin")}
          >
            Sửa thông tin
          </span>{" "}
          để biết cách cập nhật thông tin của một thành viên.
        </>
      )
    },
    {
      icon: "✏️",
      title: "Sửa thông tin",
      desc: "Cập nhật thông tin của một thành viên nếu bạn có quyền chỉnh sửa.",

      goal: "Giúp người dùng biết cách cập nhật thông tin của một thành viên và lưu các thay đổi vào FamilyTree.",

      learnTitle: "📖 Bạn sẽ thực hiện được",

      learnItems: [
        <>
          Để sửa thông tin của một thành viên, trước hết bạn phải vào{" "}
          <span
            className="font-bold text-blue-600 cursor-pointer hover:underline"
            onClick={() => goToPage("/person")}
          >
            Danh sách thành viên
          </span>.
        </>,
      
        "Nhấn nút Sửa (biểu tượng cây bút chì) ở dòng của thành viên cần cập nhật.",
      
        "Chỉnh sửa những thông tin bạn muốn cập nhật và bảo đảm nội dung là chính xác.",
      
        'Nhấn "Lưu" để cập nhật các thay đổi. Nếu nhấn "Đóng chỉnh sửa" trước khi lưu, các thay đổi sẽ không được cập nhật.',
      
        "Nếu không mở được màn hình chỉnh sửa, có nghĩa là bạn không có quyền cập nhật thành viên đó."
      ],

      nextTitle: "💡 Bước tiếp theo",

      nextText: (
        <>
          Tiếp tục đọc Mục 8:{" "}
          <span
            className="font-bold text-blue-600 cursor-pointer hover:underline"
            onClick={() => goToSection("Tìm mối quan hệ")}
          >
            Tìm mối quan hệ
          </span>{" "}
          để biết cách xác định cách xưng hô giữa hai thành viên.
        </>
      )
    },
    {
      icon: "🔎",
      title: "Tìm mối quan hệ",
      desc: "Phân tích và xác định cách xưng hô giữa hai thành viên trong FamilyTree.",

      goal: "Giúp người dùng chọn hai thành viên và phân tích xác định cách xưng hô giữa hai thành viên trong gia phả nếu hai người có mối quan hệ.",

      learnTitle: "📖 Bạn sẽ biết được",

      learnItems: [
        <>
          Để tìm mối quan hệ, trước hết bạn phải vào{" "}
          <span
            className="font-bold text-blue-600 cursor-pointer hover:underline"
            onClick={() => goToPage("/relation_finder")}
          >
            Tìm mối quan hệ
          </span>.
        </>,
      
        "Chọn đủ hai thành viên: Người thứ nhất và Người thứ hai trong danh sách. Bạn có thể gõ tên để tìm nhanh thay vì kéo danh sách.",
      
        'Nhấn nút "Phân tích" để hệ thống xác định cách xưng hô giữa hai người.',
      
        "Kết quả sẽ hiển thị cách xưng hô nếu hai người có mối quan hệ trong gia phả.",
      
        "Nếu bạn biết chính xác họ tên của hai thành viên, việc tìm kiếm sẽ nhanh và chính xác hơn."
      ],

      nextTitle: "💡 Bước tiếp theo",

      nextText: (
        <>
          Tiếp tục đọc Mục 9:{" "}
          <span
            className="font-bold text-blue-600 cursor-pointer hover:underline"
            onClick={() => goToSection("Thêm thành viên")}
          >
            Thêm thành viên
          </span>{" "}
          để biết cách thêm thành viên mới vào FamilyTree.
        </>
      )
    },
    {
      icon: "👥",
      title: "Thêm thành viên",
      desc: "Thêm một thành viên mới vào FamilyTree nếu bạn có quyền cập nhật.",

      goal: "Giúp người dùng biết cách thêm một thành viên mới vào FamilyTree và lưu đúng thông tin ban đầu.",

      learnTitle: "📖 Bạn sẽ thực hiện được",

      learnItems: [
        <>
          Để thêm thành viên mới, trước hết bạn phải vào{" "}
          <span
            className="font-bold text-blue-600 cursor-pointer hover:underline"
            onClick={() => goToPage("/person")}
          >
            Danh sách thành viên
          </span>.
        </>,
      
        'Nhấn nút "Thêm thành viên" để mở màn hình nhập thông tin thành viên mới.',
      
        "Nhập những thông tin bạn muốn bổ sung cho thành viên mới và bảo đảm nội dung là chính xác.",
      
        'Nhấn "Lưu" để thêm thành viên. Nhấn "Lưu và thêm mới" nếu bạn muốn tiếp tục thêm thành viên khác vào FamilyTree. Nếu nhấn "Hủy" trước khi "Lưu", thành viên mới sẽ không được tạo.',
      
        'Nếu trên màn hình chính không có nút "Thêm thành viên", có nghĩa là bạn không có quyền thêm thành viên.'
      ],

      nextTitle: "💡 Bước tiếp theo",

      nextText: (
        <>
          Tiếp tục đọc Mục 10:{" "}
          <span
            className="font-bold text-blue-600 cursor-pointer hover:underline"
            onClick={() => goToSection("Thiết lập quan hệ gia đình")}
          >
            Thiết lập quan hệ gia đình
          </span>{" "}
          để biết cách thiết lập quan hệ Cha - Mẹ - Con.
        </>
      )
    },
    {
      icon: "👨‍👩‍👧",
      title: "Thiết lập quan hệ gia đình",
      desc: "Thiết lập quan hệ Cha - Mẹ - Con để hình thành gia đình trong FamilyTree.",

      goal: "Giúp người dùng biết cách thiết lập quan hệ cha mẹ và con để hình thành cấu trúc gia đình trong cây gia phả.",

      learnTitle: "📖 Bạn sẽ thực hiện được",

      learnItems: [
        <>
          Để thiết lập gia đình, trước hết bạn phải vào{" "}
          <span
            className="font-bold text-blue-600 cursor-pointer hover:underline"
            onClick={() => goToPage("/family-setup")}
          >
            Thiết lập gia đình
          </span>.
        </>,
      
        "Bạn phải có mối quan hệ gần với ít nhất một trong ba thành viên: người Cha, người Mẹ hoặc người Con.",

        <>
        Có hai Tab: <b>"Quan hệ Gia đình & Con"</b> và <b>"Quan hệ Con & Cha/Mẹ"</b>. Bạn nên chọn Tab <b>"Quan hệ Con & Cha/Mẹ"</b> vì trong hầu hết các trường hợp người Con là thành viên mới và chưa có mối quan hệ với ai.
        </>,

        <>
        Tab <b>"Quan hệ Con & Gia đình"</b> thường được sử dụng khi thêm người Cha hoặc người Mẹ còn thiếu cho một người Con đã có Cha đơn thân hoặc Mẹ đơn thân và bạn có mối quan hệ gần với những thành viên này.
        </>,
      
        'Chọn "Không thuộc gia đình nào" nếu người Con được thiết lập với một người Cha hoặc một người Mẹ nhưng hai người này không có quan hệ hôn nhân với nhau.',

        'Bỏ chọn "Không thuộc gia đình nào" nếu người Con được thiết lập với một gia đình có cả Cha và Mẹ đã có quan hệ hôn nhân với nhau.',
      
        "Hệ thống sẽ thông báo rõ nguyên nhân trong từng trường hợp để bạn biết vì sao không thể thiết lập quan hệ gia đình cho thành viên này.",

        'Nhấn "Lưu Gia Đình" để hoàn thành việc thiết lập quan hệ Cha - Mẹ - Con.',

        'Nhấn "Hủy" nếu không muốn lưu các thay đổi.',

        'Nhấn "Thêm mới" để tiếp tục thiết lập mối quan hệ gia đình khác.',
      
        "Nếu không mở được màn hình thiết lập, có nghĩa là bạn không có quyền cập nhật các thành viên đó."
      ],

      nextTitle: "💡 Bước tiếp theo",

      nextText: (
        <>
          Tiếp tục đọc Mục 11:{" "}
          <span
            className="font-bold text-blue-600 cursor-pointer hover:underline"
            onClick={() => goToSection("Lập hôn nhân")}
          >
            Lập hôn nhân
          </span>{" "}
          để biết cách thiết lập quan hệ vợ chồng giữa hai thành viên.
        </>
      )
    },
    {
      icon: "💍",
      title: "Lập hôn nhân",
      desc: "Thiết lập quan hệ hôn nhân giữa hai thành viên trong FamilyTree.",

      goal: "Giúp người dùng biết cách thiết lập quan hệ hôn nhân giữa hai thành viên để hình thành gia đình trong cây gia phả.",

      learnTitle: "📖 Bạn sẽ thực hiện được",

      learnItems: [
        <>
          Để lập hôn nhân, trước hết bạn phải vào{" "}
          <span
            className="font-bold text-blue-600 cursor-pointer hover:underline"
            onClick={() => goToPage("/marriage")}
          >
            Lập hôn nhân
          </span>.
        </>,
      
        "Bạn phải có mối quan hệ gần với ít nhất một trong hai thành viên.",
      
        "Chọn hai thành viên bạn muốn thiết lập quan hệ hôn nhân.",
      
        "Chọn tình trạng hôn nhân phù hợp với mối quan hệ hôn nhân này.",

        "Nhập hoặc cập nhật các thông tin khác về hôn nhân nếu muốn. Nếu nhập ngày kết hôn, hệ thống sẽ tự động thông báo kỷ niệm ngày cưới.",
      
        "Kiểm tra lại thông tin của hai thành viên trước khi lưu.",
      
        'Nhấn "Lưu Hôn Nhân" để hoàn thành việc thiết lập quan hệ hôn nhân.',
      
        'Nhấn "Hủy" nếu không muốn lưu các thay đổi.',
      
        'Nhấn "Thêm mới" để tiếp tục thiết lập quan hệ hôn nhân khác.',
      
        "Hệ thống sẽ thông báo rõ nguyên nhân trong từng trường hợp để bạn biết vì sao không thể thiết lập quan hệ hôn nhân giữa hai thành viên.",
      
        "Nếu không mở được màn hình lập hôn nhân, có nghĩa là bạn không có quyền cập nhật một trong hai thành viên."
      ],

      nextTitle: "💡 Bước tiếp theo",

      nextText: (
        <>
          Tiếp tục đọc Mục 12:{" "}
          <span
            className="font-bold text-blue-600 cursor-pointer hover:underline"
            onClick={() => goToSection("Xem thông báo")}
          >
            Xem thông báo
          </span>{" "}
          để biết các thông báo quan trọng trong FamilyTree.
        </>
      )
    },
    {
      icon: "📢",
      title: "Xem thông báo",
      desc: "Theo dõi các thông báo quan trọng từ FamilyTree.",

      goal: "Giúp người dùng biết cách xem các thông báo của FamilyTree để không bỏ lỡ những sự kiện như ngày đám giỗ, sinh nhật, ngày cưới của gia đình và dòng họ.",

      learnTitle: "Bạn sẽ xem được",

      learnItems: [
        <>
          Để thiết lập quan hệ Cha - Mẹ - Con, trước hết bạn phải vào{" "}
          <span
            className="font-bold text-blue-600 cursor-pointer hover:underline"
            onClick={() => goToPage("/parent_child")}
          >
            Quan hệ Cha/Mẹ - Con
          </span>.
        </>,
      
        "Xem các thông báo do hệ thống tự động tạo hoặc do Ban quản trị gửi.",
      
        "Theo dõi các thông báo về sinh nhật, ngày giỗ, kỷ niệm ngày cưới và các sự kiện quan trọng khác.",
      
        "Đọc nội dung thông báo để biết những việc cần thực hiện hoặc những sự kiện sắp diễn ra.",
      
        "Các thông báo sẽ được cập nhật tự động khi có dữ liệu mới trong FamilyTree."
      ],

      nextTitle: "💡 Bước tiếp theo",

      nextText: (
        <>
          Tiếp tục đọc Mục 13:{" "}
          <span
            className="font-bold text-blue-600 cursor-pointer hover:underline"
            onClick={() => goToSection("Gửi góp ý")}
          >
            Gửi góp ý
          </span>{" "}
          để biết cách gửi góp ý hoặc báo lỗi cho Ban quản trị.
        </>
      )
    },
    {
      icon: "💬",
      title: "Gửi góp ý",
      desc: "Gửi góp ý, báo lỗi, báo những thông tin bạn nghi ngờ chưa chính xác hoặc đề xuất cải tiến cho FamilyTree.",

      goal: "Giúp người dùng biết cách gửi góp ý, báo lỗi hoặc đề xuất để FamilyTree ngày càng hoàn thiện hơn.",

      learnTitle: "📖 Bạn cần lưu ý",

      learnItems: [
        <>
          Để gửi góp ý, trước hết bạn phải vào{" "}
          <span
            className="font-bold text-blue-600 cursor-pointer hover:underline"
            onClick={() => goToPage("/feedback")}
          >
            Gửi góp ý
          </span>.
        </>,
      
        "Nhập tiêu đề và nội dung góp ý hoặc báo lỗi.",
      
        "Mô tả rõ vấn đề gặp phải hoặc đề xuất cải tiến để Ban quản trị dễ dàng kiểm tra và xử lý.",
      
        "Nếu có thể, hãy ghi rõ các bước thực hiện hoặc thời điểm xảy ra lỗi để việc kiểm tra được nhanh chóng và chính xác hơn. Đồng thời, hãy cung cấp số điện thoại hoặc địa chỉ email để Ban quản trị thuận tiện liên hệ khi cần.",
      
        'Nhấn "Gửi góp ý" để gửi nội dung đến Ban quản trị.',
      
        "Ban quản trị sẽ xem xét các góp ý và phản hồi hoặc cập nhật hệ thống khi cần thiết."
      ],

      nextTitle: "💡 Bước tiếp theo",

      nextText: (
        <>
          Tiếp tục đọc Mục 14:{" "}
          <span
            className="font-bold text-blue-600 cursor-pointer hover:underline"
            onClick={() => goToSection("Câu hỏi thường gặp")}
          >
            Câu hỏi thường gặp
          </span>{" "}
          để xem những câu hỏi và câu trả lời thường gặp khi sử dụng FamilyTree.
        </>
      )
    },
    {
      icon: "❓",
      title: "Câu hỏi thường gặp (FAQ)",
      desc: "Tra cứu nhanh những câu hỏi thường gặp và cách xử lý khi sử dụng FamilyTree. Nếu chưa tìm được câu trả lời, bạn có thể xem các bài Hướng dẫn & Hỗ trợ hoặc liên hệ người cộng tác khu vực.",

      goal: "Giúp người dùng nhanh chóng tìm được câu trả lời cho những câu hỏi thường gặp khi sử dụng FamilyTree.",

      learnTitle: "📖 Bạn sẽ tìm được câu trả lời",

      learnItems: [
        <>
        <b>NHÓM 1. ĐĂNG NHẬP TÀI KHOẢN</b>
        </>,

        <>
        <b>1. Tôi không đăng nhập được, phải làm gì?</b><br/>
        Hãy kiểm tra lại tên đăng nhập và mật khẩu. Nếu vẫn không đăng nhập được, có thể tài khoản của bạn chưa được cấp hoặc có vấn đề cần hỗ trợ.<br/>
        👉 Xem thêm: <b>Đăng nhập hệ thống</b>.
        </>,
        
        <>
        <b>2. Tại sao hệ thống báo tài khoản hoặc mật khẩu không đúng?</b><br/>
        Tên đăng nhập hoặc mật khẩu có thể chưa chính xác. Hãy kiểm tra lại chữ hoa, chữ thường, chữ số, ký tự đặc biệt, bảo đảm không có khoảng trắng thừa và đang gõ bằng tiếng Anh thay vì tiếng Việt.<br/>
        👉 Xem thêm: <b>Đăng nhập hệ thống</b>.
        </>,
        
        <>
        <b>3. Vì sao tôi bị đăng xuất?</b><br/>
        Phiên đăng nhập đã hết hạn để bảo đảm an toàn cho tài khoản. Bạn chỉ cần đăng nhập lại để tiếp tục sử dụng.<br/>
        👉 Xem thêm: <b>Đăng nhập hệ thống</b>.
        </>,
        
        <>
        <b>4. Tôi không có tài khoản thì phải làm thế nào?</b><br/>
        FamilyTree chỉ dành cho những người đã được cấp tài khoản. Nếu chưa có tài khoản, vui lòng liên hệ người cộng tác khu vực hoặc người quản trị để được cấp quyền sử dụng.
        </>,
        
        <>
        <b>5. Tôi có thể đổi mật khẩu không?</b><br/>
        Hiện tại FamilyTree chưa hỗ trợ người dùng tự đổi mật khẩu.
        </>,
        
        <>
        <b>6. Quyền và vai trò của tôi quyết định những gì?</b><br/>
        Vai trò của tài khoản và mối quan hệ gần sẽ quyết định những chức năng bạn được phép sử dụng cũng như phạm vi dữ liệu bạn được xem hoặc cập nhật.<br/>
        👉 Xem thêm: <b>Đăng nhập hệ thống</b>.
        </>,

        <>
        <b>NHÓM 2. XEM THÔNG TIN</b>
        </>,
        
        <>
        <b>7. Quan hệ gần là gì?</b><br/>
        Quan hệ gần là những thành viên có quan hệ huyết thống hoặc hôn nhân gần gũi với bạn theo quy định của FamilyTree. Quan hệ này quyết định bạn được xem hoặc cập nhật thông tin của những thành viên nào.
        </>,
        
        <>
        <b>8. Vì sao tôi không xem được cây gia phả?</b><br/>
        Bạn chỉ xem được cây gia phả khi có quyền xem và có quan hệ gần với thành viên đó.<br/>
        👉 Xem thêm: <b>Xem cây gia phả</b>.
        </>,
        
        <>
        <b>9. Vì sao tôi không xem được thông tin chi tiết của một thành viên?</b><br/>
        Thông tin chi tiết chỉ hiển thị khi bạn có quyền xem đối với thành viên đó.<br/>
        👉 Xem thêm: <b>Xem thông tin thành viên</b>.
        </>,
        
        <>
        <b>10. Vì sao tôi không xem được thông tin gia đình?</b><br/>
        Thông tin gia đình chỉ hiển thị khi bạn có quyền xem đối với thành viên đó.<br/>
        👉 Xem thêm: <b>Xem thông tin gia đình</b>.
        </>,
        
        <>
        <b>11. Vì sao tôi không tìm thấy một thành viên?</b><br/>
        Hãy kiểm tra lại họ tên hoặc thử nhập ít ký tự hơn để tìm kiếm. Nếu vẫn không thấy, thành viên đó có thể chưa được thêm vào gia phả hoặc bạn không có quyền xem.
        </>,
        
        <>
        <b>12. Vì sao tôi không tìm được mối quan hệ giữa hai thành viên?</b><br/>
        Mối quan hệ chỉ được xác định khi dữ liệu Cha/Mẹ, Con và Hôn nhân đã được thiết lập đầy đủ.<br/>
        👉 Xem thêm: <b>Tìm mối quan hệ</b>.
        </>,

        <>
        <b>NHÓM 3. CẬP NHẬT THÔNG TIN</b>
        </>,

        <>
        <b>13. Vì sao tôi không sửa được thông tin thành viên?</b><br/>
        Bạn chỉ được cập nhật những thành viên mà mình có quyền chỉnh sửa theo quy định của FamilyTree.<br/>
        👉 Xem thêm: <b>Sửa thông tin thành viên</b>.
        </>,

        <>
        <b>14. Vì sao tôi không thay được ảnh đại diện (Avatar)?</b><br/>
        Bạn chỉ có thể thay ảnh đại diện của những thành viên mà mình có quyền cập nhật.<br/>
        👉 Xem thêm: <b>Thay ảnh đại diện (Avatar)</b>.
        </>,

        <>
        <b>15. Vì sao tôi không thêm được thành viên mới?</b><br/>
        Chỉ tài khoản có vai trò <b>Viewer</b> mới không được phép thêm thành viên mới.<br/>
        👉 Xem thêm: <b>Thêm thành viên mới</b>.
        </>,

        <>
        <b>16. Vì sao tôi không lưu được thông tin sau khi chỉnh sửa?</b><br/>
        Dữ liệu bạn nhập có thể chưa hợp lệ, còn thiếu thông tin bắt buộc hoặc chưa đúng định dạng theo quy định của hệ thống.<br/>
        👉 Xem thêm: <b>Sửa thông tin thành viên</b>.
        </>,

        <>
        <b>17. Tôi lỡ nhập sai thông tin thì phải làm thế nào?</b><br/>
        Hãy mở lại <b>Danh sách thành viên</b>, tìm đúng thành viên và nhấn <b>Sửa</b> để cập nhật lại thông tin cho chính xác.<br/>
        👉 Xem thêm: <b>Sửa thông tin thành viên</b>.
        </>,

        <>
        <b>18. Tôi có thể cập nhật thông tin của bất kỳ thành viên nào trong gia phả không?</b><br/>
        Không. Bạn chỉ được cập nhật những thành viên thuộc phạm vi quyền của mình theo quy định của FamilyTree.
        </>,

        <>
        <b>NHÓM 4. THIẾT LẬP QUAN HỆ</b>
        </>,

        <>
        <b>19. Vì sao tôi không lập được hôn nhân?</b><br/>
        Bạn chỉ có thể lập quan hệ hôn nhân khi có quyền cập nhật đối với ít nhất một trong hai thành viên.<br/>
        👉 Xem thêm: <b>Lập hôn nhân</b>.
        </>,

        <>
        <b>20. Vì sao tôi không thiết lập được quan hệ Cha - Mẹ - Con?</b><br/>
        Việc thiết lập quan hệ phải đáp ứng các quy định của FamilyTree. Nếu chưa thực hiện được, hệ thống sẽ thông báo nguyên nhân cụ thể.<br/>
        👉 Xem thêm: <b>Thiết lập gia đình</b>.
        </>,

        <>
        <b>21. Vì sao hệ thống báo đã có Cha hoặc đã có Mẹ?</b><br/>
        Mỗi người chỉ có một Cha và một Mẹ trong cây gia phả. Hệ thống sẽ không cho phép tạo dữ liệu trùng lặp.<br/>
        👉 Xem thêm: <b>Thiết lập gia đình</b>.
        </>,

        <>
        <b>22. Vì sao tôi không tìm được người cần lập quan hệ?</b><br/>
        Hãy kiểm tra lại họ tên hoặc thử nhập ít ký tự hơn để tìm kiếm thành viên trong danh sách.<br/>
        👉 Xem thêm: <b>Lập hôn nhân</b> hoặc <b>Thiết lập gia đình</b>.
        </>,

        <>
        <b>23. Tôi lập nhầm quan hệ thì phải làm thế nào?</b><br/>
        Hãy mở lại chức năng tương ứng để kiểm tra và điều chỉnh. Nếu không thể tự xử lý, vui lòng liên hệ người cộng tác khu vực hoặc người quản trị.
        </>,

        <>
        <b>24. Vì sao kết quả quan hệ không đúng như tôi mong muốn?</b><br/>
        Kết quả phụ thuộc vào dữ liệu đã được nhập trong gia phả. Nếu dữ liệu chưa đầy đủ hoặc chưa chính xác, kết quả xác định quan hệ cũng sẽ chưa chính xác.<br/>
        👉 Xem thêm: <b>Tìm mối quan hệ</b>.
        </>,

        <>
        <b>NHÓM 5. GÓP Ý VÀ HỖ TRỢ</b>
        </>,

        <>
        <b>25. Tôi muốn góp ý để FamilyTree tốt hơn thì làm thế nào?</b><br/>
        Mọi ý kiến đóng góp đều được ghi nhận để FamilyTree ngày càng hoàn thiện.<br/>
        👉 Xem thêm: <b>Gửi góp ý</b>.
        </>,

        <>
        <b>26. Tôi phát hiện thông tin trong gia phả bị sai thì phải làm gì?</b><br/>
        Nếu có quyền cập nhật, bạn có thể chỉnh sửa lại. Nếu không có quyền, vui lòng gửi góp ý hoặc thông báo cho người cộng tác khu vực.
        </>,

        <>
        <b>27. Tôi phát hiện lỗi của phần mềm thì báo ở đâu?</b><br/>
        Hãy sử dụng chức năng <b>Gửi góp ý</b> và mô tả rõ lỗi gặp phải để người quản trị kiểm tra và xử lý.<br/>
        👉 Xem thêm: <b>Gửi góp ý</b>.
        </>,

        <>
        <b>28. FamilyTree có tiếp tục được cập nhật không?</b><br/>
        FamilyTree sẽ tiếp tục được cải tiến và bổ sung chức năng dựa trên nhu cầu sử dụng thực tế và các ý kiến đóng góp của người dùng.
        </>,

        <>
        <b>29. Tôi có thể đề nghị bổ sung chức năng mới không?</b><br/>
        Hoàn toàn được. Những đề xuất phù hợp sẽ được xem xét trong các phiên bản tiếp theo của FamilyTree.<br/>
        👉 Xem thêm: <b>Gửi góp ý</b>.
        </>,

        <>
        <b>30. Tôi cần hỗ trợ nhưng không tìm thấy câu trả lời trong FAQ thì phải làm gì?</b><br/>
        Nếu các câu hỏi trong FAQ chưa giải quyết được vấn đề của bạn, vui lòng liên hệ người cộng tác khu vực hoặc người quản trị để được hỗ trợ.
        </>,

        <>
        <b>NHÓM 6. NHỮNG VẤN ĐỀ THƯỜNG GẶP TRONG THỰC TẾ</b>
        </>,

        <>
        Các câu hỏi trong nhóm này sẽ được bổ sung trong quá trình FamilyTree được đưa vào sử dụng thực tế. Đây sẽ là nơi tổng hợp những tình huống và kinh nghiệm sử dụng mà người dùng thường gặp để giúp các thành viên khác dễ dàng tra cứu và xử lý.
        </>,

        ],

      nextTitle: "💡 Hoàn thành",

      nextText: (
        <>
          Bạn đã xem xong phần <b>Hướng dẫn & Hỗ trợ</b>. Chúc bạn sử dụng FamilyTree hiệu quả và cùng mọi người gìn giữ, lưu truyền những giá trị tốt đẹp của gia đình và dòng họ cho các thế hệ mai sau.
        </>
      )
    },
  ];

  const [selectedIndex, setSelectedIndex] = useState(0);
  const [faqSearch, setFaqSearch] = useState("");

  const selected = sections[selectedIndex];

  // ======================================================
  // Chọn mục hướng dẫn và luôn đưa màn hình về đầu trang
  // ======================================================
  const selectSection = (index) => {
      setSelectedIndex(index);

      window.scrollTo({
          top: 0,
          behavior: "smooth",
      });
  };

  const goToSection = (title) => {
      const index = sections.findIndex((s) => s.title === title);

      if (index !== -1) {
          selectSection(index);
      }
  };

  const goToPage = (path) => {
      navigate(path);

      window.scrollTo({
          top: 0,
          behavior: "smooth",
      });
  };

    return (
      <div className="min-h-screen bg-gray-50 p-4">
        {/* HEADER */}
        <div className="max-w-6xl mx-auto mb-6">
          <div className="grid grid-cols-3 items-center bg-white shadow rounded-lg p-4">
            <button
              type="button"
              onClick={() => navigate("/")}
              className="justify-self-start px-4 py-2 rounded bg-gray-700 text-white hover:bg-gray-800"
            >
              🏠 Home
            </button>

            <h1 className="justify-self-center text-2xl font-bold text-blue-700 whitespace-nowrap">
              📘 Hướng Dẫn & Hỗ Trợ
            </h1>

            <div />
          </div>
        </div>

        {/* INTRO */}
        <div className="max-w-6xl mx-auto bg-white shadow rounded-lg p-5 mb-6">
          <h2 className="text-xl font-bold text-gray-800 mb-2">
            FamilyTree Project
          </h2>
          <p className="text-gray-600 leading-relaxed">
            Trang này giúp người dùng hiểu nhanh cách sử dụng hệ thống gia phả,
            quyền truy cập, cách thêm dữ liệu và cách gửi phản hồi khi gặp lỗi.
          </p>
        </div>

        {/* GUIDE LAYOUT */}

        <div className="max-w-6xl mx-auto bg-white shadow rounded-lg overflow-hidden">

          <div className="grid grid-cols-12">

            <div className="col-span-3 border-r bg-gray-50">
            
            {/* ================= HƯỚNG DẪN ================= */}

            <div className="px-4 py-2 text-sm font-bold text-gray-500 uppercase">
              📖 Hướng dẫn
            </div>

            {sections.slice(0, 13).map((item, index) => (
              <div
                key={index}
                onClick={() => selectSection(index)}
                className={`px-4 py-3 border-b cursor-pointer ${
                  selectedIndex === index
                    ? "bg-blue-100 font-bold"
                    : "hover:bg-blue-50"
                }`}
              >
                {item.icon} {item.title}
              </div>
            ))}

            {/* ================= FAQ ================= */}

            <div className="px-4 py-2 mt-4 text-sm font-bold text-gray-500 uppercase border-t">
              ❓ FAQ
            </div>

            {sections.slice(13).map((item, idx) => {
              const index = idx + 13;

              return (
                <div
                  key={index}
                  onClick={() => selectSection(index)}
                  className={`px-4 py-3 border-b cursor-pointer ${
                    selectedIndex === index
                      ? "bg-blue-100 font-bold"
                      : "hover:bg-blue-50"
                  }`}
                >
                  {item.icon} {item.title}
                </div>
              );
            })}

            </div>

              <div className="col-span-9 p-8">

              <h2 className="text-3xl font-bold text-blue-700 mb-6">
                {selected.icon} {selected.title}
              </h2>
                {selected.title === "Câu hỏi thường gặp (FAQ)" && (
                  <div className="my-6">
                    <input
                      type="text"
                      value={faqSearch}
                      onChange={(e) => setFaqSearch(e.target.value)}
                      placeholder="🔍 Nhập từ khóa (đăng nhập, avatar, cây gia phả...)"
                      className="w-full border rounded-lg px-4 py-3 text-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                )}
              <p className="text-lg leading-9 text-gray-700 mb-8">
                {selected.desc}
              </p>

              <hr className="mb-8" />

              <h3 className="text-2xl font-bold text-red-600 mb-4">
                🎯 Mục tiêu
              </h3>

              <p className="text-lg leading-9 mb-8">
                {selected.goal}
              </p>

              <h3 className="text-2xl font-bold text-green-700 mb-4">
                {selected.learnTitle}
              </h3>

              <ul className="list-disc ml-8 text-lg leading-9 mb-8">
                {selected.learnItems.map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>

              <div className="rounded-lg bg-blue-50 border border-blue-200 p-5">
                <h3 className="text-xl font-bold text-blue-700 mb-3">
                  {selected.nextTitle}
                </h3>

                <p className="text-xl leading-9">
                  {selected.nextText}
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* FOOTER NOTE */}
        <div className="max-w-6xl mx-auto mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4 text-blue-800">
          <b>Ghi chú:</b> Nếu bạn không thấy một chức năng nào đó, có thể tài khoản
          hiện tại chưa đủ quyền hoặc phiên đăng nhập đã hết hạn.
        </div>
      </div>
    );
  }