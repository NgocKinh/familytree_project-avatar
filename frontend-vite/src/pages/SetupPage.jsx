import React, { useState } from "react";
import axios from "axios";

import { makeApiUrl } from "../api/apiConfig";
import BackgroundImagePicker from "../components/BackgroundImagePicker";


const initialForm = {
  family_code: "FamilyTree",
  family_name: "",
  signboard: "",
  subtitle: "Gìn Giữ Cội Nguồn",
  slogan_line_1: "Kết Nối Các Thế Hệ",
  slogan_line_2: "Gìn Giữ Truyền Thống",
  origin_line: "",
  welcome_title: "Chào mừng bạn đến với hệ thống gia phả",
  welcome_text:
    "Nơi lưu giữ truyền thống, kết nối các thế hệ và tôn vinh cội nguồn.",
  background_image: "/trongdong.png",
  admin_full_name: "",
  admin_username: "",
  admin_password: "",
};


function Field({
  label,
  name,
  value,
  onChange,
  required = false,
  type = "text",
  placeholder = "",
}) {
  return (
    <label className="block">
      <span className="mb-1 block text-sm font-semibold text-gray-700">
        {label}
        {required && <span className="text-red-600"> *</span>}
      </span>
      <input
        type={type}
        name={name}
        value={value}
        onChange={onChange}
        required={required}
        placeholder={placeholder}
        className="w-full rounded-lg border border-gray-300 px-3 py-2 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
      />
    </label>
  );
}


export default function SetupPage() {
  const [form, setForm] = useState(initialForm);
  const [setupToken, setSetupToken] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const updateForm = (event) => {
    const { name, value } = event.target;

    setForm((current) => ({
      ...current,
      [name]: value,
    }));
  };

  const completeSetup = async (event) => {
    event.preventDefault();
    setError("");

    if (form.admin_password !== confirmPassword) {
      setError("Hai lần nhập mật khẩu chưa giống nhau.");
      return;
    }

    setLoading(true);

    try {
      const response = await axios.post(
        makeApiUrl("/setup/complete"),
        form,
        {
          headers: {
            "X-Setup-Token": setupToken,
          },
        }
      );

      localStorage.setItem("token", response.data.access_token);
      localStorage.setItem(
        "currentUser",
        JSON.stringify(response.data.user)
      );
      window.location.replace("/");
    } catch (requestError) {
      const detail = requestError?.response?.data?.detail;

      if (Array.isArray(detail)) {
        setError(
          detail
            .map((item) => item?.msg)
            .filter(Boolean)
            .join(". ")
        );
      } else {
        setError(
          detail ||
            "Không thể hoàn tất thiết lập. Vui lòng kiểm tra lại thông tin."
        );
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-slate-100 px-4 py-8">
      <form
        onSubmit={completeSetup}
        className="mx-auto max-w-4xl rounded-2xl bg-white p-6 shadow-xl md:p-8"
      >
        <div className="mb-7 text-center">
          <h1 className="text-3xl font-bold text-blue-800">
            Thiết lập Gia Phả lần đầu
          </h1>
          <p className="mt-2 text-gray-600">
            Nhập thông tin dòng họ và tạo tài khoản Admin đầu tiên.
          </p>
        </div>

        {error && (
          <div className="mb-6 rounded-lg bg-red-100 px-4 py-3 text-red-700">
            {error}
          </div>
        )}

        <section className="mb-8">
          <h2 className="mb-4 border-b pb-2 text-xl font-bold text-gray-800">
            1. Thông tin dòng họ
          </h2>

          <div className="grid gap-4 md:grid-cols-2">
            <Field
              label="Mã dòng họ"
              name="family_code"
              value={form.family_code}
              onChange={updateForm}
              required
              placeholder="Ví dụ: TocLe"
            />
            <Field
              label="Tên hiển thị"
              name="family_name"
              value={form.family_name}
              onChange={updateForm}
              required
              placeholder="Ví dụ: Gia Phả Tộc Lê"
            />
            <Field
              label="Tên bảng hiệu"
              name="signboard"
              value={form.signboard}
              onChange={updateForm}
              required
              placeholder="Ví dụ: GIA PHẢ TỘC LÊ"
            />
            <Field
              label="Dòng phụ"
              name="subtitle"
              value={form.subtitle}
              onChange={updateForm}
            />
            <Field
              label="Câu giới thiệu 1"
              name="slogan_line_1"
              value={form.slogan_line_1}
              onChange={updateForm}
            />
            <Field
              label="Câu giới thiệu 2"
              name="slogan_line_2"
              value={form.slogan_line_2}
              onChange={updateForm}
            />
            <div className="md:col-span-2">
              <Field
                label="Tên dòng họ - Quê quán"
                name="origin_line"
                value={form.origin_line}
                onChange={updateForm}
                placeholder="Ví dụ: Tộc Lê - Quảng Nam"
              />
            </div>
            <div className="md:col-span-2">
              <Field
                label="Tiêu đề lời chào"
                name="welcome_title"
                value={form.welcome_title}
                onChange={updateForm}
              />
            </div>
            <label className="block md:col-span-2">
              <span className="mb-1 block text-sm font-semibold text-gray-700">
                Nội dung lời chào
              </span>
              <textarea
                name="welcome_text"
                value={form.welcome_text}
                onChange={updateForm}
                rows="3"
                className="w-full rounded-lg border border-gray-300 px-3 py-2 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
              />
            </label>
            <div className="md:col-span-2">
              <BackgroundImagePicker
                value={form.background_image}
                onChange={(backgroundImage) =>
                  setForm((current) => ({
                    ...current,
                    background_image: backgroundImage,
                  }))
                }
                onError={setError}
              />
            </div>
          </div>
        </section>

        <section className="mb-8">
          <h2 className="mb-4 border-b pb-2 text-xl font-bold text-gray-800">
            2. Tài khoản Admin đầu tiên
          </h2>

          <div className="grid gap-4 md:grid-cols-2">
            <Field
              label="Họ tên Admin"
              name="admin_full_name"
              value={form.admin_full_name}
              onChange={updateForm}
              required
            />
            <Field
              label="Tên đăng nhập"
              name="admin_username"
              value={form.admin_username}
              onChange={updateForm}
              required
              placeholder="Chỉ dùng chữ, số, dấu chấm, gạch ngang"
            />
            <Field
              label="Mật khẩu"
              name="admin_password"
              value={form.admin_password}
              onChange={updateForm}
              required
              type="password"
            />
            <Field
              label="Nhập lại mật khẩu"
              name="confirm_password"
              value={confirmPassword}
              onChange={(event) => setConfirmPassword(event.target.value)}
              required
              type="password"
            />
          </div>
        </section>

        <section className="mb-8">
          <h2 className="mb-4 border-b pb-2 text-xl font-bold text-gray-800">
            3. Xác nhận thiết lập
          </h2>

          <Field
            label="Mã thiết lập một lần"
            name="setup_token"
            value={setupToken}
            onChange={(event) => setSetupToken(event.target.value)}
            required
            type="password"
            placeholder="Mã này được cấp khi triển khai hệ thống"
          />

          <p className="mt-2 text-sm text-gray-500">
            Mã thiết lập không phải mật khẩu Admin và chỉ được dùng một lần.
          </p>
        </section>

        <button
          type="submit"
          disabled={loading}
          className="w-full rounded-xl bg-blue-700 px-5 py-3 text-lg font-bold text-white transition hover:bg-blue-800 disabled:bg-blue-300"
        >
          {loading ? "Đang thiết lập..." : "Hoàn tất thiết lập"}
        </button>
      </form>
    </main>
  );
}
