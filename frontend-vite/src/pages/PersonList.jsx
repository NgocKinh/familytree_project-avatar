// ======================================================
// File: src/pages/PersonList.jsx (v7.0-AvatarEngine)
// Mô tả:
//   - Thay avatar logic bằng avatarEngine.js
//   - Không đổi bất kỳ logic nào khác
//   - Giữ nguyên filter/tab/delete/sort
// ======================================================

import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getAvatarURL, handleAvatarError } from "../utils/avatarEngine";
import {
  getAllPersons,
  softDeletePerson,
  restorePerson,
  hardDeletePerson,
} 
from "../api/personApi";
import { formatGender } from "../utils/formatGender";
import { formatDateVN } from "../utils/formatDate";
import { formatName } from "../utils/formatName";

export default function PersonList({ role }) {
  const [persons, setPersons] = useState([]);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState("active"); 
  const navigate = useNavigate();
  // ✅ [CHANGE 1]: Chuẩn hóa ID vì backend có lúc trả id, có lúc trả person_id
  const getPersonId = (person) => person?.person_id ?? person?.id;
  // 🔵 [ADDED]: Quyền xem ID
  const canViewId =
    role === "co_operator" || role === "admin";
  // ======================================================
  // LOAD DATA
  // ======================================================
  useEffect(() => {
    fetchPersons();
  }, []);

  const fetchPersons = async () => {
    try {
      setLoading(true);
      const data = await getAllPersons();
      setPersons(data.persons || data.data || data || []);  
    } catch (err) {
      console.error("❌ Lỗi tải danh sách:", err?.response?.data || err.message);
    } finally {
      setLoading(false);
    }
  };

  // ======================================================
  // ACTIONS
  // ======================================================
  const handleEdit = (id) =>
    navigate(`/person/basic/${id}`, {
      state: {
        onAvatarUpdated: fetchPersons, // 🔵 callback chuẩn
      },
    });
  const handleViewTree = (id) => navigate(`/tree/${id}`);

  const handleSoftDelete = async (id) => {

    if (!window.confirm("Bạn có chắc muốn Ẩn tạm người này?")) {
      return;
    }
  
    try {
  
      await softDeletePerson(id);
  
      alert("Đã tạm ẩn thành công");
  
      fetchPersons();
  
    } catch (err) {
  
      const detail = err?.response?.data?.detail;
  
      alert(
        detail.message + "\n\n" +
        detail.details.join("\n")
      );
    }
  };

  const handleRestore = async (id) => {
    if (!window.confirm("Phục hồi người này?")) return;
    await restorePerson(id);
    fetchPersons();
  };

  const handleHardDelete = async (id) => {
    if (!window.confirm("⚠️ Xóa vĩnh viễn? Không thể hoàn tác!")) return;
    await hardDeletePerson(id);
    fetchPersons();
  };

  // ======================================================
  // FILTER THEO TAB
  // ======================================================
  const filteredPersons =
    activeTab === "active"
      ? persons.filter((p) => (p.delete_status ?? 0) === 0)
      : persons.filter((p) => (p.delete_status ?? 0) === 1);

  const sortedPersons = [...filteredPersons].sort((a, b) => {
    const ay = a.birth_date ? Number(String(a.birth_date).slice(0, 4)) : 0;
    const by = b.birth_date ? Number(String(b.birth_date).slice(0, 4)) : 0;
  
    // Không có năm sinh lên trước
    if (!ay && by) return -1;
    if (ay && !by) return 1;
  
    // Có năm sinh: tăng dần
    if (ay !== by) return ay - by;
  
    // Nếu cùng năm sinh: sắp xếp ABC theo tên chuẩn
    return formatName(a).localeCompare(formatName(b), "vi");
  });

  // ======================================================
  // RENDER
  // ======================================================
  return (
    <div className="p-4">
      {loading && <div className="mb-2 text-blue-500">⏳ Đang tải dữ liệu...</div>}
      {/* TAB */}
      <div className="flex gap-4 mb-4">
        <button
          className={`px-4 py-2 rounded-lg ${
            activeTab === "active"
              ? "bg-blue-600 text-white"
              : "bg-gray-200 hover:bg-gray-300"
          }`}
          onClick={() => setActiveTab("active")}
        >
          🟢 Hoạt động
        </button>

        <button
          className={`px-4 py-2 rounded-lg ${
            activeTab === "hidden"
              ? "bg-yellow-600 text-white"
              : "bg-gray-200 hover:bg-gray-300"
          }`}
          onClick={() => setActiveTab("hidden")}
        >
          🟡 Đã Ẩn Tạm
        </button>
      </div>
      
      {/* TABLE */}
      <table className="min-w-full border border-gray-300">
        <thead className="bg-gray-100">
          <tr>
            <th className="px-4 py-2">Ảnh</th>
            {canViewId && (
              <th className="px-4 py-2">ID</th>
            )}
            <th className="px-4 py-2">Họ tên</th>
            <th className="px-4 py-2">Giới tính</th>
            <th className="px-4 py-2">Sinh–Mất</th>
            <th className="px-4 py-2 text-center">Hành động</th>
          </tr>
        </thead>

        <tbody>
          {loading ? (
            <tr>
              <td colSpan="5" className="py-4 text-center text-blue-500">
                ⏳ Đang tải...
              </td>
            </tr>
          ) : sortedPersons.length === 0 ? (
            <tr>
              <td colSpan="5" className="py-4 text-center italic text-gray-500">
                Không có dữ liệu
              </td>
            </tr>
          ) : (
            sortedPersons.map((p) => (
              <tr key={getPersonId(p)} className="border-t hover:bg-gray-50">
                <td className="px-4 py-2 text-center">
                  <img
                    src={getAvatarURL({
                      id: getPersonId(p),
                      gender: p.gender,
                    })}
                    onError={(e) => handleAvatarError(e, p.gender)}
                    className="w-10 h-10 rounded-full object-cover"
                  />
                </td>
                {canViewId && (
                  <td className="px-4 py-2 text-center font-mono">
                    {getPersonId(p)}
                  </td>
                )}
                <td className="px-4 py-2">
                  {formatName(p, { mode: "full", showAlias: true })}
                </td>

                <td className="px-4 py-2">{formatGender(p.gender)}</td>

                <td className="px-4 py-2 text-center">
                  {p.birth_date?.slice(0, 4) || "?"}
                  {" - "}
                  {p.death_date?.slice(0, 4) || "?"}
                </td>

                <td className="px-4 py-2 text-center space-x-2">
                  <button
                    onClick={() => handleViewTree(getPersonId(p))}
                    className="bg-green-500 hover:bg-green-600 text-white px-2 py-1 rounded"
                  >
                    🌳
                  </button>

                  {role !== "viewer" && (
                    <button
                      onClick={() => navigate(`/person/basic/${getPersonId(p)}`)}
                      className="bg-yellow-500 hover:bg-yellow-600 text-white px-2 py-1 rounded"
                    >
                      ✏️
                    </button>
                  )}

                  {activeTab === "active" &&
                    (role === "co_operator" || role === "admin") && (
                      <button
                        onClick={() => handleSoftDelete(getPersonId(p))}
                        className="bg-yellow-600 hover:bg-yellow-700 text-white px-2 py-1 rounded"
                      >
                        👻 Ẩn
                      </button>
                    )}

                  {activeTab === "hidden" &&
                    (role === "co_operator" || role === "admin") && (
                      <button
                        onClick={() => handleRestore(getPersonId(p))}
                        className="bg-green-600 hover:bg-green-700 text-white px-2 py-1 rounded"
                      >
                        ♻️ Phục hồi
                      </button>
                    )}

                  {activeTab === "hidden" && role === "admin" && (
                    <button
                      onClick={() => handleHardDelete(getPersonId(p))}
                      className="bg-red-600 hover:bg-red-700 text-white px-2 py-1 rounded"
                    >
                      🔥 Xóa
                    </button>
                  )}
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}
