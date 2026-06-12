import React, { useEffect, useState } from "react";
import {
    getUsers,
    createUser,
    updateUser,
    lockUser,
    unlockUser,
    resetPassword,
} from "../api/userApi";
import axios from "axios";
import { API_BASE_URL } from "../api/apiConfig";
import PersonDropdown from "../components/common/PersonDropdown";
import { formatName } from "../utils/formatName";
import { handleAuthError } from "../utils/authErrorHandler";
import AdminHeader from "../components/admin/AdminHeader";
const ROLES = [
    { value: "viewer", label: "👁 Người xem" },
    { value: "member_basic", label: "👤 Thành viên" },
    { value: "co_operator", label: "🛠 Cộng tác viên" },
    { value: "admin", label: "⚙ Quản trị viên" },
];

export default function AdminUsersPage({ currentUser }) {
    const [users, setUsers] = useState([]);
    const [persons, setPersons] = useState([]);
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState("");
    const [error, setError] = useState("");

    const [form, setForm] = useState({
        username: "",
        password: "",
        full_name: "",
        role: "",
        person_id: "",
        is_active: true,
    });

    async function loadUsers() {
        setLoading(true);
        setError("");

        try {
            const data = await getUsers();
            setUsers(data);
        } catch (err) {
            if (handleAuthError(err)) {
                return;
              }
            setError(err.message || "Không tải được danh sách tài khoản");
        } finally {
            setLoading(false);
        }
    }
    async function loadPersons() {
        try {
            const res = await axios.get(`${API_BASE_URL}/person`);

            const data = res.data || [];

            const normalized = data.map((p) => ({
                ...p,
                name: formatName(p),
            }));

            setPersons(normalized);
        } catch (err) {
            if (handleAuthError(err)) {
                return;
              }
            console.error("Không tải được danh sách thành viên:", err);
            setPersons([]);
        }
    }
    useEffect(() => {
        loadUsers();
        loadPersons();
    }, []);

    function handleChange(e) {
        const { name, value, type, checked } = e.target;

        setForm((prev) => ({
            ...prev,
            [name]: type === "checkbox" ? checked : value,
        }));
    }

    async function handleCreate(e) {
        e.preventDefault();
        setMessage("");
        setError("");

        try {
            await createUser({
                ...form,
                person_id: form.person_id ? Number(form.person_id) : null,
            });

            setMessage("✅ Tạo tài khoản thành công");

            setForm({
                username: "",
                password: "",
                full_name: "",
                role: "",
                person_id: "",
                is_active: true,
            });

            await loadUsers();
        } catch (err) {
            if (handleAuthError(err)) {
                return;
              }
            setError(err.message || "Không tạo được tài khoản");
        }
    }

    async function handleRoleChange(user, newRole) {
        setMessage("");
        setError("");

        try {
            await updateUser(user.id, { role: newRole });
            setMessage("✅ Cập nhật vai trò thành công");
            await loadUsers();
        } catch (err) {
            if (handleAuthError(err)) {
                return;
              }
            setError(err.message || "Không cập nhật vai trò");
        }
    }

    async function handleToggleActive(user) {
        setMessage("");
        setError("");

        try {
            if (user.is_active) {
                await lockUser(user.id);
                setMessage("✅ Đã khóa tài khoản.");
            } else {
                await unlockUser(user.id);
                setMessage("✅ Đã mở khóa tài khoản.");
            }

            await loadUsers();
        } catch (err) {
            if (handleAuthError(err)) {
                return;
              }
            setError(err.message || "❌ Không thể thay đổi trạng thái khóa/mở khóa tài khoản.");
        }
    }

    async function handleResetPassword(user) {
        const newPassword = window.prompt(
            `Nhập password mới cho tài khoản: ${user.username}`
        );

        if (!newPassword) return;

        setMessage("");
        setError("");

        try {
            await resetPassword(user.id, newPassword);
            setMessage("✅ Đặt lại mật khẩu thành công.");
        } catch (err) {
            if (handleAuthError(err)) {
                return;
              }
            setError(err.message || "❌ Không thể đặt lại mật khẩu.");
        }
    }

    return (
        <div className="max-w-6xl mx-auto p-4 bg-white rounded shadow">
            <AdminHeader title="👤 Quản Lý User" />

            {message && (
                <div className="mb-3 p-2 rounded bg-green-100 text-green-700">
                    {message}
                </div>
            )}

            {error && (
                <div className="mb-3 p-2 rounded bg-red-100 text-red-700">
                    {error}
                </div>
            )}

            <form
                onSubmit={handleCreate}
                className="mb-6 border p-3 rounded bg-gray-50"
            >
                <div className="mb-3">
                    <PersonDropdown
                        label={null}
                        value={form.person_id}
                        onChange={(id) =>
                            setForm((prev) => ({
                                ...prev,
                                person_id: id,
                            }))
                        }
                        persons={persons}
                        placeholder="🔍Gõ tên để tìm nhanh hoặc bấm ▼ để chọn thành viên trong gia phả"
                    />
                </div>
                <div className="grid grid-cols-1 md:grid-cols-4 gap-2">
                <input
                    name="username"
                    value={form.username}
                    onChange={handleChange}
                    placeholder="😎 Đặt tên người dùng (Username)"
                    className="border rounded px-2 py-1"
                    required
                />

                <input
                    name="password"
                    type="password"
                    value={form.password}
                    onChange={handleChange}
                    placeholder="🔑 Đặt mật khẩu"
                    className="border rounded px-2 py-1"
                    required
                />

                <select
                    name="role"
                    value={form.role}
                    onChange={handleChange}
                    className="border rounded px-2 py-1"
                    required
                >
                    <option value="" disabled>
                        🎭 Chọn vai trò
                    </option>

                    {ROLES.map((role) => (
                        <option key={role.value} value={role.value}>
                            {role.label}
                        </option>
                    ))}
                </select>

                <button
                    type="submit"
                    className="bg-blue-600 text-white rounded px-3 py-1 hover:bg-blue-700"
                >
                    Thêm User
                </button>
                </div>
            </form>

            {loading ? (
                <div className="text-blue-600">⏳ Đang tải...</div>
            ) : (
                <div className="overflow-x-auto">
                    <table className="w-full border text-sm">
                        <thead className="bg-gray-100">
                            <tr>
                                <th className="border px-2 py-1">ID</th>
                                <th className="border px-2 py-1">👤 Thành viên</th>
                                <th className="border px-2 py-1">Username</th>
                                <th className="border px-2 py-1">Person ID</th>
                                <th className="border px-2 py-1">Role</th>
                                <th className="border px-2 py-1">Trạng thái</th>
                                <th className="border px-2 py-1">Hành động</th>
                            </tr>
                        </thead>

                        <tbody>
                            {users.map((user) => (
                                <tr key={user.id}>
                                    <td className="border px-2 py-1 text-center">{user.id}</td>
                                    <td className="border px-2 py-1">
                                        {persons.find((p) => Number(p.id ?? p.person_id) === Number(user.person_id))?.name || "-"}
                                    </td>
                                    <td className="border px-2 py-1">{user.username}</td>
                                    <td className="border px-2 py-1 text-center">
                                        {user.person_id || "-"}
                                    </td>

                                    <td className="border px-2 py-1">
                                        <select
                                            value={user.role}
                                            onChange={(e) =>
                                                handleRoleChange(user, e.target.value)
                                            }
                                            className="border rounded px-2 py-1 w-full"
                                        >
                                            {ROLES.map((role) => (
                                                <option key={role.value} value={role.value}>
                                                    {role.label}
                                                </option>
                                            ))}
                                        </select>
                                    </td>

                                    <td className="border px-2 py-1 text-center">
                                        {user.is_active ? (
                                            <span className="text-green-600 font-semibold">
                                                Active
                                            </span>
                                        ) : (
                                            <span className="text-red-600 font-semibold">
                                                Locked
                                            </span>
                                        )}
                                    </td>

                                    <td className="border px-2 py-1">
                                        <div className="flex gap-2 justify-center">
                                            <button
                                                type="button"
                                                disabled={currentUser?.id === user.id}
                                                onClick={() => handleToggleActive(user)}
                                                className={`px-2 py-1 rounded text-white ${currentUser?.id === user.id
                                                        ? "bg-gray-400 cursor-not-allowed"
                                                        : user.is_active
                                                            ? "bg-red-600 hover:bg-red-700"
                                                            : "bg-green-600 hover:bg-green-700"
                                                    }`}
                                            >
                                                {currentUser?.id === user.id
                                                    ? "Bạn"
                                                    : user.is_active
                                                        ? "Khóa"
                                                        : "Mở"}
                                            </button>

                                            <button
                                                type="button"
                                                onClick={() => handleResetPassword(user)}
                                                className="px-2 py-1 rounded bg-yellow-500 text-white hover:bg-yellow-600"
                                            >
                                                Đặt lại mật khẩu
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                            ))}

                            {users.length === 0 && (
                                <tr>
                                    <td colSpan="7" className="text-center py-4 text-gray-500">
                                        Chưa có user nào
                                    </td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
}