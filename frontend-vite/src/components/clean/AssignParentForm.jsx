import React, { useEffect, useState, useRef } from "react";
import axios from "axios";
import { API_BASE_URL } from "../../api/apiConfig";
import PersonDropdown from "../common/PersonDropdown";
import MarriageDropdown from "../common/MarriageDropdown";
import { formatName } from "../../utils/formatName";
import { useNavigate } from "react-router-dom";
function AssignParentForm() {
  const getAuthConfig = () => {
    const token = localStorage.getItem("token");

    return {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    };
  };
  const navigate = useNavigate();
  // -----------------------------
  // DATA LISTS
  // -----------------------------
  const [persons, setPersons] = useState([]);
  const [marriages, setMarriages] = useState([]);

  // 🔹 Chuẩn hóa hiển thị tên (KHÔNG sửa DB)
  const displayName = (name = "") => name.replaceAll("|", " ");
  // -----------------------------
  // FORM STATE
  // -----------------------------
  const [childId, setChildId] = useState("");
  const [noMarriage, setNoMarriage] = useState(true);
  const [marriageId, setMarriageId] = useState("");

  const [parentId, setParentId] = useState("");
  const [type, setType] = useState("");

  // -----------------------------
  // UI STATE
  // -----------------------------
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);
  const [hasFather, setHasFather] = useState(false);
  const [hasMother, setHasMother] = useState(false);
  const [lockForm, setLockForm] = useState(false);
  const [birthConflictWarning, setBirthConflictWarning] = useState("");
  const [showBirthOrderPanel, setShowBirthOrderPanel] = useState(false);
  const [birthOrderRows, setBirthOrderRows] = useState([]);
  const [birthOrderLoading, setBirthOrderLoading] = useState(false);
  const birthOrderPanelRef = useRef(null);
  useEffect(() => {
    axios.get(`${API_BASE_URL}/person`)
      .then(res => {
        const data = res.data || [];

        // ✅ [CHANGE 1]: chuẩn hóa name để dropdown không bị undefined
        const normalized = data.map(p => ({
          ...p,
          name: formatName(p)
        }));

        setPersons(normalized);
      })
      .catch(() => setPersons([]));

    axios.get(`${API_BASE_URL}/marriage`)
      .then(res => setMarriages(res.data || []))
      .catch(() => setMarriages([]));
  }, []);

  const checkParentStatus = async (id) => {
    try {
      const res = await axios.get(`${API_BASE_URL}/parent_child/child/${id}/parents-status`);
      const { has_father, has_mother } = res.data;

      setHasFather(has_father);
      setHasMother(has_mother);

      if (has_father && has_mother) {
        setError("Người này đã có đủ cha mẹ. Không thể thêm. Bấm Hủy ❌ để trở về.");
        setLockForm(true);
      } else {
        setLockForm(false);
      }
    } catch {
      setError("❌ Không kiểm tra được trạng thái cha mẹ.");
      setLockForm(true);
    }
  };
  const checkBirthConflict = async (childId) => {
    try {

      const childRes = await axios.get(
        `${API_BASE_URL}/person/${childId}`
      );

      const siblingsRes = await axios.get(
        `${API_BASE_URL}/parent_child/child/${childId}/siblings`
      );

      const child = childRes.data;
      const siblings = siblingsRes.data || [];
      console.log("BO CHECK siblings:", siblings);
      const hasBirthOrder = (p) =>
        Number.isInteger(p.birth_order) &&
        p.birth_order > 0;
      
      const missingBirthOrder = (people) =>
        people.some(p => !hasBirthOrder(p));

      // CASE 1: không có ngày sinh
      if (!child.birth_date) {

        if (siblings.length === 0) {
          setBirthConflictWarning("");
          return;
        }
      
        if (!missingBirthOrder([child, ...siblings])) {
          setBirthConflictWarning("");
          return;
        }
      
        setBirthConflictWarning(
          "⚠ Người con này chưa có ngày sinh và đã có anh/chị/em trong gia đình. Vui lòng bấm Cập nhập Birth Order để xác định anh/chị/em."
        );
      
        return;
      }

      // CASE 2: có sibling trùng ngày sinh
      const getBirthYear = (birthDate) => {
        if (!birthDate) return null;
        return String(birthDate).slice(0, 4);
      };
      const childBirthYear = getBirthYear(child.birth_date);
      const sameYearSiblings = siblings.filter((s) => {
        const siblingBirthYear = getBirthYear(s.birth_date);
        return siblingBirthYear && siblingBirthYear === childBirthYear;
      });
      console.log("childBirthYear:", childBirthYear);
      console.log("sameYearSiblings:", sameYearSiblings);
      console.log("child:", child);
      console.log("siblings:", siblings);
      if (sameYearSiblings.length > 0) {
      
        if (!missingBirthOrder([child, ...sameYearSiblings])) {
          setBirthConflictWarning("");
          return;
        }
      
        setBirthConflictWarning(
          "⚠ Có anh/chị/em trùng năm sinh. Vui lòng bấm nút Cập nhập Birth Order để xác định thứ tự sinh."
        );
      
        return;
      }
      // KHÔNG conflict
      setBirthConflictWarning("");

    } catch (err) {

      console.error("Birth conflict check error:", err);

      setBirthConflictWarning("");
    }
  };
  const openBirthOrderPanel = async () => {

    if (!childId) return;

    try {

      setBirthOrderLoading(true);

      const res = await axios.get(
        `${API_BASE_URL}/parent_child/child/${childId}/siblings`
      );

      const siblings = res.data || [];

      const childRes = await axios.get(
        `${API_BASE_URL}/person/${childId}`
      );

      const child = childRes.data;
      console.log("BO CHECK child:", child);
      const rows = [
        child,
        ...siblings
      ].sort((a, b) => {
      
        // 1. sort theo BO
        const boA = a.birth_order ?? 9999;
        const boB = b.birth_order ?? 9999;
      
        if (boA !== boB) {
          return boA - boB;
        }
      
        // 2. sort theo birth_date
        const dateA = a.birth_date || "";
        const dateB = b.birth_date || "";
      
        if (dateA !== dateB) {
          return dateA.localeCompare(dateB);
        }
      
        // 3. sort theo tên
        const nameA = displayName(
          a.name ||
          a.full_name ||
          `${a.sur_name || ""} ${a.last_name || ""} ${a.middle_name || ""} ${a.first_name || ""}`.trim()
        );
      
        const nameB = displayName(
          b.name ||
          b.full_name ||
          `${b.sur_name || ""} ${b.last_name || ""} ${b.middle_name || ""} ${b.first_name || ""}`.trim()
        );
      
        return nameA.localeCompare(nameB);
      
      });
      
      setBirthOrderRows(rows);

      setShowBirthOrderPanel(true);
      setTimeout(() => {
        birthOrderPanelRef.current?.scrollIntoView({
          behavior: "smooth",
          block: "start"
        });
      }, 100);
    } catch (err) {

      console.error("Open BO panel error:", err);

    } finally {

      setBirthOrderLoading(false);

    }
  };
  const hasDuplicateBirthOrder = () => {

    const values = birthOrderRows
      .map(p => p.birth_order)
      .filter(v => v !== null && v !== undefined && v !== "");
  
    return new Set(values).size !== values.length;
  
  };
  const saveBirthOrders = async () => {
    if (hasDuplicateBirthOrder()) {
      setError("❌ Birth Order không được trùng nhau trong cùng nhóm anh/chị/em.\n Sửa BO hoặc chọn thao tác khác");
      return;
    }
    try {
  
      await axios.put(
        `${API_BASE_URL}/person/birth-order/bulk`,
        {
          items: birthOrderRows.map((p) => ({
            person_id: p.id || p.person_id,
            birth_order: p.birth_order
          }))
        },
        getAuthConfig()
      );
  
      await checkBirthConflict(childId);
  
      setShowBirthOrderPanel(false);
  
    } catch (err) {
  
      console.error("Save BO error:", err);
  
      setError("❌ Không lưu được Birth Order");
  
    }
  };
  // -----------------------------
  // SUBMIT
  // -----------------------------
  const handleSubmit = async (e) => {
    e.preventDefault();
  
    setLoading(true);
    setError("");
    setSuccess("");
  
    try {
  
      if (!childId) {
        setError("❌ Chưa chọn người con.");
        return;
      }  
      // ===============================
      // CASE 1: KHÔNG CÓ HÔN NHÂN
      // ===============================
      if (noMarriage) {
        if (!parentId || !type) {
          setError("❌ Thiếu cha/mẹ hoặc vai trò.");
          return;
        }

        await axios.post(
          `${API_BASE_URL}/parent_child/assign`,
          {
            child_id: Number(childId),
            parent_id: Number(parentId),
            type: type
          },
          getAuthConfig()
        );
      }

      // ===============================
      // CASE 2: CÓ HÔN NHÂN → AUTO CHA + MẸ
      // ===============================
      else {
        const m = marriages.find(x => String(x.id) === String(marriageId));
        if (!m) {
          setError("❌ Không tìm thấy hôn nhân.");
          return;
        }
        try {
          // CHA
          await axios.post(
            `${API_BASE_URL}/parent_child/assign`,
            {
              child_id: Number(childId),
              parent_id: m.spouse_a_id,
              type: "father"
            },
            getAuthConfig()
          );
          // MẸ
          await axios.post(
            `${API_BASE_URL}/parent_child/assign`,
            {
              child_id: Number(childId),
              parent_id: m.spouse_a_id,
              type: "mother"
            },
            getAuthConfig()
          );
        } catch (err) {
          console.error("❌ BACKEND ERROR:", err.response?.data);
          setError(err.response?.data?.detail || "Lỗi hệ thống");
          return;
        }
      }
      setSuccess("✅ Đã bổ sung cha/mẹ thành công.");
      // 🔄 Reset form về trạng thái ban đầu sau khi lưu thành công

      setParentId('');
      setType('');
      setMarriageId('');
      setNoMarriage(true);
      setHasFather(false);
      setHasMother(false);
      setLockForm(true);

    } catch (err) {
      console.error("❌ ASSIGN ERROR:", err.response?.data || err);
    
      setError(
        err.response?.data?.detail ||
        err.response?.data?.error ||
        "❌ Lỗi hệ thống."
      );
    
    } finally {
      setLoading(false);
    }
  };

  // =========================================================
  // RENDER
  // =========================================================
  return (
    <div className="max-w-xl mx-auto p-4 bg-white shadow rounded">

      {success && <div className="text-green-600 mb-2">{success}</div>}
      {birthConflictWarning && (
        <div className="text-yellow-700 bg-yellow-100 p-2 rounded mb-2">

          <div className="flex flex-col gap-2">

            <span>{birthConflictWarning}</span>

            <button
              type="button"
              onClick={openBirthOrderPanel}
              className="w-fit px-3 py-1 bg-yellow-600 text-white rounded hover:bg-yellow-700"
            >
              Cập nhật Birth Order
            </button>

          </div>

        </div>
      )}
      <form onSubmit={handleSubmit} className="space-y-4">

        {/* ================================================= */}
        {/* 1️⃣ SELECT CON */}
        {/* ================================================= */}
        <div>
          <label className="block font-semibold">1️⃣ Người Con (bắt buộc)</label>
          <PersonDropdown
            label={null}
            value={childId}
            onChange={(id) => {
              setChildId(id);
              setError("");
              setSuccess("");
              setHasFather(false);
              setHasMother(false);
              setLockForm(false);

              if (!id) return;
              checkParentStatus(id);
              checkBirthConflict(id);
            }}
            persons={persons}
            placeholder="-- Gõ tên hoặc kéo xuống Chọn người con --"
          />
        </div>

        {/* ================================================= */}
        {/* 2️⃣ SELECT MARRIAGE */}
        {/* ================================================= */}
        {
          childId && (
            <div>
              <label className="block font-semibold">2️⃣ Thuộc gia đình (nếu có)</label>

              <label className="block mb-2">
                <input
                  type="checkbox"
                  checked={noMarriage}
                  disabled={lockForm}
                  onChange={() => {
                    const nextNoMarriage = !noMarriage;

                    // ❌ Có đúng 1 bên cha/mẹ mà chuyển sang "thuộc gia đình" → chặn
                    if (!nextNoMarriage && (hasFather ^ hasMother)) {
                      setError("❌ Người này chỉ có 1 bên cha/mẹ, không thể gán theo gia đình.");
                      return;
                    }

                    setNoMarriage(nextNoMarriage);

                    // 🔄 Nếu CHUYỂN SANG "thuộc gia đình" → reset Cha/Mẹ
                    if (!nextNoMarriage) {
                      setParentId("");
                      setType("");
                    }

                    // luôn reset marriage khi đổi mode
                    setMarriageId("");
                  }}


                />{" "}
                Không thuộc gia đình nào
              </label>

              {!noMarriage && (
                <MarriageDropdown
                  value={marriageId}
                  onChange={setMarriageId}
                  marriages={marriages}
                  placeholder="-- Gõ tên hoặc kéo xuống chọn Cha & Mẹ --"
                  disabled={lockForm}
                />
              )}
            </div>
          )
        }
        {/* ================================================= */}
        {/* 3️⃣ TYPE */}
        {/* ================================================= */}
        {
          childId && noMarriage && (
            <div>
              <label className="block font-semibold">
                3️⃣ Vai trò (bắt buộc)
              </label>
              <div className="flex gap-6">
                <label>
                  <input
                    type="radio"
                    value="father"
                    checked={type === "father"}
                    onChange={() => {
                      setType("father");
                      setParentId("");   // reset chọn Cha/Mẹ khi đổi vai trò
                    }}
                    disabled={lockForm || hasFather}
                  />

                  Cha
                </label>

                <label>
                  <input
                    type="radio"
                    value="mother"
                    checked={type === "mother"}
                    onChange={() => {
                      setType("mother");
                      setParentId("");   // reset cho đồng bộ
                    }}
                    disabled={lockForm || hasMother}
                  />

                  Mẹ
                </label>
              </div>
            </div>
          )
        }

        {/* ================================================= */}
        {/* 4️⃣ SELECT PARENT */}
        {/* ================================================= */}
        {
          childId && noMarriage && !lockForm && (
            <div>
              <label className="block font-semibold">
                4️⃣ Cha / Mẹ (bắt buộc)
              </label>
              <PersonDropdown
                label={null}
                value={parentId}
                onChange={setParentId}
                persons={persons}
                disabled={lockForm}
                filterFn={(p) => {
                  const t = (type || "").toLowerCase();

                  if (t === "father") return p.gender === "male";
                  if (t === "mother") return p.gender === "female";

                  return false;
                }}
                placeholder="-- Gõ tên hoặc kéo xuống chọn --"
              />
            </div>
          )
        }

        {/* ================================================= */}
        {/* BUTTONS */}
        {/* ================================================= */}
        <div className="flex justify-between pt-4">
          {/* NÚT HỦY */}
          <button
            type="button"
            className="px-4 py-2 bg-gray-400 text-white rounded"
            onClick={() => {
              setParentId('');
              setType('');
              setMarriageId('');
              setNoMarriage(true);
              setError('');
              setSuccess('');
              setHasFather(false);
              setHasMother(false);
              setLockForm(false);
            }}
          >
            ❌ Hủy
          </button>

          {/* 🔵 [CHANGE]: Ẩn Lưu khi đã lockForm (đã lưu xong) */}
          {!lockForm && (
            <button
              type="submit"
              disabled={loading}
              className={`px-4 py-2 text-white rounded ${
                loading
                  ? "bg-blue-300 cursor-not-allowed"
                  : "bg-blue-600 hover:bg-blue-700"
              }`}
            >
              {loading ? "⏳ Đang kiểm tra quyền..." : "💾 Lưu"}
            </button>
          )}
          {lockForm && (
            <button
              type="button"
              onClick={() => navigate("/")}
              className="px-4 py-2 bg-gray-600 text-white rounded"
            >
              ⬅ Quay về Home
            </button>
          )}
        </div>
        {error && (
          <div className="text-red-600 mb-2 whitespace-pre-line">
            {error}
          </div>
        )}
        {showBirthOrderPanel && (
          <div
            ref={birthOrderPanelRef}
            className="mt-4 border rounded p-4 bg-gray-50"
          >

            <h3 className="font-bold mb-4">
              Cập nhật Birth Order
            </h3>

            <div className="space-y-2">

              {birthOrderRows.map((p) => (

                <div
                  key={p.id}
                  className="flex items-center justify-between gap-4"
                >

                  <div className="flex-1">
                  {displayName(
                    p.name ||
                    p.full_name ||
                    p.fullname ||
                    [p.sur_name, p.last_name, p.middle_name, p.first_name]
                      .filter(Boolean)
                      .join(" ")
                  )}
                  </div>

                  <div className="flex-1 text-sm text-gray-600">
                    {p.birth_date || "Chưa có ngày sinh"}
                  </div>

                  <input
                    type="number"
                    min={1}
                    value={p.birth_order || ""}
                    onChange={(e) => {
                      setError("");
                      const value = e.target.value;

                      setBirthOrderRows(rows =>
                        rows.map(r =>
                          r.id === p.id
                            ? {
                              ...r,
                              birth_order:
                                value === ""
                                  ? null
                                  : Number(value)
                            }
                            : r
                        )
                      );

                    }}
                    className="w-24 border rounded p-1"
                    placeholder="BO"
                  />

                </div>
              ))}

            </div>

              <div className="flex gap-2 mt-4">

                <button
                  type="button"
                  onClick={saveBirthOrders}
                  className="px-4 py-2 bg-amber-500 text-white rounded hover:bg-amber-600"
                >
                  💾 Lưu BO
                </button>

                <button
                  type="button"
                  onClick={() => setShowBirthOrderPanel(false)}
                  className="px-4 py-2 bg-gray-500 text-white rounded"
                >
                  Đóng
                </button>

              </div>

          </div>
        )}
      </form >
    </div >
  );
}

export default AssignParentForm;
