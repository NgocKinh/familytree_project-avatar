import React, { useEffect, useState } from "react";
import { handleAuthError } from "../utils/authErrorHandler";
function InternalNotificationPage() {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchNotifications = async () => {
    try {
      const res = await fetch("http://localhost:8000/api/admin/announcement/list");
      if (res.status === 401) {
        handleAuthError({ response: { status: 401 } });
        return;
      }
      const json = await res.json();

      if (json.success) {
        const activeItems = (json.data || []).filter((item) => item.is_active);
        setNotifications(activeItems);
      }
    } catch (err) {
      if (handleAuthError(err)) {
        return;
      }
      console.error("❌ Lỗi tải thông báo nội bộ:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchNotifications();
  }, []);

  return (
    <div className="max-w-4xl mx-auto px-6 pt-2 pb-6">
      <div className="mb-4">
        <button
          onClick={() => (window.location.href = "/")}
          className="px-4 py-2 rounded-lg bg-gray-700 text-white hover:bg-gray-800"
        >
          🏠 Home
        </button>
      </div>

      <h1 className="text-2xl font-bold text-center mb-2 text-blue-700">
        📢 Thông Báo Nội Bộ
      </h1>

      <p className="text-center text-gray-500 mb-4">
        Dành cho thành viên trong gia phả
      </p>

      {loading ? (
        <div className="text-center text-gray-500">
          Đang tải thông báo nội bộ...
        </div>
      ) : notifications.length === 0 ? (
        <div className="text-center text-gray-500 italic">
          Hiện chưa có thông báo nội bộ nào.
        </div>
      ) : (
        <div className="space-y-3">
          {notifications.map((item) => (
            <div
              key={item.id}
              className="p-4 rounded-2xl shadow-sm bg-blue-100 border-l-4 border-blue-500"
            >
              <p className="font-semibold text-blue-800">
                📣 {item.title}
              </p>

              <p className="text-gray-700 text-sm mt-1">
                {item.description}
              </p>

              <p className="text-xs text-gray-400 italic mt-2">
                Thông báo nội bộ
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default InternalNotificationPage;