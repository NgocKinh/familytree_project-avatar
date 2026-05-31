import React, { useEffect, useState } from "react";
import { getParentChildList, deleteParentChild } from "../api/parentChildApi";
import { formatName } from "../utils/formatName";

function ParentChildList({ onEdit }) {
  const [relations, setRelations] = useState([]);
  const [mode, setMode] = useState("full");
  const [showSurName, setShowSurName] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const [highlightIds, setHighlightIds] = useState([]);
  const [searchMatchIds, setSearchMatchIds] = useState([]);
  const [searchCurrentIndex, setSearchCurrentIndex] = useState(0);
  const [searchResultCount, setSearchResultCount] = useState(0);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    const data = await getParentChildList();
    console.log("🔥 PARENT_CHILD DATA:", data);
    setRelations(data);
  };
  
  const handleDelete = async (id) => {
    if (!window.confirm("Bạn có chắc muốn xóa mối quan hệ này không?")) {
      return;
    }
  
    try {
      await deleteParentChild(id);
      await loadData();
    } catch (err) {
      alert(
        err?.response?.data?.detail ||
        "Bạn không có quyền xóa quan hệ này."
      );
    }
  };
  // ✅ [CHANGE 1]: Dùng formatName chuẩn toàn project
  const renderPersonName = (person, fallbackName = "") => {
    if (person && typeof person === "object") {
      return formatName(person, {
        mode,
        showAlias: showSurName,
      });
    }

    return fallbackName || "";
  };
  const handleSearch = () => {
    const keyword = searchTerm.trim().toLowerCase();
  
    if (!keyword) return;
  
    const matches = relations.filter((r) => {
      const parentName = renderPersonName(r.parent, r.parent_name).toLowerCase();
      const childName = renderPersonName(r.child, r.child_name).toLowerCase();
  
      return (
        parentName.includes(keyword) ||
        childName.includes(keyword)
      );
    });
  
    if (matches.length === 0) {
      alert("Không tìm thấy kết quả.");
      return;
    }
  
    const ids = matches.map((r) => r.id);
  
    setSearchResultCount(matches.length);
    setSearchMatchIds(ids);
    setSearchCurrentIndex(0);
    setHighlightIds(ids);
  };
  
  const handleShowNext = () => {
    if (searchMatchIds.length === 0) return;
  
    const id = searchMatchIds[searchCurrentIndex];
  
    setHighlightIds([id]);
  
    const element = document.getElementById(`relation-${id}`);
  
    if (element) {
      const y =
        element.getBoundingClientRect().top +
        window.scrollY -
        180;
    
      window.scrollTo({
        top: y,
        behavior: "smooth",
      });
    }
  
    setSearchCurrentIndex((prev) =>
      prev + 1 >= searchMatchIds.length ? 0 : prev + 1
    );
  };
  return (
    <div className="bg-white shadow-md rounded-lg p-4">
      <h3 className="text-xl font-bold text-gray-700 mb-4">
        📋 Danh Sách Quan Hệ Cha – Con
      </h3>

      {/* Bộ điều khiển hiển thị + tìm kiếm */}
      <div className="sticky top-[48px] z-[999] bg-white border-b py-1 mb-0 flex flex-wrap items-center justify-between gap-4">
        <div className="flex flex-wrap items-center gap-4">
          <div className="flex items-center space-x-2">
            <label className="font-medium text-gray-700">🎛️ Kiểu hiển thị tên:</label>

            <select
              value={mode}
              onChange={(e) => setMode(e.target.value)}
              className="border border-gray-300 rounded p-2"
            >
              <option value="full">Đầy đủ</option>
              <option value="short">Rút gọn</option>
            </select>
          </div>

          <label className="flex items-center space-x-2 cursor-pointer">
            <input
              type="checkbox"
              checked={showSurName}
              onChange={() => setShowSurName(!showSurName)}
              className="w-4 h-4 accent-blue-600"
            />
            <span className="text-gray-700 font-medium">Hiển thị "Tên hiệu"</span>
          </label>
        </div>

        <div className="flex items-center gap-3">
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                handleSearch();
              }
            }}
            placeholder="Tìm Cha/Mẹ hoặc Con..."
            className="border rounded px-3 py-2 w-[320px]"
          />

          <button
            onClick={handleSearch}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            🔍 Tìm
          </button>

          {searchResultCount > 0 && (
            <>
              <span className="text-sm text-green-700">
                {searchResultCount} kết quả
              </span>

              <button
                onClick={handleShowNext}
                className="px-3 py-2 bg-green-600 text-white rounded hover:bg-green-700"
              >
                Hiển thị
              </button>

              <button
                onClick={() => {
                  setSearchTerm("");
                  setSearchResultCount(0);
                  setSearchMatchIds([]);
                  setHighlightIds([]);
                }}
                className="px-3 py-2 bg-gray-500 text-white rounded hover:bg-gray-600"
              >
                Thoát
              </button>
            </>
          )}
        </div>
      </div>
      {/* Bảng dữ liệu */}
      <div className="-mt-2">
      <table className="min-w-full border border-gray-300">
        <thead className="sticky top-[96px] z-40 bg-gray-100 text-gray-700">
          <tr>
            <th className="border px-4 py-2">#</th>
            <th className="border px-4 py-2">Cha/Mẹ</th>
            <th className="border px-4 py-2">Con</th>
            <th className="border px-4 py-2">Loại</th>
            <th className="border px-4 py-2">Ghi chú</th>
            <th className="border px-4 py-2 text-center">Thao tác</th>
          </tr>
        </thead>
          <tbody>
            {relations.map((r, index) => (
              <tr
                id={`relation-${r.id}`}
                key={r.id}
                className={`hover:bg-gray-50 ${
                  highlightIds.includes(r.id)
                    ? "bg-yellow-100"
                    : ""
                }`}
              >
                <td className="border px-4 py-2 text-center">{index + 1}</td>

                {/* Cột Cha/Mẹ */}
                  <td className="border px-4 py-2">
                    {renderPersonName(r.parent, r.parent_name)}
                  </td>

                  {/* Cột Con */}
                  <td className="border px-4 py-2">
                    {renderPersonName(r.child, r.child_name)}
                  </td>

                {/* Loại */}
                <td className="border px-4 py-2 text-center">
                  {r.type === "father" ? "Cha" : r.type === "mother" ? "Mẹ" : r.type}
                </td>

                {/* Ghi chú */}
                <td className="border px-4 py-2">{r.notes || ""}</td>

                {/* Nút thao tác */}
                <td className="border px-4 py-2 text-center space-x-2">
                  {/* <button
                    onClick={() => onEdit(r.id)}
                    className="bg-yellow-400 hover:bg-yellow-500 text-white px-3 py-1 rounded"
                  >
                    ✏️
                  </button> */}
                  <button
                    onClick={() => handleDelete(r.id)}
                    className="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded"
                  >
                    🗑️
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default ParentChildList;
