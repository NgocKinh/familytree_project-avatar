// ======================================================================
// File: src/components/person/PersonBasicForm.jsx
// ======================================================================

import React, { useEffect, useState } from "react";
import { useParams, useNavigate, useLocation } from "react-router-dom";

import {
  addPerson,
  updatePerson,
  getPersonById,
  checkDuplicatePerson,
  uploadAvatar,
} from "../../api/personApi";

import { getAvatarURL, fallbackAvatar, handleAvatarError } from "../../utils/avatarEngine";

import {
  formatDateVN,
  parseVNDate,
  detectPrecision,
} from "../../utils/formatDate";

import AvatarUploaderUltraTriple from "../AvatarUploaderUltraTriple";

// ✅ [CHANGE 1]: Nhận personId từ cha (AddPersonPage)
export default function PersonBasicForm({ role, onSaved, personId }) {
  const { id } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const onAvatarUpdated = location.state?.onAvatarUpdated;
  // ✅ [CHANGE 2]: Ưu tiên personId từ props
  const realId = personId || id;

  // ✅ [CHANGE 3]: Xác định edit theo realId
  const isEdit = Boolean(realId && realId !== "new");

  // =========================
  // STATE
  // =========================
  const [form, setForm] = useState({
    sur_name: "",
    last_name: "",
    middle_name: "",
    first_name: "",
    gender: "",
    birth_date: "",
    death_date: "",
    birth_date_precision: "unknown",
    death_date_precision: "unknown",
  });

  const [avatarPreview, setAvatarPreview] = useState(null);
  const [showAvatarEditor, setShowAvatarEditor] = useState(false);
  const [showPendingModal, setShowPendingModal] = useState(false);
  const [duplicateMessage, setDuplicateMessage] = useState("");

  // =========================
  // RESET FORM
  // =========================
  const resetForm = () => {
    setForm({
      sur_name: "",
      last_name: "",
      middle_name: "",
      first_name: "",
      gender: "",
      birth_date: "",
      death_date: "",
      birth_date_precision: "unknown",
      death_date_precision: "unknown",
    });
    // 🔵 [ADDED]
    setAvatarPreview(null);
    setDuplicateMessage("");
  };

  // =========================
  // LOAD DATA (EDIT) - FINAL CLEAN
  // =========================

  const [loading, setLoading] = useState(false);

  // 👉 LOAD DATA
  const loadData = async (id) => {
    try {
      setLoading(true);

      console.log("🔥 LOAD PERSON ID:", id);

      const data = await getPersonById(id);

      setForm({
        sur_name: data.sur_name || "",
        last_name: data.last_name || "",
        middle_name: data.middle_name || "",
        first_name: data.first_name || "",
        gender: data.gender || "",
        birth_date: formatDateVN(
          data.birth_date,
          data.birth_date_precision
        ),
        death_date: formatDateVN(
          data.death_date,
          data.death_date_precision
        ),
        birth_date_precision: data.birth_date_precision || "unknown",
        death_date_precision: data.death_date_precision || "unknown",
      });

    } catch (err) {
      console.error("❌ Load error:", err);
    } finally {
      setLoading(false);
    }
  };
  // 👉 CHỈ LOAD 1 LẦN KHI CÓ ID
  useEffect(() => {
    // 🔵 [CHANGE 1]: reset avatar khi KHÔNG phải edit
    if (!isEdit) {
      setAvatarPreview(null);
    }
  }, [isEdit]);
  // =========================
  // 🔵 LOAD DATA WHEN EDIT
  // =========================
  useEffect(() => {
    console.log("🔥 isEdit:", isEdit, "realId:", realId);

    if (isEdit && realId) {
      loadData(realId);
    }

  }, [realId, isEdit]);
  // =========================
  // AVATAR
  // =========================

  // 🔵 [CHANGE 2]: tránh dính avatar cũ
  const displayAvatar = avatarPreview
    ? avatarPreview
    : isEdit
      ? getAvatarURL({ id: realId, gender: form.gender })
      : fallbackAvatar(form.gender);

  // =========================
  // HANDLE CHANGE
  // =========================
  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  // =========================
  // SUBMIT
  // =========================
  const handleSubmit = async (e) => {
    e.preventDefault();

    // ✅ [CHANGE]: disable duplicate check hoàn toàn
    try {
      const dupRes = await checkDuplicatePerson({
        last_name: form.last_name,
        first_name: form.first_name,
        gender: form.gender,
      });
    
      if (dupRes?.duplicate) {
        const realMatches = (dupRes.matches || []).filter(
          (p) => Number(p.person_id) !== Number(id)
        );
      
        if (realMatches.length > 0) {
          console.log("🔥 DUPLICATE FOUND", realMatches);
          setDuplicateMessage(JSON.stringify(realMatches, null, 2));
          setShowPendingModal(true);
          return;
        }
      }
    
    } catch (err) {
      console.error("❌ Duplicate API ERROR:", err);
      return;
    }

    const payload = {
      ...form,
      birth_date: parseVNDate(form.birth_date),
      death_date: parseVNDate(form.death_date),
      birth_date_precision: detectPrecision(form.birth_date),
      death_date_precision: detectPrecision(form.death_date),
      role,
    };

    try {
      
      if (isEdit) {
        console.log("🔥 BEFORE API");
        await updatePerson(realId, payload);
        alert("✅ Cập nhật thành công!");
      } else {
        const res = await addPerson(payload);
        console.log("🔥 ADD RESPONSE:", res);

        alert("✅ Thêm thành công!");
        navigate("/person");
      }
    
      if (onSaved) onSaved();
    
    } catch (err) {
      console.error("❌ Submit error:", err);
      alert("❌ Không thể lưu dữ liệu!");
    }
  };

  // =========================
  // SEND TO PENDING
  // =========================
  const sendToPending = async () => {
    try {
      await addPerson({ ...form, role });
      alert("🟡 Đã gửi Pending!");
      setShowPendingModal(false);
      resetForm();
      navigate("/pending");
    } catch (err) {
      console.error(err);
      alert("Không gửi được Pending!");
    }
  };

  // =========================
  // UI
  // =========================
  return (
    <div className="max-w-xl mx-auto p-4 border rounded shadow">
      <h2 className="text-2xl font-bold mb-4">
        {isEdit ? "Chỉnh sửa thành viên" : "Thêm thành viên mới"}
      </h2>

      {/* AVATAR */}
      
      <div className="flex flex-col items-center mb-6">
        {!showAvatarEditor && (
          <div
            className="relative mb-3 cursor-pointer group"
            onClick={() => setShowAvatarEditor(true)}
            title="Click để chỉnh sửa avatar"
          >
            <img
              src={displayAvatar}
              onError={(e) => handleAvatarError(e, form.gender)}
              alt="avatar"
              className="w-24 h-24 rounded-full object-cover border"
            />

            <div className="absolute inset-0 flex items-center justify-center rounded-full bg-black/40 opacity-0 group-hover:opacity-100 transition">
              <span className="text-white text-lg">✏️</span>
            </div>
          </div>
        )}
      </div>
      
      {isEdit && showAvatarEditor && (
        <div className="flex flex-col items-center mt-4">
          <AvatarUploaderUltraTriple
            personId={realId}
            onAvatarUpdated={onAvatarUpdated}
          />

          <button
            onClick={() => setShowAvatarEditor(false)}
            className="mt-3 text-sm text-gray-500 hover:text-black"
          >
            Đóng chỉnh sửa
          </button>
        </div>
      )}
      {/* FORM */}
      <form onSubmit={handleSubmit} autoComplete="off">
        <input
          type="text"
          name="fake-username"
          autoComplete="username"
          style={{ display: "none" }}
        />

        <input
          type="password"
          name="fake-password"
          autoComplete="new-password"
          style={{ display: "none" }}
        />
        {[
          ["👑 Tên hiệu", "sur_name"],
          ["🏡 Tên họ", "last_name"],
          ["🧩 Tên đệm", "middle_name"],
          ["🌟 Tên chính", "first_name"],
        ].map(([label, name]) => (
          <div className="mb-2" key={name}>
            <label>{label}:</label>
            <input
              autoComplete="off"
              name={name}
              value={form[name]}
              onChange={handleChange}
              className="border p-2 w-full"
              required={name === "last_name" || name === "first_name"}
            />
          </div>
        ))}

        <div className="mb-2">
          <label>🚻 Giới tính:</label>
          <select
            name="gender"
            value={form.gender}
            onChange={handleChange}
            className="border p-2 w-full"
            required
          >
            <option value="">-- chọn --</option>
            <option value="male">Nam</option>
            <option value="female">Nữ</option>
            <option value="other">Khác</option>
          </select>
        </div>

        <div className="mb-2">
          <label>🎂 Ngày sinh:</label>
          <input
            autoComplete="off"
            type="text"
            name="birth_date"
            value={form.birth_date}
            onChange={handleChange}
            className="border p-2 w-full"
          />
        </div>

        <div className="mb-2">
          <label>🕯 Ngày mất:</label>
          <input
            autoComplete="off"
            type="text"
            name="death_date"
            value={form.death_date}
            onChange={handleChange}
            className="border p-2 w-full"
          />
        </div>

        <div className="mt-3 flex gap-3">
          <button
            type="submit"
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
          >
            💾 Lưu
          </button>

          {!isEdit && (
            <button
              type="button"
              onClick={resetForm}
              className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded"
            >
              ➕ Hủy và Thêm Mới
            </button>
          )}
        </div>
      </form>

      {/* MODAL PENDING */}
      {showPendingModal && (
        <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center">
          <div className="bg-white p-6 rounded shadow w-[400px]">
            <h3 className="text-xl font-bold mb-2 text-red-600">
              ⚠️ Trùng thành viên
            </h3>
            <p className="mb-3">{duplicateMessage}</p>

            <div className="text-right space-x-2">
              <button
                onClick={() => setShowPendingModal(false)}
                className="px-3 py-1 bg-gray-300 rounded"
              >
                Hủy
              </button>

              <button
                onClick={sendToPending}
                className="px-3 py-1 bg-yellow-600 text-white rounded"
              >
                🟡 Gửi Pending
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
