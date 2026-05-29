import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

function AdminFeedbackPage() {
  const navigate = useNavigate();

  const [feedbacks, setFeedbacks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedFeedback, setSelectedFeedback] = useState(null);
  const [saving, setSaving] = useState(false);

  const loadFeedbacks = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/api/feedback/list");
      const data = await res.json();

      if (data.success) {
        setFeedbacks(data.feedbacks || []);
      }
    } catch (err) {
      console.error(err);
      alert("Không tải được danh sách feedback");
    } finally {
      setLoading(false);
    }
  };

  const updateFeedback = async () => {
    if (!selectedFeedback) return;

    setSaving(true);

    try {
      const res = await fetch(
        `http://127.0.0.1:8000/api/feedback/${selectedFeedback.feedback_id}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            status: selectedFeedback.status,
            admin_note: selectedFeedback.admin_note,
          }),
        }
      );

      const data = await res.json();

      if (data.success) {
        alert("Đã cập nhật feedback.");
        setSelectedFeedback(null);
        loadFeedbacks();
      } else {
        alert("Không cập nhật được feedback.");
      }
    } catch (err) {
      console.error(err);
      alert("Lỗi khi cập nhật feedback.");
    } finally {
      setSaving(false);
    }
  };

  useEffect(() => {
    loadFeedbacks();
  }, []);

  return (
    <div className="w-full p-4 bg-white">
      {/* HEADER */}
      <div className="sticky top-0 z-50 bg-white border-b py-2 mb-4">
        <div className="grid grid-cols-3 items-center">
          <button
            onClick={() => navigate("/")}
            className="justify-self-start px-4 py-2 rounded bg-gray-700 text-white hover:bg-gray-800"
          >
            🏠 Home
          </button>

          <h2 className="justify-self-center text-2xl font-bold text-blue-600 whitespace-nowrap">
            📨 Quản Lý Feedback
          </h2>

          <div />
        </div>
      </div>

      {loading && (
        <div className="mb-3 text-blue-600">
          ⏳ Đang tải feedback...
        </div>
      )}

      {!loading && feedbacks.length === 0 && (
        <div className="p-4 rounded bg-gray-100 text-gray-700">
          Chưa có feedback nào.
        </div>
      )}

      {!loading && feedbacks.length > 0 && (
        <div className="overflow-x-auto border rounded shadow">
          <table className="min-w-full bg-white text-sm">
            <thead className="bg-gray-100">
              <tr>
                <th className="border px-3 py-2 text-left">ID</th>
                <th className="border px-3 py-2 text-left">Loại</th>
                <th className="border px-3 py-2 text-left">Tiêu đề</th>
                <th className="border px-3 py-2 text-left">Liên hệ</th>
                <th className="border px-3 py-2 text-left">Trạng thái</th>
                <th className="border px-3 py-2 text-left">Ngày gửi</th>
              </tr>
            </thead>

            <tbody>
              {feedbacks.map((fb) => (
                <tr
                  key={fb.feedback_id}
                  onClick={() => setSelectedFeedback(fb)}
                  className="hover:bg-gray-50 cursor-pointer"
                >
                  <td className="border px-3 py-2">{fb.feedback_id}</td>
                  <td className="border px-3 py-2">{fb.category}</td>
                  <td className="border px-3 py-2 font-semibold">{fb.title}</td>

                  <td className="border px-3 py-2">
                    <div>{fb.contact_email || "-"}</div>
                    <div>{fb.contact_phone || "-"}</div>
                  </td>

                  <td className="border px-3 py-2">
                    <span className="px-2 py-1 rounded bg-yellow-100 text-yellow-700">
                      {fb.status}
                    </span>
                  </td>

                  <td className="border px-3 py-2">{fb.created_at}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {selectedFeedback && (
        <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
          <div className="bg-white rounded shadow-lg w-full max-w-2xl p-6">
            <h3 className="text-xl font-bold text-blue-600 mb-4">
              📨 Feedback #{selectedFeedback.feedback_id}
            </h3>

            <div className="space-y-3">
              <div>
                <strong>Loại:</strong> {selectedFeedback.category}
              </div>

              <div>
                <strong>Tiêu đề:</strong> {selectedFeedback.title}
              </div>

              <div>
                <strong>Nội dung:</strong>
                <div className="mt-1 p-3 bg-gray-100 rounded whitespace-pre-wrap">
                  {selectedFeedback.message}
                </div>
              </div>

              <div>
                <strong>Liên hệ:</strong>
                <div>Email: {selectedFeedback.contact_email || "-"}</div>
                <div>Phone: {selectedFeedback.contact_phone || "-"}</div>
              </div>

              <div>
                <label className="block font-semibold mb-1">
                  Trạng thái
                </label>

                <select
                  value={selectedFeedback.status}
                  onChange={(e) =>
                    setSelectedFeedback((prev) => ({
                      ...prev,
                      status: e.target.value,
                    }))
                  }
                  className="w-full border rounded p-2"
                >
                  <option value="new">new</option>
                  <option value="reviewing">reviewing</option>
                  <option value="resolved">resolved</option>
                  <option value="rejected">rejected</option>
                </select>
              </div>

              <div>
                <label className="block font-semibold mb-1">
                  Ghi chú nội bộ
                </label>

                <textarea
                  rows="4"
                  value={selectedFeedback.admin_note || ""}
                  onChange={(e) =>
                    setSelectedFeedback((prev) => ({
                      ...prev,
                      admin_note: e.target.value,
                    }))
                  }
                  className="w-full border rounded p-2"
                />
              </div>
            </div>

            <div className="flex justify-end gap-3 mt-6">
              <button
                onClick={() => setSelectedFeedback(null)}
                className="px-4 py-2 rounded bg-gray-300 hover:bg-gray-400"
              >
                Đóng
              </button>

              <button
                onClick={updateFeedback}
                disabled={saving}
                className="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700 disabled:bg-gray-400"
              >
                {saving ? "Đang lưu..." : "Lưu"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default AdminFeedbackPage;
