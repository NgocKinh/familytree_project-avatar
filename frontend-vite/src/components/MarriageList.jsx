// ======================================================================
// File: MarriageList.jsx (v11.0-Optimized)
// Mô tả:
//   - Hiển thị danh sách hôn nhân
//   - Full / Short Name + SurName
//   - Nhấn ✏️ truyền id sang MarriagePage → MarriageForm
// ======================================================================

import React, { useEffect, useState } from "react";
import axios from "axios";
import { API_BASE_URL } from "../api/apiConfig";
import { formatDateVN } from "../utils/formatDate";
import { formatName } from "../utils/formatName";
const getAuthConfig = () => ({
  headers: {
    Authorization: `Bearer ${localStorage.getItem("token")}`,
  },
});
export default function MarriageList({ onEdit, role }) {
  const savePriority = async (marriageId, priority) => {
    try {
      await axios.put(
        `${API_BASE_URL}/marriage/${marriageId}/priority`,
        {
          priority,
        },
        getAuthConfig()
      );
  
      console.log("✅ Priority saved");
    } catch (err) {
      console.error("❌ Save priority failed", err);
    }
  };
  const [marriages, setMarriages] = useState([]);
  const [mode, setMode] = useState("full");
  const [showSurName, setShowSurName] = useState(false);
  const [deleteConfirmId, setDeleteConfirmId] = useState(null);
  const [message, setMessage] = useState("");
  const [searchText, setSearchText] = useState("");
  const [activeSearch, setActiveSearch] = useState("");

  // ================================================================
  // LOAD
  // ================================================================
  const fetchMarriages = async () => {
    try {
      const res = await axios.get(
        `${API_BASE_URL}/marriage`
      );
      setMarriages(res.data || []);
    } catch (err) {
      setMessage("❌ Không tải được danh sách hôn nhân!");
    }
  };

  useEffect(() => {
    fetchMarriages();
  }, []);

  // ================================================================
  // ✅ [CHANGE 1]: Hiển thị tên bằng formatName chuẩn
  // - Không tự tách chuỗi spouse_a_name / spouse_b_name nữa
  // - Nếu backend chưa trả spouse_a/spouse_b thì chỉ dùng tên cũ để hiển thị tạm
  // ================================================================
  const renderPersonName = (person, fallbackName = "") => {
    // ✅ Nếu có object chuẩn → dùng formatName
    if (person && typeof person === "object") {
      return formatName(person, {
        mode,
        showAlias: showSurName,
      });
    }
    // ✅ Nếu chưa có object (backend cũ) → dùng fallback string
    if (fallbackName) return fallbackName;

    return "";
  };

  // ================================================================
  // Xóa quan hệ
  // ================================================================
  const handleDelete = async (id) => {
    try {
      await axios.delete(
        `${API_BASE_URL}/marriage/${id}`,
        getAuthConfig()
      );
      await fetchMarriages(); // 🔥 THÊM DÒNG NÀY
      setMessage("🗑️ Đã xóa quan hệ hôn nhân!");
      setDeleteConfirmId(null);
      
    } catch (err) {
      const detail =
        err?.response?.data?.detail ||
        "Không thể kết nối đến máy chủ.";

      setMessage(`❌ ${detail}`);
    }
  };

  // ================================================================
  // SEARCH / FILTER
  // ================================================================
  const normalizedSearch = activeSearch.trim().toLowerCase();
  
  const filteredMarriages = marriages.filter((m) => {
    if (!normalizedSearch) return true;
  
    const text = [
      renderPersonName(m.spouse_a, m.spouse_a_name),
      renderPersonName(m.spouse_b, m.spouse_b_name),
      formatDateVN(m.start_date),
      formatDateVN(m.end_date),
      m.status,
      m.priority,
    ]
      .join(" ")
      .toLowerCase();
  
    return text.includes(normalizedSearch);
  });
  
  // ================================================================
  // UI
  // ================================================================
  return (
    <div className="bg-white p-0">
      <div className="bg-white border rounded-xl shadow-sm px-1 py-1">
        <div className="flex flex-wrap justify-center items-center gap-3">
          <input
            type="text"
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") setActiveSearch(searchText);
            }}
            placeholder="Nhập tên, ngày, trạng thái..."
            className="w-72 rounded-lg bg-gray-50 px-4 py-3 border border-gray-300 focus:border-blue-500 focus:outline-none"
          />
  
          <button
            onClick={() => setActiveSearch(searchText)}
            className="px-5 py-3 rounded-lg bg-blue-600 text-white hover:bg-blue-700 shadow-sm"
          >
            🔍 Tìm kiếm
          </button>
  
          {activeSearch && (
            <button
              onClick={() => {
                setSearchText("");
                setActiveSearch("");
              }}
              className="px-5 py-3 rounded-lg bg-yellow-500 text-white hover:bg-yellow-600 shadow-sm"
            >
              🚪 Thoát
            </button>
          )}
  
          <div className="flex items-center gap-2">
            <span className="text-gray-700 font-medium">Kiểu hiển thị tên:</span>
            <select
              value={mode}
              onChange={(e) => setMode(e.target.value)}
              className="border px-3 py-2 rounded"
            >
              <option value="full">Đầy đủ</option>
              <option value="short">Rút gọn</option>
            </select>
          </div>
  
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={showSurName}
              onChange={() => setShowSurName(!showSurName)}
              className="w-4 h-4 accent-blue-600"
            />
            <span className="font-medium text-gray-700">Tên hiệu</span>
          </label>
        </div>
  
        {activeSearch && (
          <p className="text-center text-sm text-gray-600 mt-2">
            Tìm thấy {filteredMarriages.length} kết quả cho:{" "}
            <span className="font-semibold text-blue-600">{activeSearch}</span>
          </p>
        )}
      </div>
  
      {message && (
        <div
          className={`fixed top-20 left-1/2 z-[9999] w-[90%] max-w-4xl -translate-x-1/2 rounded border px-4 py-3 text-center font-semibold shadow-lg ${
            message.startsWith("🗑️")
              ? "border-green-300 bg-green-50 text-green-700"
              : "border-red-300 bg-red-50 text-red-700"
          }`}
        >
          {message}
        </div>
      )}
  
        <div className="overflow-x-auto">
          <table className="min-w-full border text-sm text-center">
            <thead className="bg-blue-50 sticky top-[0px] z-30">
              <tr>
                <th className="border p-2">#</th>
                <th className="border p-2">Người thứ nhất</th>
                <th className="border p-2">Người thứ hai</th>
                <th className="border p-2">Ngày bắt đầu</th>
                <th className="border p-2">Ngày kết thúc</th>
                <th className="border p-2">Trạng thái</th>
                <th className="border p-2">Ưu tiên</th>
                <th className="border p-2">Thao tác</th>
              </tr>
            </thead>
  
            <tbody>
              {filteredMarriages.length === 0 ? (
                <tr>
                  <td colSpan="8" className="p-4 text-gray-500">
                    Không có dữ liệu
                  </td>
                </tr>
              ) : (
                filteredMarriages.map((m, idx) => (
                  <tr key={m.id} className="hover:bg-gray-50">
                    <td className="border p-2">{idx + 1}</td>
  
                    <td className="border p-2">
                      {renderPersonName(m.spouse_a, m.spouse_a_name)}
                    </td>
  
                    <td className="border p-2">
                      {renderPersonName(m.spouse_b, m.spouse_b_name)}
                    </td>
  
                    <td className="border p-2">{formatDateVN(m.start_date)}</td>
                    <td className="border p-2">{formatDateVN(m.end_date)}</td>
                    <td className="border p-2 capitalize">{m.status}</td>
  
                    <td className="border p-2">
                      <input
                        type="number"
                        value={m.priority ?? 0}
                        onChange={(e) => {
                          m.priority = Number(e.target.value);
                          setMarriages([...marriages]);
                        }}
                        onBlur={() => savePriority(m.id, m.priority)}
                        className="w-16 border rounded px-2 py-1 text-center"
                      />
                    </td>
  
                    <td className="border p-2">
                      {deleteConfirmId === m.id ? (
                        <div className="text-red-600 font-medium">
                          Xác nhận xóa?
                          <div className="flex justify-center gap-2 mt-1">
                            <button
                              onClick={() => handleDelete(m.id)}
                              className="bg-red-500 text-white px-2 py-1 rounded hover:bg-red-600"
                            >
                              Xóa
                            </button>
                            <button
                              onClick={() => setDeleteConfirmId(null)}
                              className="bg-gray-300 px-2 py-1 rounded hover:bg-gray-400"
                            >
                              Hủy
                            </button>
                          </div>
                        </div>
                      ) : (
                        <div className="flex justify-center gap-2">
                          <button
                            onClick={() => onEdit(m.id)}
                            className="bg-yellow-400 text-white px-2 py-1 rounded hover:bg-yellow-500"
                          >
                            ✏️
                          </button>
  
                          {role === "admin" && (
                            <button
                              onClick={() => setDeleteConfirmId(m.id)}
                              className="bg-red-500 text-white px-2 py-1 rounded hover:bg-red-600"
                            >
                              🗑️
                            </button>
                          )}
                        </div>
                      )}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
    </div>
  );
}
