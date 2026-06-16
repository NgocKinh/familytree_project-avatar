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

  const openPanel = async () => {
    console.log("OPEN PANEL CALLED");
    if (!childId) {
      setError("Không xác định được người con.");
      return;
    }
  
    const allowed = await checkNearAccessForBO();
  
    if (!allowed) {
      setCheckingAccess(false);
      return;
    }
  
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