import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { handleAuthError } from "../utils/authErrorHandler";
function FeedbackPage() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    category: "bug",
    title: "",
    message: "",
    contact_email: "",
    contact_phone: "",
  });

  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    // ======================================================
    // VALIDATION: Tiêu đề
    // ======================================================
    if (!form.title.trim()) {
    alert("Vui lòng nhập tiêu đề phản hồi.");
    setLoading(false);
    return;
    }

    // ======================================================
    // VALIDATION: Nội dung
    // ======================================================
    if (!form.message.trim()) {
    alert("Vui lòng nhập nội dung phản hồi.");
    setLoading(false);
    return;
    }

    // ======================================================
    // VALIDATION: Email hoặc Số điện thoại
    // ======================================================
    if (
    !form.contact_email.trim() &&
    !form.contact_phone.trim()
    ) {
    alert("Vui lòng nhập Email hoặc Số điện thoại để ban quản trị có thể phản hồi.");
    setLoading(false);
    return;
    }
  
    try {
      const res = await fetch(
        "http://127.0.0.1:8000/api/feedback/create",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(form),
        }
      );
      if (res.status === 401) {
        handleAuthError({ response: { status: 401 } });
        return;
      }
      const data = await res.json();

      if (data.success) {
        setSuccess(true);

        setForm({
          category: "bug",
          title: "",
          message: "",
          contact_email: "",
          contact_phone: "",
        });
      }
    } catch (err) {
      console.error(err);
      alert("Không gửi được góp ý");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto">

      {/* HEADER */}
      <div className="flex justify-between items-center mb-6">
        <button
          onClick={() => navigate("/")}
          className="px-4 py-2 rounded bg-gray-700 text-white hover:bg-gray-800"
        >
          🏠 Home
        </button>

        <h1 className="text-2xl font-bold text-blue-600">
          📝 Góp Ý & Hỗ Trợ
        </h1>

        <div />
      </div>

      {success && (
        <div className="mb-4 p-3 rounded bg-green-100 text-green-700">
          ✅ Cảm ơn bạn đã gửi góp ý.
          Ban quản trị sẽ xem xét và phản hồi nếu cần.
        </div>
      )}

        <form
        noValidate
        onSubmit={handleSubmit}
        className="space-y-4 bg-white p-4 rounded shadow"
        >
        {/* CATEGORY */}
        <div>
          <label className="block mb-1 font-semibold">
            Loại phản hồi
          </label>

          <select
            value={form.category}
            onChange={(e) =>
              setForm({
                ...form,
                category: e.target.value,
              })
            }
            className="w-full border rounded p-2"
          >
            <option value="bug">Báo lỗi</option>
            <option value="feature">Đề xuất tính năng</option>
            <option value="data">Sai dữ liệu gia phả</option>
            <option value="account">Hỗ trợ tài khoản</option>
            <option value="other">Khác</option>
          </select>
        </div>

        {/* TITLE */}
        <div>
          <label className="block mb-1 font-semibold">
            Tiêu đề
          </label>

          <input
            type="text"
            value={form.title}
            onChange={(e) =>
              setForm({
                ...form,
                title: e.target.value,
              })
            }
            className="w-full border rounded p-2"
          />
        </div>

        {/* MESSAGE */}
        <div>
          <label className="block mb-1 font-semibold">
            Nội dung
          </label>

          <textarea
            rows="6"
            value={form.message}
            onChange={(e) =>
              setForm({
                ...form,
                message: e.target.value,
              })
            }
            className="w-full border rounded p-2"
          />
        </div>

        {/* EMAIL */}
        <div>
          <label className="block mb-1 font-semibold">
            Email liên hệ
          </label>

          <input
            type="email"
            value={form.contact_email}
            onChange={(e) =>
              setForm({
                ...form,
                contact_email: e.target.value,
              })
            }
            className="w-full border rounded p-2"
          />
        </div>

        {/* PHONE */}
        <div>
          <label className="block mb-1 font-semibold">
            Số điện thoại
          </label>

          <input
            type="text"
            value={form.contact_phone}
            onChange={(e) =>
              setForm({
                ...form,
                contact_phone: e.target.value,
              })
            }
            className="w-full border rounded p-2"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className={`px-6 py-2 rounded text-white ${
            loading
              ? "bg-blue-300 cursor-not-allowed"
              : "bg-blue-600 hover:bg-blue-700"
          }`}
        >
          {loading ? "⏳ Đang gửi..." : "Gửi phản hồi"}
        </button>

      </form>
    </div>
  );
}

export default FeedbackPage;