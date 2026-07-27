// ======================================================================
// File: MarriageForm.jsx (v11.6-FINAL)
// Mô tả:
//   - Tích hợp PersonSelectWithAvatarV2
//   - Sort danh sách: Có năm sinh → có năm mất → theo ABC
//   - Avatar đúng chuẩn avatarEngine
//   - Convert ngày VN <→ ISO
//   - Load dữ liệu edit chuẩn
// ======================================================================

import React, { useEffect, useRef, useState } from "react";
import {
  addMarriage,
  getMarriageById,
  updateMarriage,
} from "../../api/marriageApi";
import {
  getPersonBasicList,
  getPersonBasicById,
} from "../../api/personBasicApi";
import { checkNearAccess } from "../../api/authApi";
// Utils ngày tháng
import { formatDateVN, parseVNDate, detectPrecision } from "../../utils/formatDate";
import { formatName } from "../../utils/formatName";
import { handleAuthError } from "../../utils/authErrorHandler";
// Component dropdown avatar chuẩn mới
import PersonSelectWithAvatarV2 from "../common/PersonSelectWithAvatarV2";

// ======================================================================
// Component chính
// ======================================================================
export default function MarriageForm({ role = "admin", editId = null, onBack }) {

  if (role === "viewer") {
    return (
      <p className="text-red-500 text-center">
        ❌ Bạn không có quyền thêm hoặc chỉnh sửa quan hệ hôn nhân.
      </p>
    );
  }

  // STATE – form
  const [formData, setFormData] = useState({
    spouse_a_id: "",
    spouse_b_id: "",
    start_date: "",
    end_date: "",
    start_precision: "exact",
    end_precision: "exact",
    status: "",
    priority: 0,
    ceremony_type: "",
    location: "",
    notes: "",
    consanguineous: 0,
  });
  // STATE – filter gender
  const [filterHusbandGender, setFilterHusbandGender] = useState(true);
  const [filterWifeGender, setFilterWifeGender] = useState(true);
  const husbandGender = filterHusbandGender ? 'male' : null;
  const wifeGender = filterWifeGender ? 'female' : null;

  // STATE – data / ui
  const [persons, setPersons] = useState([]);
  const [errorMsg, setErrorMsg] = useState("");
  const [statusError, setStatusError] = useState("");
  const statusRef = useRef(null);
  const [successMsg, setSuccessMsg] = useState("");
  const [loading, setLoading] = useState(false);
  const [canShowMarriageDetails, setCanShowMarriageDetails] = useState(
    role !== "member_basic"
  );
  const [checkingNearAccess, setCheckingNearAccess] = useState(false);
  const [selectedPersonDetails, setSelectedPersonDetails] = useState({
    spouseA: null,
    spouseB: null,
  });
  const [lifeDataWarnings, setLifeDataWarnings] = useState([]);
  const [mode, setMode] = useState("full");
  const [showSurName, setShowSurName] = useState(true);

  // ======================================================================
  // Load danh sách Person (với sorting chuẩn)
  // ======================================================================
  useEffect(() => {
    async function fetchPersons() {
      try {

        const list = await getPersonBasicList();

        const sorted = [...list]
          .filter((p) => p.delete_status === undefined || Number(p.delete_status) === 0)
          .sort((a, b) => {
            const ay = a.birth_date ? Number(a.birth_date.slice(0, 4)) : 0;
            const by = b.birth_date ? Number(b.birth_date.slice(0, 4)) : 0;

            if (ay && !by) return -1;
            if (!ay && by) return 1;
            if (ay && by && ay !== by) return ay - by;

            const ad = a.death_date ? Number(a.death_date.slice(0, 4)) : 9999;
            const bd = b.death_date ? Number(b.death_date.slice(0, 4)) : 9999;
            if (ad !== bd) return ad - bd;

            const an = (a.full_name_vn ||
              [a.last_name, a.middle_name, a.first_name].filter(Boolean).join(" ")).trim();
            const bn = (b.full_name_vn ||
              [b.last_name, b.middle_name, b.first_name].filter(Boolean).join(" ")).trim();

            return an.localeCompare(bn);
          });

        setPersons(sorted);
      } catch (err) {
        if (handleAuthError(err)) {
          return;
        }
        console.error(err);
        setErrorMsg("❌ Không thể tải danh sách thành viên!");
      }
    }
    fetchPersons();
  }, []);

  // ======================================================================
  // Load EDIT
  // ======================================================================
  useEffect(() => {
    if (editId) {
      loadOldData(editId);
    } else {
      resetForm(); // ✅ [CHANGE]: vào chế độ Thêm mới thì xóa dữ liệu cũ
    }
  }, [editId]);
  // ======================================================================
  // Kiểm tra quyền ngay sau khi chọn đủ hai người
  // ======================================================================
  useEffect(() => {
    let cancelled = false;

    const verifySelectedPeopleAccess = async () => {
      const spouseAId = formData.spouse_a_id;
      const spouseBId = formData.spouse_b_id;

      // Admin và co_operator không cần khóa phần chi tiết
      if (role !== "member_basic") {
        setCanShowMarriageDetails(true);
        setCheckingNearAccess(false);
        return;
      }

      // Member chưa chọn đủ hai người: chưa mở phần chi tiết
      if (!spouseAId || !spouseBId) {
        setCanShowMarriageDetails(false);
        setCheckingNearAccess(false);
        setErrorMsg("");
        return;
      }

      setCheckingNearAccess(true);
      setCanShowMarriageDetails(false);
      setErrorMsg("");

      try {
        const [accessA, accessB] = await Promise.all([
          checkNearAccess(spouseAId),
          checkNearAccess(spouseBId),
        ]);

        if (cancelled) return;

        const allowed = Boolean(accessA?.allowed || accessB?.allowed);
        setCanShowMarriageDetails(allowed);

        if (!allowed) {
          setErrorMsg(
            "❌ Bạn không có quyền thêm/chỉnh sửa quan hệ hôn nhân này."
          );
        }
      } catch (err) {
        if (cancelled) return;

        setCanShowMarriageDetails(false);

        if (handleAuthError(err)) {
          return;
        }

        setErrorMsg("❌ Không thể kiểm tra quyền quan hệ gần.");
      } finally {
        if (!cancelled) {
          setCheckingNearAccess(false);
        }
      }
    };

    verifySelectedPeopleAccess();

    return () => {
      cancelled = true;
    };
  }, [role, formData.spouse_a_id, formData.spouse_b_id]);
  // ======================================================================
  // Kiểm tra dữ liệu ngày qua đời / ngày giỗ của hai người
  // ======================================================================
  useEffect(() => {
    let cancelled = false;

    const checkLifeData = async () => {
      const spouseAId = formData.spouse_a_id;
      const spouseBId = formData.spouse_b_id;

      // Chỉ đọc chi tiết khi đã chọn đủ và đã được phép mở form
      if (!spouseAId || !spouseBId || !canShowMarriageDetails) {
        setSelectedPersonDetails({
          spouseA: null,
          spouseB: null,
        });
        setLifeDataWarnings([]);
        return;
      }

      try {
        const [spouseA, spouseB] = await Promise.all([
          getPersonBasicById(spouseAId),
          getPersonBasicById(spouseBId),
        ]);

        if (cancelled) return;

        setSelectedPersonDetails({
          spouseA,
          spouseB,
        });

        const createWarning = (person, fallbackName) => {
          const name =
            person?.full_name_vn ||
            [
              person?.sur_name,
              person?.last_name,
              person?.middle_name,
              person?.first_name,
            ]
              .filter(Boolean)
              .join(" ") ||
            fallbackName;

          return `⚠️ ${name}: không đủ dữ liệu ngày tháng hoặc đã qua đời. Cần kiểm tra trước khi thêm mối quan hệ hôn nhân.`;
        };

        setLifeDataWarnings([
          createWarning(spouseA, "Người chồng"),
          createWarning(spouseB, "Người vợ"),
        ]);
      } catch (err) {
        if (cancelled) return;

        setSelectedPersonDetails({
          spouseA: null,
          spouseB: null,
        });

        if (handleAuthError(err)) {
          return;
        }

        setLifeDataWarnings([
          "⚠️ Không thể kiểm tra dữ liệu ngày qua đời/ngày giỗ.",
        ]);
      }
    };

    checkLifeData();

    return () => {
      cancelled = true;
    };
  }, [
    canShowMarriageDetails,
    formData.spouse_a_id,
    formData.spouse_b_id,
  ]);

  const loadOldData = async (id) => {
    try {
      const data = await getMarriageById(id);

      setFormData({
        spouse_a_id: data.spouse_a_id ? String(data.spouse_a_id) : "",
        spouse_b_id: data.spouse_b_id ? String(data.spouse_b_id) : "",
        start_date: formatDateVN(data.start_date),
        end_date: formatDateVN(data.end_date),
        start_precision: detectPrecision(data.start_date),
        end_precision: detectPrecision(data.end_date),
        status: data.status ?? "",
        priority: data.priority ?? 0,
        ceremony_type: data.ceremony_type ?? "",
        location: data.location ?? "",
        notes: data.notes ?? "",
        consanguineous: data.consanguineous ?? 0,
      });
    } catch (err) {
      if (handleAuthError(err)) {
        return;
      }
      setErrorMsg("❌ Không thể tải dữ liệu hôn nhân cần chỉnh sửa!");
    }
  };

  // ======================================================================
  // Chung: handleChange
  // ======================================================================
  const handleChange = (name, value) => {
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
    setErrorMsg("");
    setSuccessMsg("");
  };

  // ======================================================================
  // RESET
  // ======================================================================
  const resetForm = () => {
    setFormData({
      spouse_a_id: "",
      spouse_b_id: "",
      start_date: "",
      end_date: "",
      start_precision: "exact",
      end_precision: "exact",
      status: "",
      priority: 0,
      ceremony_type: "",
      location: "",
      notes: "",
      consanguineous: 0,
    });
    setErrorMsg("");
    setStatusError("");
    setSuccessMsg("");
  };

  // ======================================================================
  // SUBMIT
  // ======================================================================
  const handleSubmit = async (e) => {
    e.preventDefault();

    setLoading(true);
    setErrorMsg("");
    setSuccessMsg("");

    const {
      spouse_a_id,
      spouse_b_id,
      start_date,
      end_date,
      status,
      priority,
      ceremony_type,
      location,
      notes,
      consanguineous,
    } = formData;

    if (!spouse_a_id || !spouse_b_id) {
      setErrorMsg("⚠️ Vui lòng chọn đầy đủ Vợ và Chồng.");
      setLoading(false);
      return;
    }

    if (spouse_a_id === spouse_b_id) {
      setErrorMsg("❌ Vợ và Chồng không thể là cùng một người.");
      setLoading(false);
      return;
    }
    // Y3: chỉ chặn trùng người khi gender = other
    if (
      husbandGender === null &&
      spouse_a_id === spouse_b_id
    ) {
      setLoading(false);
      return; // silent block, không popup
    }
    if (!status) {
      setStatusError("⚠️ Vui lòng chọn tình trạng hôn nhân.");
      setLoading(false);

      requestAnimationFrame(() => {
        statusRef.current?.focus({ preventScroll: true });
        statusRef.current?.scrollIntoView({
          behavior: "smooth",
          block: "center",
        });
      });

      return;
    }

    const start_iso = parseVNDate(start_date);
    const end_iso = parseVNDate(end_date);
    // ======================================================
    // Dynamic Close Member Check
    // ======================================================

    try {
      const accessA = await checkNearAccess(spouse_a_id);
      const accessB = await checkNearAccess(spouse_b_id);

      if (!accessA.allowed && !accessB.allowed) {
        setErrorMsg("❌ Bạn không có quyền thêm/chỉnh sửa quan hệ hôn nhân này.");
        setLoading(false);
        return;
      }
      let res;
      if (editId) {
        res = await updateMarriage(editId, {
          spouse_a_id,
          spouse_b_id,
          start_date: start_iso,
          end_date: end_iso,
          status,
          priority,
          ceremony_type: ceremony_type || null,
          location,
          notes,
          consanguineous,
        });

      } else {
        res = await addMarriage({
          spouse_a_id,
          spouse_b_id,
          start_date: start_iso,
          end_date: end_iso,
          status,
          priority,
          ceremony_type: ceremony_type || null,
          location,
          notes,
          consanguineous,
        });

        resetForm();
      }

      setSuccessMsg(res.message || "✅ Lưu quan hệ hôn nhân thành công!Trở về đầu Form nhập mới hoặc HOME");

      if (editId && onBack) {
        setTimeout(() => {
          onBack();   // quay lại danh sách
        }, 500);      // đợi 0.5s cho user thấy thông báo
      }

    } catch (err) {
      if (handleAuthError(err)) {
        return;
      }
      const data = err.response?.data;

      const msg =
        data?.message ||
        data?.detail?.message ||
        data?.detail ||
        data?.warning ||
        data?.error ||
        "❌ Không thể lưu quan hệ hôn nhân!";

      setErrorMsg(msg);
    } finally {
      setLoading(false);
    }
  };

  // ======================================================================
  // UI
  // ======================================================================
  return (
    <div className="max-w-3xl mx-auto p-6 bg-white shadow-lg rounded-xl mt-6">
      <h2 className="text-2xl font-bold text-blue-700 mb-4 text-center">
        {editId ? "✏️ Chỉnh Sửa Quan Hệ Hôn Nhân" : "💍 Thêm Quan Hệ Hôn Nhân"}
      </h2>

      <form onSubmit={handleSubmit} className="space-y-4" noValidate>

        <PersonSelectWithAvatarV2
          label="👨 Chồng:"
          value={formData.spouse_a_id}
          genderFilter={husbandGender}
          onChange={(v) =>
            setFormData((prev) => ({
              ...prev,
              spouse_a_id: v,
            }))
          }
          persons={persons}
        />
        <div className="flex items-center space-x-2 mb-3">
          <input
            type="checkbox"
            checked={filterHusbandGender}
            onChange={(e) => setFilterHusbandGender(e.target.checked)}
          />
          <span className="text-sm text-gray-600">
            Chỉ hiện người giới tính Nam
          </span>
        </div>
        <PersonSelectWithAvatarV2
          label="👩 Vợ:"
          value={formData.spouse_b_id}
          genderFilter={wifeGender}
          onChange={(v) =>
            setFormData((prev) => ({
              ...prev,
              spouse_b_id: v,
            }))
          }
          persons={persons}
        />
        <div className="flex items-center space-x-2 mb-3">
          <input
            type="checkbox"
            checked={filterWifeGender}
            onChange={(e) => setFilterWifeGender(e.target.checked)}
          />
          <span className="text-sm text-gray-600">
            Chỉ hiện người giới tính Nữ
          </span>
        </div>

        {checkingNearAccess && (
          <div className="p-2 bg-blue-100 text-blue-700 rounded text-center font-medium">
            ⏳ Đang kiểm tra quyền quan hệ gần...
          </div>
        )}

        {errorMsg && (
          <div className="p-2 bg-red-100 text-red-700 rounded text-center font-medium">
            {errorMsg}
          </div>
        )}

        {successMsg && (
          <div className="p-2 bg-green-100 text-green-700 rounded text-center font-medium">
            {successMsg}
          </div>
        )}
    {canShowMarriageDetails && lifeDataWarnings.length > 0 && (
      <div className="p-3 bg-yellow-100 text-yellow-800 rounded font-medium space-y-1">
        {lifeDataWarnings.map((warning, index) => (
          <p key={index}>{warning}</p>
        ))}
      </div>
    )}
    {canShowMarriageDetails && (
      <>
        {/* Ngày cưới */}
        <div>
          <label className="block mb-1 font-medium text-gray-700">📅 Ngày cưới:</label>
          <input
            type="text"
            value={formData.start_date}
            onChange={(e) => handleChange("start_date", e.target.value)}
            placeholder="dd/mm/yyyy hoặc mm/yyyy hoặc yyyy"
            className="w-full border border-gray-300 rounded p-2"
          />
        </div>

        {/* Ngày kết thúc */}
        <div>
          <label className="block mb-1 font-medium text-gray-700">💔 Ngày kết thúc:</label>
          <input
            type="text"
            value={formData.end_date}
            onChange={(e) => handleChange("end_date", e.target.value)}
            placeholder="dd/mm/yyyy hoặc mm/yyyy hoặc yyyy"
            className="w-full border border-gray-300 rounded p-2"
          />
        </div>

        {/* Tình trạng + Ưu tiên */}
        <div className="grid grid-cols-2 gap-4">

          {/* Tình trạng */}
          <div>
            <label className="block mb-1 font-medium text-gray-700">
              💍 Tình trạng:
            </label>

            <select
              ref={statusRef}
              value={formData.status}
              onChange={(e) => {
                handleChange("status", e.target.value);
                setStatusError("");
              }}
              required
              aria-invalid={Boolean(statusError)}
              aria-describedby="status-error"
              className={`w-full border rounded p-2 ${
                statusError
                  ? "border-red-500 ring-1 ring-red-500"
                  : "border-gray-300"
              }`}
            >
              <option value="" disabled>
                -- Chọn tình trạng hôn nhân --
              </option>
              <option value="married">Đã kết hôn</option>
              <option value="cohabiting">Sống chung</option>
              <option value="separated">Ly thân</option>
              <option value="divorced">Ly hôn</option>
            </select>

            {statusError && (
              <p
                id="status-error"
                className="mt-1 text-sm font-medium text-red-600"
              >
                {statusError}
              </p>
            )}
          </div>

          {/* Ưu tiên */}
          <div>
            <label className="block mb-1 font-medium text-gray-700">
              ⭐ Ưu tiên:
            </label>

            <input
              type="number"
              value={formData.priority}
              onChange={(e) =>
                handleChange(
                  "priority",
                  Number(e.target.value)
                )
              }
              className="w-full border border-gray-300 rounded p-2"
            />
          </div>

        </div>

        {/* Ghi chú */}
        <div>
          <label className="block mb-1 font-medium text-gray-700">📝 Ghi chú:</label>
          <input
            type="text"
            value={formData.notes}
            onChange={(e) => handleChange("notes", e.target.value)}
            className="w-full border border-gray-300 rounded p-2"
          />
        </div>

        {/* Cùng huyết thống */}
        <div className="flex items-center space-x-2 mt-3">
          <input
            type="checkbox"
            id="consanguineous"
            checked={Number(formData.consanguineous) === 1}
            onChange={(e) =>
              handleChange("consanguineous", e.target.checked ? 1 : 0)
            }
            className="w-4 h-4 accent-red-600 cursor-pointer"
          />
          <label
            htmlFor="consanguineous"
            className="font-medium text-gray-700 cursor-pointer"
          >
            Cùng huyết thống (≤ 5 đời)
          </label>
        </div>

        {/* Nút */}
        <div className="flex justify-between gap-4 pt-2">
        <button
          type="submit"
          disabled={loading}
          className={`flex-1 text-white px-4 py-2 rounded ${
            loading
              ? "bg-green-300 cursor-not-allowed"
              : "bg-green-600 hover:bg-green-700"
          }`}
        >
          {loading ? "⏳ Đang lưu..." : "💾 Lưu Quan Hệ"}
        </button>

          <button
            type="button"
            onClick={onBack || resetForm}
            className="flex-1 bg-gray-400 text-white px-4 py-2 rounded hover:bg-gray-500"
          >
            ⬅️ {editId ? "Quay lại" : "Hủy / Nhập lại"}
          </button>
        </div>
        </>
      )}
      </form>
    </div>
  );
}
