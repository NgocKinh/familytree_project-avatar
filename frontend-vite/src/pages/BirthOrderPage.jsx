import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { API_BASE_URL } from "../api/apiConfig";
import BirthOrderPanel from "../components/birth_order/BirthOrderPanel";
import useBirthOrder from "../components/birth_order/useBirthOrder";

export default function BirthOrderPage() {
  const { childId } = useParams();
  const navigate = useNavigate();
  const [checkingAccess, setCheckingAccess] = useState(true);
  const [error, setError] = useState("");
  const [parents, setParents] = useState(null);
  const getAuthConfig = () => {
    const token = localStorage.getItem("token");
    return {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    };
  };
  const checkNearAccessForBO = async () => {
    try {
      const token = localStorage.getItem("token");
  
      const res = await fetch(`${API_BASE_URL}/auth/check-near-access`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          target_person_id: Number(childId),
          action: "birth_order:update",
        }),
      });
  
      const result = await res.json();

      if (!res.ok || result.allowed === false) {
        setError(
          result?.detail ||
            result?.reason ||
            "Bạn không có quyền sắp xếp thứ tự anh/chị/em trong gia đình này."
        );
        return false;
      }
  
      return true;
    } catch (err) {
      setError("Không kiểm tra được quyền truy cập.");
      return false;
    }
  };

  const birthOrder = useBirthOrder({
    persons: [],
    getAuthConfig,
  });

  const loadParents = async () => {
    try {
      const res = await fetch(
        `${API_BASE_URL}/parent_child/child/${childId}/parents-status`,
        getAuthConfig()
      );
  
      const data = await res.json();
      setParents(data);
    } catch (err) {
      setParents(null);
    }
  };

  const openPanel = async () => {
    if (!childId) {
      setError("Không xác định được người con.");
      return;
    }
  
    const allowed = await checkNearAccessForBO();
  
    if (!allowed) {
      setCheckingAccess(false);
      return;
    }
    await loadParents();
    await birthOrder.openPanelByChild(childId);
    setCheckingAccess(false);
  };
  useEffect(() => {
    openPanel();
  }, [childId]);
  return (
    <div className="max-w-4xl mx-auto p-4 bg-white shadow rounded">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold text-blue-700">
          👨‍👩‍👧‍👦 Sắp xếp thứ tự anh/chị/em
        </h2>

        <button
          type="button"
          onClick={() => navigate(-1)}
          className="px-4 py-2 bg-gray-600 text-white rounded"
        >
          ⬅️ Quay lại
        </button>
      </div>
      {parents && (
        <div className="mb-4 p-3 border rounded bg-gray-50 text-gray-700">
          <div className="font-semibold mb-1">Gia đình:</div>
          <div>Cha: {parents.father?.name || parents.father_name || "Chưa có"}</div>
          <div>Mẹ: {parents.mother?.name || parents.mother_name || "Chưa có"}</div>
        </div>
      )}
      {checkingAccess && (
        <p className="text-blue-600 mb-4">
          ⏳ Đang kiểm tra quyền truy cập...
        </p>
      )}

      {error && (
        <div className="mb-4 text-red-600 font-semibold">
          ❌ {error}
        </div>
      )}

      {birthOrder.showBirthOrderPanel &&
        Array.isArray(birthOrder.birthOrderRows) && (
          <BirthOrderPanel
            birthOrderPanelRef={birthOrder.birthOrderPanelRef}
            birthOrderRows={birthOrder.birthOrderRows}
            setBirthOrderRows={birthOrder.setBirthOrderRows}
            saveBirthOrders={async () => {
              const result = await birthOrder.saveBirthOrders();

              if (!result.ok) {
                alert(result.message || "Không lưu được BO.");
                return;
              }

              alert("✅ Đã lưu thứ tự anh/chị/em.");
              birthOrder.setShowBirthOrderPanel(false);
            }}
            setShowBirthOrderPanel={birthOrder.setShowBirthOrderPanel}
            setError={(msg) => alert(msg)}
            displayName={(name = "") => name.replaceAll("|", " ")}
          />
        )}
    </div>
  );
}