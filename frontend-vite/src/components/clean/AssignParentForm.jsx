import React, { useEffect, useState, useRef } from "react";
import axios from "axios";
import { API_BASE_URL } from "../../api/apiConfig";
import PersonDropdown from "../common/PersonDropdown";
import MarriageDropdown from "../common/MarriageDropdown";
import { formatName } from "../../utils/formatName";
import { useNavigate } from "react-router-dom";
import BirthOrderPanel from "../birth_order/BirthOrderPanel";
import useBirthOrder from "../birth_order/useBirthOrder";
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
  const birthOrder = useBirthOrder({
    persons,
    getAuthConfig,
  });
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
      const res = await axios.get(
        `${API_BASE_URL}/parent_child/child/${id}/parents-status`,
        getAuthConfig()
      );
  
      const father = res.data?.father;
      const mother = res.data?.mother;
  
      const has_father = !!father;
      const has_mother = !!mother;
  
      setHasFather(has_father);
      setHasMother(has_mother);
  
      if (has_father && has_mother) {
        setError(
          "❌ Người con này đã có đủ Cha và Mẹ. Không thể thêm vào gia đình khác."
        );
        setLockForm(true);
      } else {
        setLockForm(false);
      }
    } catch (err) {
      console.error(
        "Check parent status error:",
        err.response?.data || err
      );
  
      setError(
        "❌ Không kiểm tra được trạng thái Cha/Mẹ của người con."
      );
  
      setLockForm(true);
    }
  };

  // -----------------------------
  // SUBMIT
  // -----------------------------
  const handleSubmit = async (e, options = {}) => {
    e?.preventDefault?.();
  
    const skipBirthOrderCheck = options.skipBirthOrderCheck === true;

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
          setError("❌ Vui lòng chọn Cha/Mẹ và vai trò cần thêm.");
          return;
        }
      
        if (hasFather && hasMother) {
          setError("❌ Người con này đã có đủ Cha và Mẹ.");
          return;
        }
      
        if (type === "father" && hasFather) {
          setError("❌ Người con này đã có Cha. Nếu muốn bổ sung, vui lòng chọn vai trò Mẹ.");
          return;
        }
      
        if (type === "mother" && hasMother) {
          setError("❌ Người con này đã có Mẹ. Nếu muốn bổ sung, vui lòng chọn vai trò Cha.");
          return;
        }
      
        await axios.post(
          `${API_BASE_URL}/parent_child/assign`,
          {
            child_id: Number(childId),
            parent_id: Number(parentId),
            type: type,
          },
          getAuthConfig()
        );
      }

      // ===============================
      // CASE 2: CÓ HÔN NHÂN → AUTO CHA + MẸ
      // ===============================
      else {

        // Đã có đủ cha và mẹ
        if (hasFather && hasMother) {
          setError(
            "❌ Người con này đã có đủ Cha và Mẹ. Không thể thêm vào gia đình khác."
          );
          return;
        }

        // Đã có cha nhưng chưa có mẹ
        if (hasFather && !hasMother) {
          setError(
            "❌ Người con này đã có Cha. Nếu muốn bổ sung Mẹ, vui lòng chọn 'Không thuộc gia đình nào' rồi chọn vai trò Mẹ."
          );
          return;
        }

        // Đã có mẹ nhưng chưa có cha
        if (!hasFather && hasMother) {
          setError(
            "❌ Người con này đã có Mẹ. Nếu muốn bổ sung Cha, vui lòng chọn 'Không thuộc gia đình nào' rồi chọn vai trò Cha."
          );
          return;
        }

        const m = marriages.find(
          x => String(x.id) === String(marriageId)
        );

        const boResult = skipBirthOrderCheck
          ? { opened: false }
          : await birthOrder.checkBeforeSave(childId, marriageId);

        if (boResult.opened) {
          setLoading(false);
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
              parent_id: m.spouse_b_id,
              type: "mother"
            },
            getAuthConfig()
          );

        } catch (err) {

          console.error(
            "❌ BACKEND ERROR:",
            err.response?.data
          );

          const data = err.response?.data;

          setError(
            data?.message ||
            data?.detail?.message ||
            data?.detail ||
            data?.warning ||
            data?.error ||
            "❌ Không thể bổ sung người con vào gia đình này."
          );

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

      const data = err.response?.data;

      setError(
        data?.message ||
        data?.detail?.message ||
        data?.detail ||
        data?.warning ||
        data?.error ||
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
      {birthOrder.birthConflictWarning && (
        <div className="text-yellow-700 bg-yellow-100 p-2 rounded mb-2">

          <div className="flex flex-col gap-2">

            <span>{birthOrder.birthConflictWarning}</span>

            <button
              type="button"
              onClick={() => {
                if (!noMarriage && marriageId) {
                  birthOrder.openPanelByMarriage(
                    childId,
                    marriageId
                  );
                } else {
                  birthOrder.openPanelByChild(childId);
                }
              }}
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
              birthOrder.checkBeforeSave(id);
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
        {error && (
            <div className="text-red-600 mb-2 whitespace-pre-line">
              {error}
            </div>
          )}
        {birthOrder.showBirthOrderPanel && (
            <BirthOrderPanel
              birthOrderPanelRef={birthOrder.birthOrderPanelRef}
              birthOrderRows={birthOrder.birthOrderRows}
              setBirthOrderRows={birthOrder.setBirthOrderRows}
              saveBirthOrders={async () => {
                const result = await birthOrder.saveBirthOrders();
              
                if (result.ok) {
                  setSuccess(result.message);
                  setError("");
              
                  await handleSubmit(null, { skipBirthOrderCheck: true });
                } else {
                  setError(result.message);
                }
              }}
              setShowBirthOrderPanel={birthOrder.setShowBirthOrderPanel}
              setError={setError}
              displayName={displayName}
            />
          )}
        {/* ================================================= */}
        {/* BUTTONS */}
        {/* ================================================= */}
        <div className="flex gap-2 pt-4">

          <button
            type="button"
            onClick={() => {
              if (!noMarriage && marriageId) {
                birthOrder.openPanelByMarriage(childId, marriageId);
              } else {
                birthOrder.openPanelByChild(childId);
              }
            }}
            disabled={!childId || birthOrder.birthOrderLoading}
            className={`px-4 py-2 text-white rounded ${
              !childId || birthOrder.birthOrderLoading
                ? "bg-gray-300 cursor-not-allowed"
                : birthOrder.showBirthOrderPanel
                ? "bg-purple-600 hover:bg-purple-700"
                : "bg-gray-500 hover:bg-gray-600"
            }`}
          >
            {birthOrder.birthOrderLoading ? "⏳ Đang tải..." : "🔢 Birth Order"}
          </button>

          <button
            type="button"
            className="px-4 py-2 bg-gray-400 text-white rounded"
            onClick={() => {
              setParentId("");
              setType("");
              setMarriageId("");
              setNoMarriage(true);
              setError("");
              setSuccess("");
              setHasFather(false);
              setHasMother(false);
              setLockForm(false);
            }}
          >
            ❌ Hủy
          </button>
          <button
            type="button"
            onClick={() => {
              setChildId("");
              setParentId("");
              setType("");
              setMarriageId("");
              setNoMarriage(true);
              setError("");
              setSuccess("");
              setHasFather(false);
              setHasMother(false);
              setLockForm(false);
              birthOrder.setShowBirthOrderPanel(false);
            }}
            className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded"
          >
            ➕ Thêm
          </button> 
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
              {loading ? "⏳ Đang kiểm tra quyền..." : "💾 Lưu Gia Đình"}
            </button>
          )}

          {lockForm && (
            <button
              type="button"
              onClick={() => navigate("/")}
              className="px-4 py-2 bg-gray-600 text-white rounded"
            >
              🏠 Home
            </button>
          )}
        </div>
      </form >
    </div >
  );
}
export default AssignParentForm;
