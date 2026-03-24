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
} from "../api/personApi";

import { formatGender } from "../utils/formatGender";
import { formatDateVN } from "../utils/formatDate";
import { formatName } from "../utils/formatName";


export default function PersonList({ role }) {
  console.log("🚨 THIS IS THE FRONTEND I AM EDITING 🚨");
  const [persons, setPersons] = useState([]);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState("active"); 
  const navigate = useNavigate();

  // ======================================================
  // LOAD DATA
  // ======================================================
  useEffect(() => {
    console.log("🔥 PersonList mounted");
    fetchPersons();
  }, []);

  const fetchPersons = async () => {
    try {
      setLoading(true);
      console.log("🚀 CALL API...");
      const data = await getAllPersons();
      console.log("🔥 DATA:", data);
      setPersons(data.persons || data.data || data || []);  
    } catch (err) {
      console.error("❌ Lỗi tải danh sách:", err);
      console.error("❌ RESPONSE:", err?.response);
      console.error("❌ DATA:", err?.response?.data);
    } finally {
      setLoading(false);
    }
  };

  // ======================================================
  // ACTIONS
  // ======================================================
  const handleEdit = (id) => navigate(`/person/basic/${id}`);
  const handleViewTree = (id) => navigate(`/tree/${id}`);

  const handleSoftDelete = async (id) => {
    if (!window.confirm("Bạn có chắc muốn Ẩn tạm người này?")) return;
    await softDeletePerson(id);
    fetchPersons();
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

  const sortedPersons = filteredPersons;

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
            <th className="px-4 py-2">Họ tên</th>
            <th className="px-4 py-2">Giới tính</th>
            <th className="px-4 py-2">Ngày sinh</th>
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
              <tr key={p.person_id} className="border-t hover:bg-gray-50">
                <td className="px-4 py-2 text-center">
                  <img
                    src={getAvatarURL(p)}
                    onError={(e) => handleAvatarError(e, p.gender)}
                    className="w-10 h-10 rounded-full object-cover"
                  />
                </td>

                <td className="px-4 py-2">{formatName(p)}</td>
                <td className="px-4 py-2">{formatGender(p.gender)}</td>
                <td className="px-4 py-2">{formatDateVN(p.birth_date)}</td>

                <td className="px-4 py-2 text-center space-x-2">
                  <button
                    onClick={() => handleViewTree(p.person_id)}
                    className="bg-green-500 hover:bg-green-600 text-white px-2 py-1 rounded"
                  >
                    🌳
                  </button>

                  {role !== "viewer" && (
                    <button
                      onClick={() => handleEdit(p.person_id)}
                      className="bg-yellow-500 hover:bg-yellow-600 text-white px-2 py-1 rounded"
                    >
                      ✏️
                    </button>
                  )}

                  {activeTab === "active" &&
                    (role === "co_operator" || role === "admin") && (
                      <button
                        onClick={() => handleSoftDelete(p.person_id)}
                        className="bg-yellow-600 hover:bg-yellow-700 text-white px-2 py-1 rounded"
                      >
                        👻 Ẩn
                      </button>
                    )}

                  {activeTab === "hidden" &&
                    (role === "co_operator" || role === "admin") && (
                      <button
                        onClick={() => handleRestore(p.person_id)}
                        className="bg-green-600 hover:bg-green-700 text-white px-2 py-1 rounded"
                      >
                        ♻️ Phục hồi
                      </button>
                    )}

                  {activeTab === "hidden" && role === "admin" && (
                    <button
                      onClick={() => handleHardDelete(p.person_id)}
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
