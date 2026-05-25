import React, { useEffect, useRef, useState } from "react";

export default function MarriageDropdown({
  value,
  onChange,
  marriages = [],
  placeholder = "-- chọn Cha & Mẹ --",
  disabled = false,
}) {
  const [open, setOpen] = useState(false);
  const [search, setSearch] = useState("");
  const wrapperRef = useRef(null);

  const displayName = (name = "") => name.replaceAll("|", " ");

  const getDisplay = (m) =>
    `#${m.id} – ${displayName(m.spouse_a_name)} & ${displayName(m.spouse_b_name)}`;

  const selectedMarriage = marriages.find(
    (m) => String(m.id) === String(value)
  );

  const filteredMarriages = marriages.filter((m) =>
    getDisplay(m).toLowerCase().includes(search.toLowerCase())
  );

  useEffect(() => {
    function handleClickOutside(e) {
      if (wrapperRef.current && !wrapperRef.current.contains(e.target)) {
        setOpen(false);
      }
    }

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div className="relative" ref={wrapperRef}>
      <div className="relative">
        <input
          type="text"
          disabled={disabled}
          value={open ? search : selectedMarriage ? getDisplay(selectedMarriage) : ""}
          placeholder={placeholder}
          onFocus={() => {
            setSearch("");
            setOpen(true);
          }}
          onChange={(e) => {
            setSearch(e.target.value);
            setOpen(true);
          }}
          className="w-full border rounded-lg p-2 pr-16 bg-white"
        />

        {value && !disabled && (
          <button
            type="button"
            onClick={() => {
              onChange("");
              setSearch("");
              setOpen(false);
            }}
            className="absolute right-9 top-1/2 -translate-y-1/2 text-gray-400 hover:text-red-500"
          >
            ×
          </button>
        )}

        <button
          type="button"
          disabled={disabled}
          onClick={() => {
            setSearch("");
            setOpen((prev) => !prev);
          }}
          className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-500"
        >
          ▾
        </button>
      </div>

      {open && !disabled && (
        <div className="absolute z-50 mt-1 w-full max-h-64 overflow-y-auto rounded-lg border bg-white shadow-lg">
          {filteredMarriages.length === 0 ? (
            <div className="p-3 text-gray-500 text-sm">
              Không tìm thấy gia đình phù hợp
            </div>
          ) : (
            filteredMarriages.map((m) => {
              const isSelected = String(m.id) === String(value);

              return (
                <button
                  key={m.id}
                  type="button"
                  onClick={() => {
                    onChange(String(m.id));
                    setSearch("");
                    setOpen(false);
                  }}
                  className={`w-full text-left px-3 py-2 hover:bg-indigo-50 ${
                    isSelected
                      ? "bg-indigo-100 font-semibold text-indigo-700"
                      : "text-gray-800"
                  }`}
                >
                  {getDisplay(m)}
                </button>
              );
            })
          )}
        </div>
      )}
    </div>
  );
}