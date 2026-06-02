import React, { useEffect, useMemo, useRef, useState } from "react";
import { formatName } from "../../utils/formatName";
export default function PersonDropdown({
    label,
    value,
    onChange,
    persons = [],
    placeholder = "-- Chọn --",
    filterFn = null,
    disabled = false,
}) {
    const [open, setOpen] = useState(false);
    const [search, setSearch] = useState("");
    const wrapperRef = useRef(null);
    const selectedRef = useRef(null);

    const sortedPersons = useMemo(() => {
        const list = filterFn ? persons.filter(filterFn) : persons;

        return [...list].sort((a, b) => {
            const nameA = formatName(a).toString();
            const nameB = formatName(b).toString();

            if (!a.birth_date && !b.birth_date) {
                return nameA.localeCompare(nameB, "vi");
            }

            if (!a.birth_date) return 1;
            if (!b.birth_date) return -1;

            if (a.birth_date !== b.birth_date) {
                return new Date(b.birth_date) - new Date(a.birth_date);
            }

            return nameA.localeCompare(nameB, "vi");
        });
    }, [persons, filterFn]);

    const selectedPerson = sortedPersons.find(
        (p) => String(p.person_id ?? p.id) === String(value)
    );

    const getDisplay = (p) => {
        if (!p) return "";
        const birthYear = p.birth_date
            ? new Date(p.birth_date).getFullYear()
            : "";

        return `${formatName(p)}${birthYear ? ` (${birthYear})` : ""}`;
    };

    const filteredPersons = sortedPersons.filter((p) =>
        getDisplay(p).toLowerCase().includes(search.toLowerCase())
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

    useEffect(() => {
        if (open && selectedRef.current) {
            selectedRef.current.scrollIntoView({
                block: "center",
            });
        }
    }, [open]);

    return (
        <div className="relative" ref={wrapperRef}>
            {label && (
                <label className="block font-medium text-gray-700 mb-1">
                    {label}
                </label>
            )}

            <div className="relative">
                <input
                    type="text"
                    disabled={disabled}
                    value={open ? search : getDisplay(selectedPerson)}
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
                    {filteredPersons.length === 0 ? (
                        <div className="p-3 text-red-500 text-sm">
                            Không tìm thấy người phù hợp
                        </div>
                    ) : (
                        filteredPersons.map((p) => {
                            const personId = p.person_id ?? p.id;
                            const isSelected = String(personId) === String(value);

                            return (
                                <button
                                    key={`${personId}-${formatName(p) || "noname"}`}
                                    ref={isSelected ? selectedRef : null}
                                    type="button"
                                    onClick={() => {
                                        onChange(String(personId));
                                        setSearch("");
                                        setOpen(false);
                                    }}
                                    className={`w-full text-left px-3 py-2 hover:bg-indigo-50 ${
                                        isSelected
                                            ? "bg-indigo-100 font-semibold text-indigo-700"
                                            : "text-gray-800"
                                    }`}
                                >
                                    {getDisplay(p)}
                                </button>
                            );
                        })
                    )}
                </div>
            )}
        </div>
    );
}
