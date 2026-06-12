import React, { useEffect, useState } from "react";
import AdminHeader from "../components/admin/AdminHeader";
import { handleAuthError } from "../utils/authErrorHandler";
function AnnouncementAdminPage() {
    const [announcements, setAnnouncements] = useState([]);
    const [loading, setLoading] = useState(true);
    const [title, setTitle] = useState("");
    const [description, setDescription] = useState("");
    const fetchAnnouncements = async () => {
        try {
            const token = localStorage.getItem("token");

            const res = await fetch("http://localhost:8000/api/admin/announcement/list", {
            headers: {
                Authorization: `Bearer ${token}`,
            },
            });
          
            if (res.status === 401) {
              handleAuthError({ response: { status: 401 } });
              return;
            }
          
            const json = await res.json();
          
            if (json.success) {
              setAnnouncements(json.data || []);
            }
          } catch (err) {
            if (handleAuthError(err)) {
              return;
            }
          
            console.error("❌ Lỗi tải announcements:", err);
          } finally {
            setLoading(false);
          }
    };

    useEffect(() => {
        fetchAnnouncements();
    }, []);
    const handleCreate = async () => {
        try {
          const token = localStorage.getItem("token");
      
          const res = await fetch(
            "http://localhost:8000/api/admin/announcement/create",
            {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
              },
              body: JSON.stringify({
                title,
                description,
                event_type: "custom",
                calendar_type: "solar",
                solar_date: null,
                lunar_day: null,
                lunar_month: null,
                lunar_year: null,
                repeat_type: "none",
                person_id: null,
                is_active: true,
              }),
            }
          );
      
          if (res.status === 401) {
            handleAuthError({ response: { status: 401 } });
            return;
          }
      
          const json = await res.json();
      
          if (json.success) {
            setTitle("");
            setDescription("");
      
            fetchAnnouncements();
          }
        } catch (err) {
          if (handleAuthError(err)) {
            return;
          }
      
          console.error("❌ Create failed:", err);
        }
      };

    return (
        <div className="max-w-5xl mx-auto p-6">
            
            <AdminHeader title="📢 Quản Lý Thông Báo" />

            <div className="bg-white rounded-xl shadow p-6 border">
                <div className="mb-6 border rounded-xl p-4 bg-blue-50">
                    <h2 className="text-xl font-bold text-blue-700 mb-4">
                        ➕ Tạo thông báo mới
                    </h2>

                    <input
                        type="text"
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                        placeholder="Tiêu đề thông báo"
                        className="w-full border rounded-lg px-3 py-2 mb-3"
                    />

                    <textarea
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                        placeholder="Nội dung thông báo"
                        className="w-full border rounded-lg px-3 py-2 mb-3"
                        rows={3}
                    />

                    <button
                        onClick={handleCreate}
                        className="px-4 py-2 rounded-lg bg-blue-600 text-white hover:bg-blue-700"
                    >
                        Lưu thông báo
                    </button>
                </div>
                {loading ? (
                    <p className="text-gray-500">Đang tải thông báo...</p>
                ) : announcements.length === 0 ? (
                    <p className="text-gray-500 italic">Chưa có thông báo nào.</p>
                ) : (
                    <div className="space-y-3">
                        {announcements.map((item) => (
                            <div
                                key={item.id}
                                className="border rounded-lg p-4 bg-gray-50"
                            >
                                <h2 className="font-bold text-lg text-gray-800">
                                    {item.title}
                                </h2>

                                <p className="text-gray-600 mt-1">
                                    {item.description}
                                </p>

                                <p className="text-xs text-gray-400 mt-2">
                                    Type: {item.event_type} | Active: {item.is_active ? "Yes" : "No"}
                                </p>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}

export default AnnouncementAdminPage;