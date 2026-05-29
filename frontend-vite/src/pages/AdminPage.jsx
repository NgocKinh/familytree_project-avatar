import React from "react";
import { useNavigate } from "react-router-dom";

export default function AdminPage() {
  const navigate = useNavigate();

  const cards = [
    {
      icon: "📢",
      title: "Quản Lý Thông Báo",
      desc: "Tạo, sửa, xoá thông báo nội bộ.",
      path: "/admin/announcement",
      color: "bg-blue-600 hover:bg-blue-700",
    },
    {
      icon: "📨",
      title: "Quản Lý Feedback",
      desc: "Xem góp ý, báo lỗi và ghi chú xử lý.",
      path: "/admin/feedback",
      color: "bg-green-600 hover:bg-green-700",
    },
    {
      icon: "⏳",
      title: "Chờ Duyệt",
      desc: "Kiểm tra các dữ liệu đang chờ phê duyệt.",
      path: "/pending",
      color: "bg-orange-600 hover:bg-orange-700",
    },
  ];

  return (
    <div className="max-w-5xl mx-auto p-4">
      <h1 className="text-3xl font-bold text-center text-red-600 mb-8">
        ⚙️ Trang Quản Trị
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {cards.map((card) => (
          <button
            key={card.path}
            onClick={() => navigate(card.path)}
            className={`${card.color} text-white rounded-lg shadow p-5 text-left transition`}
          >
            <div className="text-4xl mb-3">{card.icon}</div>

            <div className="text-xl font-bold mb-2">
              {card.title}
            </div>

            <div className="text-sm opacity-90">
              {card.desc}
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}