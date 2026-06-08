import { useRef, useState } from "react";
import axios from "axios";
import { API_BASE_URL } from "../../api/apiConfig";

export default function useBirthOrder({ persons, getAuthConfig }) {
  const [birthConflictWarning, setBirthConflictWarning] = useState("");
  const [showBirthOrderPanel, setShowBirthOrderPanel] = useState(false);
  const [birthOrderRows, setBirthOrderRows] = useState([]);
  const [birthOrderLoading, setBirthOrderLoading] = useState(false);

  const birthOrderPanelRef = useRef(null);

  const getBirthYear = (birthDate) => {
    if (!birthDate) return null;
    return String(birthDate).slice(0, 4);
  };
  const sortBirthOrderRows = (rows) => {
    return [...rows].sort((a, b) => {
      const yearA = getBirthYear(a.birth_date) ?? 9999;
      const yearB = getBirthYear(b.birth_date) ?? 9999;
  
      if (yearA !== yearB) {
        return yearA - yearB;
      }
  
      const boA = a.birth_order ?? 9999;
      const boB = b.birth_order ?? 9999;
  
      return boA - boB;
    });
  };
  const findPerson = (personId) => {
    return persons.find((p) => String(p.id) === String(personId));
  };

  const scrollToPanel = () => {
    setTimeout(() => {
      birthOrderPanelRef.current?.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }, 100);
  };
  const analyzeRowsForBirthOrder = (rows) => {
    const hasMissingBirthYear = rows.some(
      (p) => !getBirthYear(p.birth_date)
    );
  
    const yearMap = {};
  
    rows.forEach((p) => {
      const year = getBirthYear(p.birth_date);
      if (!year) return;
  
      if (!yearMap[year]) {
        yearMap[year] = [];
      }
  
      yearMap[year].push(p);
    });
  
    const sameYearGroup = Object.values(yearMap).find(
      (group) => group.length >= 2
    );
  
    return {
      hasMissingBirthYear,
      sameYearGroup,
    };
  };
  const openPanelByChild = async (childId, { force = true } = {}) => {
    if (!childId) {
      return {
        opened: false,
        message: "❌ Vui lòng chọn Người Con trước khi cập nhật Birth Order.",
      };
    }

    setBirthOrderLoading(true);

    try {
      const res = await axios.get(
        `${API_BASE_URL}/parent_child/child/${childId}/siblings`,
        getAuthConfig()
      );

      const siblings = (res.data || []).map((p) => ({
        ...p,
        id: p.id ?? p.person_id,
      }));
      
      const childRes = await axios.get(
        `${API_BASE_URL}/person/${childId}`,
        getAuthConfig()
      );
      
      const child = {
        ...childRes.data,
        id: childRes.data.id ?? childRes.data.person_id,
      };

      if (!child) {
        return {
          opened: false,
          message: "❌ Không tìm thấy thông tin Người Con.",
        };
      }

      const rows = [child, ...siblings];

      if (rows.length <= 1) {
        return {
          opened: false,
          message: "ℹ️ Người con này chưa có anh/chị/em để sắp xếp Birth Order.",
        };
      }

      if (!force) {
        const childYear = getBirthYear(child.birth_date);
      
        const hasChildMissingBirthYear = !childYear;
      
        const hasSiblingMissingBirthYear = siblings.some(
          (p) => !getBirthYear(p.birth_date)
        );
      
        const sameYearSiblings = childYear
          ? siblings.filter(
              (p) => getBirthYear(p.birth_date) === childYear
            )
          : [];
      
        const shouldOpenBirthOrder =
          hasChildMissingBirthYear ||
          hasSiblingMissingBirthYear ||
          sameYearSiblings.length > 0;
      
        if (!shouldOpenBirthOrder) {
          setBirthConflictWarning("");
          return { opened: false };
        }

        setBirthOrderRows(sortBirthOrderRows(rows));
      
        if (hasChildMissingBirthYear) {
          setBirthConflictWarning(
            "⚠ Người con đang thêm chưa có năm sinh. Vui lòng cập nhật Birth Order để xác định thứ tự sinh."
          );
        } else if (hasSiblingMissingBirthYear) {
          setBirthConflictWarning(
            "⚠ Trong nhóm anh/chị/em có người chưa có năm sinh. Vui lòng cập nhật Birth Order để xác định thứ tự sinh."
          );
        } else {
          setBirthConflictWarning(
            "⚠ Người con đang thêm trùng năm sinh với anh/chị/em. Vui lòng cập nhật Birth Order để xác định thứ tự sinh."
          );
        }

      } else {
        setBirthOrderRows(sortBirthOrderRows(rows));
      }

      setShowBirthOrderPanel(true);
      scrollToPanel();

      return { opened: true };
    } catch (err) {
      console.error("Open BO panel error:", err);
      return {
        opened: false,
        message: "❌ Không thể mở Birth Order.",
      };
    } finally {
      setBirthOrderLoading(false);
    }
  };
  const openPanelByMarriage = async (
    childId,
    marriageId,
    { force = true } = {}
  ) => {
    if (!childId) {
      return {
        opened: false,
        message: "❌ Vui lòng chọn Người Con trước khi cập nhật Birth Order.",
      };
    }
  
    if (!marriageId) {
      return openPanelByChild(childId, { force });
    }
  
    setBirthOrderLoading(true);
  
    try {
      const childrenRes = await axios.get(
        `${API_BASE_URL}/parent_child/marriage/${marriageId}/children`,
        getAuthConfig()
      );
  
      const existingChildren = (childrenRes.data || []).map((p) => ({
        ...p,
        id: p.id ?? p.person_id,
      }));
  
      const childRes = await axios.get(
        `${API_BASE_URL}/person/${childId}`,
        getAuthConfig()
      );
  
      const child = {
        ...childRes.data,
        id: childRes.data.id ?? childRes.data.person_id,
      };
  
      const rowsMap = new Map();
  
      [child, ...existingChildren].forEach((p) => {
        const id = p.id ?? p.person_id;
        if (!id) return;
  
        rowsMap.set(String(id), {
          ...p,
          id,
        });
      });
  
      const rows = Array.from(rowsMap.values());
  
      if (rows.length <= 1) {
        return {
          opened: false,
          message: "ℹ️ Gia đình này chưa có anh/chị/em để sắp xếp Birth Order.",
        };
      }
  
      if (!force) {
        const childYear = getBirthYear(child.birth_date);
      
        const hasChildMissingBirthYear = !childYear;
      
        const hasSiblingMissingBirthYear = existingChildren.some(
          (p) => !getBirthYear(p.birth_date)
        );
      
        const sameYearSiblings = childYear
          ? existingChildren.filter(
              (p) => getBirthYear(p.birth_date) === childYear
            )
          : [];
      
        const shouldOpenBirthOrder =
          hasChildMissingBirthYear ||
          hasSiblingMissingBirthYear ||
          sameYearSiblings.length > 0;
      
        if (!shouldOpenBirthOrder) {
          setBirthConflictWarning("");
          return { opened: false };
        }
      
        setBirthOrderRows(sortBirthOrderRows(rows));
      
        if (hasChildMissingBirthYear) {
          setBirthConflictWarning(
            "⚠ Người con đang thêm chưa có năm sinh. Vui lòng cập nhật Birth Order để xác định thứ tự sinh."
          );
        } else if (hasSiblingMissingBirthYear) {
          setBirthConflictWarning(
            "⚠ Trong nhóm anh/chị/em có người chưa có năm sinh. Vui lòng cập nhật Birth Order để xác định thứ tự sinh."
          );
        } else {
          setBirthConflictWarning(
            "⚠ Người con đang thêm trùng năm sinh với anh/chị/em. Vui lòng cập nhật Birth Order để xác định thứ tự sinh."
          );
        }
      } else {
        setBirthOrderRows(sortBirthOrderRows(rows));
      }
  
      setShowBirthOrderPanel(true);
      scrollToPanel();
  
      return { opened: true };
    } catch (err) {
      console.error("Open BO panel by marriage error:", err);
  
      return {
        opened: false,
        message: "❌ Không thể mở Birth Order theo gia đình.",
      };
    } finally {
      setBirthOrderLoading(false);
    }
  };
  const checkBeforeSave = async (childId, marriageId = null) => {
    if (marriageId) {
      return openPanelByMarriage(childId, marriageId, { force: false });
    }
  
    return openPanelByChild(childId, { force: false });
  };

  const hasDuplicateBirthOrder = () => {
    const values = birthOrderRows
      .map((p) => p.birth_order)
      .filter((v) => v !== null && v !== undefined && v !== "");

    return new Set(values).size !== values.length;
  };

  const saveBirthOrders = async () => {
    if (hasDuplicateBirthOrder()) {
      return {
        ok: false,
        message:
          "❌ Birth Order không được trùng nhau trong cùng nhóm anh/chị/em.\nSửa BO hoặc chọn thao tác khác.",
      };
    }

    try {
      const payload = birthOrderRows.map((p) => ({
        person_id: p.id ?? p.person_id,
        birth_order:
          p.birth_order === "" || p.birth_order === null
            ? null
            : Number(p.birth_order),
      }));

      await axios.put(
        `${API_BASE_URL}/person/birth-order/bulk`,
        { items: payload },
        getAuthConfig()
      );

      setBirthConflictWarning("");
      setShowBirthOrderPanel(false);

      return {
        ok: true,
        message: "✅ Đã cập nhật Birth Order thành công.",
      };
    }catch (err) {
      console.error("❌ Save birth order error:", err);
    
      const detail = err?.response?.data?.detail;
    
      let message = "❌ Không thể cập nhật Birth Order.";
    
      if (typeof detail === "string") {
        message = detail;
      } else if (Array.isArray(detail)) {
        message = detail
          .map((item) => item?.msg || JSON.stringify(item))
          .join("\n");
      } else if (detail) {
        message = JSON.stringify(detail);
      }
    
      return {
        ok: false,
        message,
      };
    }
  };

  return {
    birthConflictWarning,
    showBirthOrderPanel,
    setShowBirthOrderPanel,
    birthOrderRows,
    setBirthOrderRows,
    birthOrderLoading,
    birthOrderPanelRef,
    openPanelByChild,
    openPanelByMarriage,
    checkBeforeSave,
    saveBirthOrders,
  };
}