import React, { useEffect, useRef, useState } from "react";
import axios from "axios";
import { API_BASE_URL } from "../../api/apiConfig";
import PersonDropdown from "../common/PersonDropdown";
import MarriageDropdown from "../common/MarriageDropdown";
import { formatName } from "../../utils/formatName";
import { handleAuthError } from "../../utils/authErrorHandler";
import { useNavigate } from "react-router-dom";
import useBirthOrder from "../birth_order/useBirthOrder";
import { makeApiUrl } from "../../api/apiConfig";
function AssignChildToParentForm() {

  const navigate = useNavigate();

  const getAuthConfig = () => {
    const token = localStorage.getItem("token");

    return {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    };
  };

  // -----------------------------
  // DATA LISTS
  // -----------------------------
  const [persons, setPersons] = useState([]);
  const [marriages, setMarriages] = useState([]);
  const displayName = (name = "") => name.replaceAll("|", " ");
  // -----------------------------
  // FORM STATE
  // -----------------------------
  const [noMarriage, setNoMarriage] = useState(true);
  const [marriageId, setMarriageId] = useState("");

  const [parentId, setParentId] = useState("");
  const [type, setType] = useState("");
  const [childId, setChildId] = useState("");

  // -----------------------------
  // UI STATE
  // -----------------------------
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [hasFather, setHasFather] = useState(false);
  const [hasMother, setHasMother] = useState(false);
  const [lockForm, setLockForm] = useState(false);
  const [loading, setLoading] = useState(false);
  useEffect(() => {
    if (childId) {
      checkParentStatus(childId, noMarriage);
    }
  }, [childId, noMarriage]);
  const birthOrder = useBirthOrder({
    persons,
    getAuthConfig,
  });
  useEffect(() => {
    axios.get(`${API_BASE_URL}/person`)
      .then(res => {
        const data = res.data || [];

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
  const checkParentStatus = async (childId, currentNoMarriage = noMarriage) => {
    try {
      const res = await fetch(
        makeApiUrl(`/parent_child/child/${childId}/parents-status`)
      );
  
      const data = await res.json();
  
      const fatherExists = !!data.father;
      const motherExists = !!data.mother;

      setHasFather(fatherExists);
      setHasMother(motherExists);
  
      // CASE 1: ĐANG CHỌN GIA ĐÌNH
      // Vì chọn gia đình nghĩa là sẽ thêm cả Cha + Mẹ
      if (!currentNoMarriage) {
        if (fatherExists && motherExists) {
          setLockForm(true);
          setError("Người con này đã có đủ Cha và Mẹ.");
          return;
        }
  
        if (fatherExists) {
          setLockForm(true);
          setError("Người con này đã có Cha. Vui lòng chuyển sang chế độ 'Không thuộc gia đình nào' để bổ sung Mẹ.");
          return;
        }
  
        if (motherExists) {
          setLockForm(true);
          setError("Người con này đã có Mẹ. Vui lòng chuyển sang chế độ 'Không thuộc gia đình nào' để bổ sung Cha.");
          return;
        }
  
        setLockForm(false);
        setError("");
        return;
      }
  
      // CASE 2: KHÔNG THUỘC GIA ĐÌNH
      if (fatherExists && motherExists) {
        setLockForm(true);
        setError("Người con này đã có đủ Cha và Mẹ.");
        return;
      }
  
      setLockForm(false);
  
      if (fatherExists && type === "father") {
        setType("");
        setParentId("");
        setError("Người con này đã có Cha. Vui lòng chọn Mẹ.");
        return;
      }
  
      if (motherExists && type === "mother") {
        setType("");
        setParentId("");
        setError("Người con này đã có Mẹ. Vui lòng chọn Cha.");
        return;
      }
  
      setError("");
    } catch (err) {
      setError("Không kiểm tra được trạng thái Cha/Mẹ của người con.");
    }
  };

  const handleSubmit = async (e, options = {}) => {
    if (e) e.preventDefault();
  
    const { skipBirthOrderCheck = false } = options;
  
    setLoading(true);
  
    setError("");
    setSuccess("");
  
    if (!childId) {
      setError("❌ Chưa chọn người con.");
      setLoading(false);
      return;
    }
    
    try {
      // ===============================
      // CASE 1: KHÔNG CÓ HÔN NHÂN
      // ===============================
      if (noMarriage) {
        if (hasFather && hasMother) {
          setError("❌ Người con này đã có đủ Cha và Mẹ.");
          return;
        }
        
        if (hasFather && !hasMother && type !== "mother") {
          setError("❌ Người con này đã có Cha. Vui lòng chọn vai trò Mẹ và chọn tên Mẹ cần bổ sung.");
          return;
        }
        
        if (!hasFather && hasMother && type !== "father") {
          setError("❌ Người con này đã có Mẹ. Vui lòng chọn vai trò Cha và chọn tên Cha cần bổ sung.");
          return;
        }
        
        if (!parentId) {
          setError("❌ Vui lòng chọn tên Cha/Mẹ cần bổ sung.");
          return;
        }
        if (!skipBirthOrderCheck) {
          const boResult = await birthOrder.checkBeforeSave(childId, null);
        
          if (boResult.opened) {
            navigate(`/birth-order/${childId}/0`, {
              state: {
                source: "AC",
                mode: "single_parent",
                childId,
                parentId,
                type,
              },
            });
        
            return;
          }
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
        const m = marriages.find(
          (x) => String(x.id) === String(marriageId)
        );

        if (!m) {
          setError("❌ Không tìm thấy hôn nhân.");
          return;
        }
        if (hasFather && hasMother) {
          setError("❌ Người con này đã có đủ Cha và Mẹ. Không thể thêm vào gia đình khác.");
          return;
        }
        
        if (hasFather && !hasMother) {
          setError('❌ Người con này đã có Cha. Vui lòng chọn "Không thuộc gia đình nào", chọn vai trò Mẹ và chọn tên Mẹ cần bổ sung.');
          return;
        }
        
        if (!hasFather && hasMother) {
          setError('❌ Người con này đã có Mẹ. Vui lòng chọn "Không thuộc gia đình nào", chọn vai trò Cha và chọn tên Cha cần bổ sung.');
          return;
        }
        if (!skipBirthOrderCheck) {
          const boResult = await birthOrder.checkBeforeSave(childId, marriageId);
        
          if (boResult.opened) {
            navigate(`/birth-order/${childId}/${marriageId}`, {
              state: {
                source: "AC",
                mode: "marriage",
                childId,
                marriageId,
              },
            });
        
            return;
          }
        }
        await axios.post(
          `${API_BASE_URL}/parent_child/assign`,
          {
            child_id: Number(childId),
            parent_id: m.spouse_a_id,
            type: "father",
          },
          getAuthConfig()
        );
        
        await axios.post(
          `${API_BASE_URL}/parent_child/assign`,
          {
            child_id: Number(childId),
            parent_id: m.spouse_b_id,
            type: "mother",
          },
          getAuthConfig()
        );
      }

      setSuccess("✅ Đã bổ sung quan hệ Cha/Mẹ & Con thành công.");
      setLockForm(true);
    } catch (err) {
      if (handleAuthError(err)) {
        return;
      }
      console.error(
        "❌ ASSIGN CHILD ERROR:",
        err.response?.data || err
      );
    
      const data = err.response?.data;

      setError(
        data?.message ||
        data?.detail?.message ||
        data?.detail ||
        data?.warning ||
        data?.error ||
        "❌ Không thể bổ sung người con vào gia đình. Vui lòng kiểm tra lại dữ liệu và thử lại."
      );
    }
    finally {
      setLoading(false);
    }
  };
  return (
    <div className="max-w-xl mx-auto p-4 bg-white shadow rounded">
      <h3 className="text-xl font-bold text-blue-700 mb-4 text-center">
        👨‍👩‍👧 Quan Hệ Cha/Mẹ & Con
      </h3>

        <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block font-semibold">
            1️⃣ Thuộc gia đình?
          </label>

          <label className="block mb-2">
            <input
              type="checkbox"
              checked={noMarriage}
              disabled={lockForm}
              onChange={() => {
                setNoMarriage(!noMarriage);
                setMarriageId("");
                setParentId("");
                setType("");
                setError("");
                setSuccess("");
              }}
            />{" "}
            Không thuộc gia đình nào
          </label>

          {!noMarriage && (
            <MarriageDropdown
              value={marriageId}
              onChange={(id) => {
                setMarriageId(id);
              
                setError("");
                setSuccess("");
              }}
              marriages={marriages}
              placeholder="-- Gõ tên hoặc kéo xuống chọn Cha & Mẹ --"
              disabled={lockForm}
            />
          )}
        </div>

        {noMarriage && (
          <div>
            <label className="block font-semibold">
              2️⃣ Vai trò (bắt buộc)
            </label>

            <div className="flex gap-6 mb-3">
              <label>
                <input
                  type="radio"
                  value="father"
                  checked={type === "father"}
                  onChange={() => {
                    setType("father");
                    setParentId("");
                    setError("");
                    setSuccess("");
                  }}
                  disabled={lockForm || hasFather}
                />{" "}
                Cha
              </label>

              <label>
                <input
                  type="radio"
                  value="mother"
                  checked={type === "mother"}
                  onChange={() => {
                    setType("mother");
                    setParentId("");
                    setError("");
                    setSuccess("");
                  }}
                  disabled={lockForm || hasMother}
                />{" "}
                Mẹ
              </label>
            </div>

            <label className="block font-semibold">
              3️⃣ Chọn Cha / Mẹ
            </label>

            <PersonDropdown
              label={null}
              value={parentId}
              onChange={(id) => {
                setParentId(id);
                setError("");
                setSuccess("");
              }}
              persons={persons}
              disabled={lockForm || !type}
              filterFn={(p) => {
                if (type === "father") return p.gender === "male";
                if (type === "mother") return p.gender === "female";
                return false;
              }}
              placeholder={
                type === "father"
                  ? "-- Gõ tên hoặc kéo xuống chọn Cha --"
                  : type === "mother"
                    ? "-- Gõ tên hoặc kéo xuống chọn Mẹ --"
                    : "-- Chọn vai trò Cha/Mẹ trước --"
              }
            />
          </div>
        )}

        <div>
        <label className="block font-semibold">
        4️⃣ Chọn Người Con
        </label>

          <PersonDropdown
            value={childId}
            onChange={(id) => {
              setChildId(id);
            
              setError("");
              setSuccess("");
            }}
            persons={persons}
            disabled={lockForm}
            placeholder="-- Gõ tên hoặc kéo xuống chọn người con --"
          />
        </div>
          
        {error && (
          <div className="mt-3 p-3 bg-red-50 border border-red-300 text-red-700 rounded">
            {error}
          </div>
        )}

        {success && (
          <div className="mt-3 p-3 bg-green-50 border border-green-300 text-green-700 rounded">
            {success}
          </div>
        )}

        <div className="flex items-center justify-between pt-4">

          <div className="flex gap-2 pt-4">
            <button
              type="button"
              className="px-4 py-2 bg-gray-400 text-white rounded"
              onClick={async () => {
                setParentId("");
                setType("");
                setMarriageId("");
                setNoMarriage(true);
                setError("");
                setSuccess("");

                if (childId) {
                  await checkParentStatus(childId);
                } else {
                  setHasFather(false);
                  setHasMother(false);
                  setLockForm(false);
                }
              }}
            >
              ❌ Hủy
            </button>
            {!lockForm && (
              <button
                type="submit"
                disabled={
                  loading ||
                  !childId ||
                  (!noMarriage && !marriageId) ||
                  (noMarriage && (!parentId || !type)) ||
                  (!noMarriage && (hasFather || hasMother)) ||
                  (noMarriage && type === "father" && hasFather) ||
                  (noMarriage && type === "mother" && hasMother)
                }
                className={`px-4 py-2 text-white rounded ${
                  loading ||
                  !childId ||
                  (!noMarriage && !marriageId) ||
                  (noMarriage && (!parentId || !type)) ||
                  (!noMarriage && (hasFather || hasMother)) ||
                  (noMarriage && type === "father" && hasFather) ||
                  (noMarriage && type === "mother" && hasMother)
                    ? "bg-blue-300 cursor-not-allowed"
                    : "bg-blue-600 hover:bg-blue-700"
                }`}
              >
                {loading ? "⏳ Đang kiểm tra quyền..." : "💾 Lưu Gia Đình"}
              </button>
            )}

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
              }}
              className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded"
            >
              ➕ Thêm mới
            </button>

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

          </div>
      </form>
    </div>
  );
}

export default AssignChildToParentForm;