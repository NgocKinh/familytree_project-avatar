// ======================================================================
// File: src/pages/AddPersonPage.jsx (v6.5-FINAL-FixDetailRender)
// Mô tả cập nhật v6.5:
//   - Đồng bộ hoàn toàn với PersonBasicForm v7.6
//   - Đảm bảo Form Detail xuất hiện khi EDIT và CREATE
//   - Sửa lỗi callback không nhận được ID từ FormBasic
//   - Giữ nguyên logic phân quyền
// ======================================================================

import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import PersonBasicForm from "../components/person/PersonBasicForm";
import PersonDetailForm from "../components/person/PersonDetailForm";

export default function AddPersonPage({ role }) {
  const { id } = useParams();
  const navigate = useNavigate();
  const isEditMode = Boolean(id);

  // ==============================================
  // QUẢN LÝ ID VÀ TRẠNG THÁI FORM DETAIL
  // ==============================================
  const [personId, setPersonId] = useState(id || null);
  const [showDetailForm, setShowDetailForm] = useState(false);
  const [hasNavigated, setHasNavigated] = useState(false);
  // Ai được phép xem Form Chi Tiết?
  const canShowDetail =
    role === "member_close" ||
    role === "co_operator" ||
    role === "admin";

  // ======================================================================
  // Khi mở trang ở chế độ EDIT → tự động hiển thị Form Detail
  // ======================================================================
  useEffect(() => {
    if (isEditMode && canShowDetail) {
      setPersonId(id);
      setShowDetailForm(true);
    }
  
    if (!isEditMode) {
      setPersonId(null);
      setShowDetailForm(false);
    }
  
    // 🔵 reset guard khi vào trang mới
    setHasNavigated(false);
  }, [isEditMode, id, canShowDetail]);

  // ======================================================================
  // Callback từ PersonBasicForm (khi lưu xong)
  // ======================================================================
  const handleSavedBasic = (result) => {
    // Backend có thể trả id hoặc person_id → chuẩn hoá
    // ----------------------------------------------------------
    // result = { id: 10, ... } hoặc { person_id: 10, ... }
    // ----------------------------------------------------------

    const savedId =
      result?.id ||
      result?.person_id ||
      id; // fallback khi đang edit

    // Guard: không có ID thì dừng
    if (!savedId) {
      console.warn("❌ Không lấy được ID sau khi lưu");
      return;
    }
    // Lưu ID vào state
    setPersonId(savedId);

    // ==================================================================
    // Quy tắc hiển thị Form Detail:
    // - member_close trở lên → luôn hiển thị
    // - member_basic → không hiển thị
    // ==================================================================
    if (canShowDetail) {
      setShowDetailForm(true);
    }
    
    // ✅ Guard navigate tránh chạy nhiều lần
    if (!hasNavigated) {
      setHasNavigated(true);
    
      if (isEditMode) {
        navigate("/person-list");
      } else {
        navigate("/");
      }
    }
  };  
  // ======================================================================
  // GIAO DIỆN CHÍNH
  // ======================================================================
  return (
    <div className="max-w-4xl mx-auto p-6">
      <h2 className="text-2xl font-semibold mb-4 text-center">
        {isEditMode ? "✏️ Sửa Thành Viên" : "➕ Thêm Thành Viên"}
      </h2>

      {/* FORM CƠ BẢN */}
      
      <PersonBasicForm
        role={role}
        personId={personId}
        onSaved={handleSavedBasic}
      />

      {/* FORM CHI TIẾT */}
      {canShowDetail && showDetailForm && personId && (
        <div className="mt-8 border-t pt-6">
          {/*  ✅ [CHANGE 3]: Truyền đúng personId đã chuẩn hoá */}
          <PersonDetailForm personId={personId} role={role} />
        </div>
      )}
    </div>
  );
}
