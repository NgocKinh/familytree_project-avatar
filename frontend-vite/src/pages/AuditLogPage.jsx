import React, { useEffect, useState } from "react";
import axios from "axios";

import { API_BASE_URL } from "../api/apiConfig";

const PAGE_SIZE = 20;

const EMPTY_FILTERS = {
  username: "",
  action: "",
  entity_type: "",
  entity_id: "",
};

const formatDateTimeVN = (value) => {
  if (!value) return "";

  const utcValue = value.endsWith("Z") ? value : `${value}Z`;

  return new Intl.DateTimeFormat("vi-VN", {
    dateStyle: "short",
    timeStyle: "medium",
    timeZone: "Asia/Ho_Chi_Minh",
  }).format(new Date(utcValue));
};

const actionClass = (action) => {
  if (action.includes("DELETE")) {
    return "bg-red-100 text-red-700";
  }

  if (action === "CREATE" || action === "RESTORE") {
    return "bg-green-100 text-green-700";
  }

  return "bg-blue-100 text-blue-700";
};

export default function AuditLogPage() {
  const [items, setItems] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);

  const [filters, setFilters] = useState(EMPTY_FILTERS);
  const [appliedFilters, setAppliedFilters] = useState(EMPTY_FILTERS);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const totalPages = Math.max(1, Math.ceil(total / PAGE_SIZE));

  useEffect(() => {
    let cancelled = false;

    const loadAuditLogs = async () => {
      setLoading(true);
      setError("");

      try {
        const params = {
          page,
          page_size: PAGE_SIZE,
        };

        Object.entries(appliedFilters).forEach(([key, value]) => {
          if (value !== "") {
            params[key] = value;
          }
        });

        const response = await axios.get(
          `${API_BASE_URL}/audit-logs`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
            params,
          }
        );

        if (!cancelled) {
          setItems(response.data.items || []);
          setTotal(response.data.total || 0);
        }
      } catch (err) {
        if (!cancelled) {
          setError(
            err?.response?.data?.detail ||
              "Không tải được Audit Log."
          );
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    };

    loadAuditLogs();

    return () => {
      cancelled = true;
    };
  }, [page, appliedFilters]);

  const updateFilter = (key, value) => {
    setFilters((current) => ({
      ...current,
      [key]: value,
    }));
  };

  const handleSearch = (event) => {
    event.preventDefault();
    setPage(1);
    setAppliedFilters({ ...filters });
  };

  const handleClear = () => {
    setFilters(EMPTY_FILTERS);
    setAppliedFilters(EMPTY_FILTERS);
    setPage(1);
  };

  return (
    <div className="mx-auto max-w-7xl">
      <div className="mb-5">
        <h1 className="text-2xl md:text-3xl font-bold text-gray-800">
          📋 Audit Log
        </h1>

        <p className="mt-1 text-sm md:text-base text-gray-600">
          Theo dõi các thao tác thay đổi dữ liệu trong FamilyTree.
        </p>
      </div>

      <form
        onSubmit={handleSearch}
        className="mb-5 grid grid-cols-1 gap-3 rounded-xl border bg-white p-4 shadow-sm sm:grid-cols-2 lg:grid-cols-5"
      >
        <input
          type="text"
          value={filters.username}
          onChange={(event) =>
            updateFilter("username", event.target.value)
          }
          placeholder="Tài khoản thao tác"
          className="rounded-lg border px-3 py-2"
        />

        <select
          value={filters.action}
          onChange={(event) =>
            updateFilter("action", event.target.value)
          }
          className="rounded-lg border px-3 py-2"
        >
          <option value="">Tất cả hành động</option>
          <option value="CREATE">CREATE</option>
          <option value="UPDATE">UPDATE</option>
          <option value="DELETE">DELETE</option>
          <option value="SOFT_DELETE">SOFT_DELETE</option>
          <option value="RESTORE">RESTORE</option>
          <option value="HARD_DELETE">HARD_DELETE</option>
          <option value="PRIORITY_UPDATE">PRIORITY_UPDATE</option>
          <option value="BIRTH_ORDER_UPDATE">
            BIRTH_ORDER_UPDATE
          </option>
        </select>

        <select
          value={filters.entity_type}
          onChange={(event) =>
            updateFilter("entity_type", event.target.value)
          }
          className="rounded-lg border px-3 py-2"
        >
          <option value="">Tất cả loại dữ liệu</option>
          <option value="person">Thành viên</option>
          <option value="parent_child">Cha–Con</option>
          <option value="marriage">Hôn nhân</option>
        </select>

        <input
          type="number"
          min="1"
          value={filters.entity_id}
          onChange={(event) =>
            updateFilter("entity_id", event.target.value)
          }
          placeholder="Mã ID hiển thị"
          className="rounded-lg border px-3 py-2"
        />

        <div className="flex gap-2">
          <button
            type="submit"
            className="flex-1 rounded-lg bg-blue-600 px-4 py-2 font-semibold text-white hover:bg-blue-700"
          >
            🔍 Tìm
          </button>

          <button
            type="button"
            onClick={handleClear}
            className="rounded-lg bg-gray-200 px-4 py-2 font-semibold text-gray-700 hover:bg-gray-300"
          >
            Xóa lọc
          </button>
        </div>
      </form>

      <div className="mb-3 flex items-center justify-between">
        <p className="font-semibold text-gray-700">
          Tổng số: {total}
        </p>

        <p className="text-sm text-gray-500">
          Trang {page}/{totalPages}
        </p>
      </div>

      {loading ? (
        <div className="rounded-xl border bg-white p-8 text-center">
          Đang tải Audit Log...
        </div>
      ) : error ? (
        <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-red-700">
          {error}
        </div>
      ) : items.length === 0 ? (
        <div className="rounded-xl border bg-white p-8 text-center text-gray-500">
          Không có Audit Log phù hợp.
        </div>
      ) : (
        <>
          {/* Mobile */}
          <div className="space-y-3 md:hidden">
            {items.map((item) => (
              <article
                key={item.id}
                className="rounded-xl border bg-white p-4 shadow-sm"
              >
                <div className="flex items-start justify-between gap-3">
                  <span className="font-bold text-gray-700">
                    #{item.id}
                  </span>

                  <span
                    className={`rounded-full px-2 py-1 text-xs font-bold ${actionClass(
                      item.action
                    )}`}
                  >
                    {item.action}
                  </span>
                </div>

                <p className="mt-2 text-sm text-gray-500">
                  {formatDateTimeVN(item.created_at)}
                </p>

                <p className="mt-2 font-semibold text-gray-800">
                  {item.username} ({item.role})
                </p>

                <p className="mt-1 text-sm text-gray-600">
                  {item.entity_type} · ID {item.entity_id ?? "—"}
                </p>

                <p className="mt-3 text-sm leading-relaxed text-gray-800">
                  {item.description || "Không có mô tả"}
                </p>
              </article>
            ))}
          </div>

          {/* Desktop */}
          <div className="hidden overflow-x-auto rounded-xl border bg-white shadow-sm md:block">
            <table className="min-w-full text-sm">
              <thead className="bg-gray-100 text-gray-700">
                <tr>
                  <th className="border-b px-3 py-3 text-left">ID</th>
                  <th className="border-b px-3 py-3 text-left">Thời gian</th>
                  <th className="border-b px-3 py-3 text-left">Tài khoản</th>
                  <th className="border-b px-3 py-3 text-left">Vai trò</th>
                  <th className="border-b px-3 py-3 text-left">Hành động</th>
                  <th className="border-b px-3 py-3 text-left">Loại</th>
                  <th className="border-b px-3 py-3 text-left">
                    Mã ID hiển thị
                  </th>
                  <th className="border-b px-3 py-3 text-left">Mô tả</th>
                </tr>
              </thead>

              <tbody>
                {items.map((item) => (
                  <tr key={item.id} className="hover:bg-gray-50">
                    <td className="border-b px-3 py-3">{item.id}</td>
                    <td className="whitespace-nowrap border-b px-3 py-3">
                      {formatDateTimeVN(item.created_at)}
                    </td>
                    <td className="border-b px-3 py-3 font-semibold">
                      {item.username}
                    </td>
                    <td className="border-b px-3 py-3">{item.role}</td>
                    <td className="border-b px-3 py-3">
                      <span
                        className={`rounded-full px-2 py-1 text-xs font-bold ${actionClass(
                          item.action
                        )}`}
                      >
                        {item.action}
                      </span>
                    </td>
                    <td className="border-b px-3 py-3">
                      {item.entity_type}
                    </td>
                    <td className="border-b px-3 py-3">
                      {item.entity_id ?? "—"}
                    </td>
                    <td className="min-w-72 border-b px-3 py-3">
                      {item.description || "Không có mô tả"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}

      <div className="mt-5 flex items-center justify-center gap-3">
        <button
          type="button"
          disabled={page <= 1}
          onClick={() => setPage((current) => current - 1)}
          className="rounded-lg bg-gray-200 px-4 py-2 font-semibold disabled:cursor-not-allowed disabled:opacity-50"
        >
          ← Trang trước
        </button>

        <button
          type="button"
          disabled={page >= totalPages}
          onClick={() => setPage((current) => current + 1)}
          className="rounded-lg bg-gray-200 px-4 py-2 font-semibold disabled:cursor-not-allowed disabled:opacity-50"
        >
          Trang sau →
        </button>
      </div>
    </div>
  );
}