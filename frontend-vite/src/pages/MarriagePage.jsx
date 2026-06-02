// ======================================================================
// File: MarriagePage.jsx (v11.0-Full-Optimized)
// Mô tả:
//   - 2 tab: Danh sách / Thêm - Sửa
//   - Khi bấm ✏️ từ danh sách → mở form và truyền editId
//   - Khi bấm Quay Lại → trở về danh sách
// ======================================================================

import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import MarriageList from "../components/MarriageList";
import MarriageForm from "../components/marriage/MarriageForm";

export default function MarriagePage({ role }) {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState("list");
  const [editId, setEditId] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);
  const handleEdit = (id) => {
    console.log("🟦 EDIT ID:", id);
    setEditId(id);
    setActiveTab("form");
  };

  const handleBack = () => {
    setEditId(null);
    setActiveTab("list");
    setRefreshKey((prev) => prev + 1);
  };

  return (
    <div className="w-full p-4 bg-white">
      <div className="sticky top-0 z-50 bg-white border-b py-1 mb-0">
        <div className="flex items-center justify-between gap-3">
          {/* LEFT */}
          <button
            onClick={() => navigate("/")}
            className="px-3 py-1 rounded bg-gray-700 text-white hover:bg-gray-800 whitespace-nowrap"
          >
            🏠 Home
          </button>

          {/* CENTER */}
          <h2 className="text-3xl font-bold text-yellow-600 whitespace-nowrap">
            👨‍👩 Quản Lý Quan Hệ Hôn Nhân
          </h2>

          {/* RIGHT */}
          <div className="flex gap-2">
            <button
              onClick={handleBack}
              className={`px-3 py-1 rounded whitespace-nowrap ${
                activeTab === "list"
                  ? "bg-blue-600 text-white"
                  : "bg-gray-200 text-gray-700 hover:bg-gray-300"
              }`}
            >
              📋 Danh sách
            </button>

            <button
              onClick={() => {
                setEditId(null);
                setActiveTab("form");
              }}
              className={`px-3 py-1 rounded whitespace-nowrap ${
                activeTab === "form"
                  ? "bg-blue-600 text-white"
                  : "bg-gray-200 text-gray-700 hover:bg-gray-300"
              }`}
            >
              ✏️ Thêm
            </button>
          </div>
        </div>
      </div>        
      {activeTab === "list" ? (
        <MarriageList
          key={refreshKey}
          onEdit={handleEdit}
          role={role}
        />
      ) : (
        <MarriageForm editId={editId} onBack={handleBack} />
      )}
    </div>
  );
}