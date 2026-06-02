import React from "react";
import { useNavigate } from "react-router-dom";

export default function HelpPage() {
  const navigate = useNavigate();

  const sections = [
    {
      icon: "🔐",
      title: "1. Đăng nhập / Đăng xuất",
      desc: "Người dùng đăng nhập để hệ thống nhận diện vai trò và cấp quyền phù hợp. Khi đăng xuất, hệ thống trở về quyền viewer.",
    },
    {
      icon: "🧩",
      title: "2. Tôi có thể là gì trong hệ ",
      desc: "viewer chỉ xem cơ bản. member_basic có thể thêm dữ liệu gần. member_close có quyền rộng hơn với người thân gần. co_operator hỗ trợ quản trị. admin có toàn quyền.",
    },
    {
      icon: "👤",
      title: "3. Thêm / sửa người",
      desc: "Dùng mục Thêm Người để nhập thông tin cơ bản. Một số thông tin chi tiết chỉ hiển thị hoặc cho sửa theo quyền truy cập.",
    },
    {
      icon: "👨‍👩‍👧",
      title: "4. Cách thêm cha mẹ cho một người",
      desc: "Dùng trang Quan hệ Cha Mẹ Con hoặc Thiết Lập Gia Đình để gắn con vào đúng cha mẹ. Hệ thống sẽ kiểm tra quyền trước khi lưu.",
    },
    {
      icon: "💍",
      title: "5. Thiết lập hôn nhân",
      desc: "Dùng trang Hôn Nhân để thêm hoặc cập nhật quan hệ vợ chồng. Người dùng thường chỉ được thao tác khi có quan hệ gần với một trong hai người.",
    },
    {
      icon: "🔎",
      title: "6. Tìm mối quan hệ",
      desc: "Dùng trang Tìm Quan Hệ để chọn hai người trong gia phả. Hệ thống sẽ trả về cách gọi quan hệ bằng tiếng Việt.",
    },
    {
      icon: "📢",
      title: "7. Thông báo",
      desc: "Trang thông báo hiển thị sinh nhật, ngày giỗ, kỷ niệm cưới và các thông báo nội bộ theo quyền người dùng.",
    },
    {
      icon: "💬",
      title: "8. Góp ý",
      desc: "Người dùng đã đăng nhập có thể gửi góp ý, báo lỗi hoặc đề xuất cải tiến. Admin có thể xem và xử lý trong trang quản trị.",
    },
    {
      icon: "🛡️",
      title: "9. Quyền xoá dữ liệu",
      desc: "Các thao tác xoá quan trọng như xoá hôn nhân hoặc xoá quan hệ cha mẹ con chỉ dành cho admin để tránh mất dữ liệu ngoài ý muốn.",
    },
  ];

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
            📘 Hướng Dẫn Sử Dụng
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

      {/* GUIDE CARDS */}
      <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-4">
        {sections.map((item, index) => (
          <div
            key={index}
            className="bg-white shadow rounded-lg p-5 border hover:shadow-md transition"
          >
            <div className="flex items-start gap-3">
              <div className="text-3xl">{item.icon}</div>
              <div>
                <h3 className="text-lg font-bold text-gray-800 mb-1">
                  {item.title}
                </h3>
                <p className="text-gray-600 leading-relaxed">{item.desc}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* FOOTER NOTE */}
      <div className="max-w-6xl mx-auto mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4 text-blue-800">
        <b>Ghi chú:</b> Nếu bạn không thấy một chức năng nào đó, có thể tài khoản
        hiện tại chưa đủ quyền hoặc phiên đăng nhập đã hết hạn.
      </div>
    </div>
  );
}