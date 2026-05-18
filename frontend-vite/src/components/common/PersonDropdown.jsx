import React from "react";
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
    const list = filterFn ? persons.filter(filterFn) : persons;

    const sortedPersons = [...list].sort((a, b) => {
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

    return (
        <div>
            {label && (
                <label className="block font-medium text-gray-700 mb-1">
                    {label}
                </label>
            )}

            <select
                value={value}
                onChange={(e) => onChange(e.target.value)}
                disabled={disabled}
                className="w-full border rounded-lg p-2"
            >
                <option value="">{placeholder}</option>

                {sortedPersons.map((p) => {
                    const personId = p.person_id ?? p.id;
                    const birthYear = p.birth_date
                        ? new Date(p.birth_date).getFullYear()
                        : "";

                    const display = `${formatName(p)}${birthYear ? ` (${birthYear})` : ""}`;

                    return (
                        <option
                            key={`${personId}-${formatName(p) || "noname"}`}
                            value={personId}
                        >
                            {display}
                        </option>
                    );
                })}
            </select>
        </div>
    );
}