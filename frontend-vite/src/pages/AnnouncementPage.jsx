import React, { useEffect, useState } from "react";
import { handleAuthError } from "../utils/authErrorHandler";
import { makeApiUrl } from "../api/apiConfig";
/**
 * ==========================================================
 * 📄 AnnouncementPage.jsx (v1.2 - gồm cả sự kiện sắp tới 7 ngày)
 * ==========================================================
 */

function AnnouncementPage() {
  const [todayData, setTodayData] = useState(null);
  const [upcomingData, setUpcomingData] = useState(null);
  const [customAnnouncements, setCustomAnnouncements] = useState([]);
  const [loading, setLoading] = useState(true);

  // Gọi API cả 2
  useEffect(() => {
    const fetchData = async () => {
      try {
        const [todayRes, upcomingRes, customRes] = await Promise.all([
          fetch(makeApiUrl("/announcement/today")),
          fetch(makeApiUrl("/announcement/upcoming?days=7")),
          fetch(makeApiUrl("/announcement/list")),
        ]);
        if (
          todayRes.status === 401 ||
          upcomingRes.status === 401 ||
          customRes.status === 401
        ) {
          handleAuthError({ response: { status: 401 } });
          return;
        }
        const todayJson = await todayRes.json();
        const upcomingJson = await upcomingRes.json();
        const customJson = await customRes.json();

        setTodayData(todayJson);
        setUpcomingData(upcomingJson);
        if (Array.isArray(customJson)) {
          setCustomAnnouncements(customJson);
        } else if (customJson.success) {
          setCustomAnnouncements(customJson.data || []);
        } else {
          setCustomAnnouncements(customJson.announcements || []);
        }
      } catch (e) {
        if (handleAuthError(e)) {
          return;
        }
        console.error("❌ Lỗi tải dữ liệu:", e);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const getBgColor = (type) => {
    switch (type) {
      case "gio":
        return "bg-purple-100 border-l-4 border-purple-500";
      case "sinh_nhat":
        return "bg-pink-100 border-l-4 border-pink-500";
      case "ky_niem_cuoi":
        return "bg-yellow-100 border-l-4 border-yellow-500";
      default:
        return "bg-gray-100 border-l-4 border-gray-400";
    }
  };

  if (loading) {
    return (
      <div className="p-6 text-center text-gray-600">
        <div className="animate-spin inline-block w-6 h-6 border-4 border-blue-300 border-t-transparent rounded-full mr-2"></div>
        Đang tải thông báo...
      </div>
    );
  }

  const todayList = todayData?.announcements || [];
  const upcomingList = upcomingData?.announcements || [];

  return (
    <div className="max-w-4xl mx-auto px-6 pt-2 pb-6">
    <div className="mb-4">
      <button
        onClick={() => window.location.href = "/"}
        className="px-4 py-2 rounded-lg bg-gray-700 text-white hover:bg-gray-800"
      >
        🏠 Home
      </button>
    </div>  
      {/* Tiêu đề */}
      <h1 className="text-2xl font-bold text-center mb-1 text-blue-700 drop-shadow-sm">
        🔔 Thông Báo Tự Động
      </h1>

      <p className="text-center text-gray-600 mb-1">
      Ngày Dương: <b>{todayData?.date}</b> &nbsp; | &nbsp; Ngày Âm:{" "}
      <b>
        {todayData?.lunar} {todayData?.lunar_year_name}
      </b>
      </p>
      
      {/* --- PHẦN 1: Hôm nay --- */}
      <h2 className="text-xl font-semibold text-center text-indigo-600 mb-2">
        📅 Sự kiện trong ngày
      </h2>

      {todayList.length === 0 ? (
        <div className="text-center text-gray-500 mb-4">
          <div className="text-4xl mb-2">🌼</div>
          <p className="italic">Hôm nay không có sự kiện đặc biệt nào.</p>
        </div>
      ) : (
        <div className="space-y-3 mb-8">
          {todayList.map((item, i) => (
            <div
              key={i}
              className={`p-4 rounded-2xl shadow-sm flex items-center space-x-4 ${getBgColor(
                item.type
              )}`}
            >
              <div className="text-3xl">{item.icon}</div>
              <div>
                <p className="font-semibold">{item.title}</p>

                <p className="text-gray-500 text-sm">
                  Dương lịch: <b>{item.date}</b> | Âm lịch:{" "}
                  <b>{item.lunar} {item.lunar_year_name}</b>
                </p>

                <p className="text-xs text-gray-400 italic">
                  {item.calendar_type === "lunar" ? "Giỗ theo âm lịch" : "Giỗ theo dương lịch"}
                </p>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* --- PHẦN 2: Sắp tới --- */}
      <h2 className="text-xl font-semibold text-center text-green-600 mb-2">
        🔮 Sự kiện sắp tới (trong {upcomingData?.range_days} ngày)
      </h2>

      {upcomingList.length === 0 ? (
        <p className="text-center text-gray-400 italic">
          Không có sự kiện nào trong {upcomingData?.range_days} ngày tới.
        </p>
      ) : (
        <div className="space-y-3">
          {upcomingList.map((item, i) => (
            <div
              key={i}
              className={`p-4 rounded-2xl shadow-sm flex items-center space-x-4 ${getBgColor(
                item.type
              )}`}
            >
              <div className="text-3xl">{item.icon}</div>
              <div>
                <p className="font-semibold">{item.title}</p>

                <p className="text-gray-500 text-sm">
                  Dương lịch: <b>{item.date}</b> | Âm lịch:{" "}
                  <b>{item.lunar} {item.lunar_year_name}</b>
                </p>

                <p className="text-xs text-gray-400 italic">
                  {item.calendar_type === "lunar" ? "Giỗ theo âm lịch" : "Giỗ theo dương lịch"}
                </p>
              </div>
            </div>
          ))}
        </div>
      )}
      {/* --- PHẦN 3: Thông báo chung --- */}
      <h2 className="text-2xl font-bold text-center mb-1 text-blue-700 drop-shadow-sm">
        📢 Thông báo chung
      </h2>
      
      {customAnnouncements.length === 0 ? (
        <p className="text-center text-gray-400 italic mb-6">
          Chưa có thông báo chung nào.
        </p>
      ) : (
        <div className="space-y-3 mb-8">
          {customAnnouncements.map((item) => (
            <div
              key={item.id}
              className="p-4 rounded-2xl shadow-sm bg-blue-50 border-l-4 border-blue-500"
            >
              <p className="font-semibold text-blue-800">{item.title}</p>
              <p className="text-gray-700 mt-1 whitespace-pre-line">
                {item.description}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default AnnouncementPage;
