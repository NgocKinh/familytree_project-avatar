import React from "react";

export default function BirthOrderPanel({
  birthOrderPanelRef,
  birthOrderRows,
  setBirthOrderRows,
  saveBirthOrders,
  setShowBirthOrderPanel,
  setError,
  displayName,
}) {
  return (
    <div
      ref={birthOrderPanelRef}
      className="mt-4 border rounded p-4 bg-gray-50"
    >
      <h3 className="font-bold mb-4">
        🔢 Sắp xếp thứ tự anh/chị/em
      </h3>

      <div className="space-y-2">
        {(birthOrderRows || []).map((p) => (
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

                setBirthOrderRows((rows) =>
                  rows.map((r) =>
                    r.id === p.id
                      ? {
                          ...r,
                          birth_order:
                            value === "" ? null : Number(value),
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
  );
}