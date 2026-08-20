import React, { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

import { makeApiUrl } from "../api/apiConfig";
import BackgroundImagePicker from "../components/BackgroundImagePicker";


const emptyForm = {
  family_code: "",
  family_name: "",
  signboard: "",
  subtitle: "",
  slogan_line_1: "",
  slogan_line_2: "",
  origin_line: "",
  welcome_title: "",
  welcome_text: "",
  background_image: "/trongdong.png",
};


function Field({ label, name, value, onChange, required = false }) {
  return (
    <label className="block">
      <span className="mb-1 block text-sm font-semibold text-gray-700">
        {label}
        {required && <span className="text-red-600"> *</span>}
      </span>
      <input
        name={name}
        value={value}
        onChange={onChange}
        required={required}
        className="w-full rounded-lg border border-gray-300 px-3 py-2 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
      />
    </label>
  );
}


export default function AdminFamilySettingsPage() {
  const navigate = useNavigate();
  const [form, setForm] = useState(emptyForm);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    axios
      .get(makeApiUrl("/setup/config"))
      .then((response) => {
        const config = response.data || {};
        setForm({
          family_code: config.familyCode || "",
          family_name: config.familyName || "",
          signboard: config.signboard || "",
          subtitle: config.subtitle || "",
          slogan_line_1: config.sloganLines?.[0] || "",
          slogan_line_2: config.sloganLines?.[1] || "",
          origin_line: config.originLine || "",
          welcome_title: config.welcomeTitle || "",
          welcome_text: config.welcomeText || "",
          background_image:
            config.backgroundImage || "/trongdong.png",
        });
      })
      .catch(() => {
        setError("Không tải được cấu hình dòng họ.");
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  const updateForm = (event) => {
    const { name, value } = event.target;
    setForm((current) => ({ ...current, [name]: value }));
  };

  const saveConfig = async (event) => {
    event.preventDefault();
    setError("");
    setSaving(true);

    try {
      const token = localStorage.getItem("token");
      await axios.put(
        makeApiUrl("/setup/config"),
        form,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      window.location.replace("/");
    } catch (requestError) {
      const detail = requestError?.response?.data?.detail;
      setError(
        typeof detail === "string"
          ? detail
          : "Không thể lưu cấu hình dòng họ."
      );
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="p-6 text-center text-gray-600">
        Đang tải cấu hình dòng họ...
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-slate-100 px-4 py-6">
      <form
        onSubmit={saveConfig}
        className="mx-auto max-w-4xl rounded-2xl bg-white p-6 shadow-xl md:p-8"
      >
        <div className="mb-6 flex flex-wrap items-center justify-between gap-3 border-b pb-4">
          <div>
            <h1 className="text-2xl font-bold text-blue-800">
              Cấu hình dòng họ
            </h1>
            <p className="mt-1 text-sm text-gray-600">
              Admin có thể sửa nội dung trang chủ và thay hình nền.
            </p>
          </div>
          <button
            type="button"
            onClick={() => navigate("/admin")}
            className="rounded-lg bg-gray-700 px-4 py-2 font-semibold text-white hover:bg-gray-800"
          >
            ← Quay lại
          </button>
        </div>

        {error && (
          <div className="mb-5 rounded-lg bg-red-100 px-4 py-3 text-red-700">
            {error}
          </div>
        )}

        <div className="grid gap-4 md:grid-cols-2">
          <Field
            label="Mã dòng họ"
            name="family_code"
            value={form.family_code}
            onChange={updateForm}
            required
          />
          <Field
            label="Tên hiển thị"
            name="family_name"
            value={form.family_name}
            onChange={updateForm}
            required
          />
          <Field
            label="Tên bảng hiệu"
            name="signboard"
            value={form.signboard}
            onChange={updateForm}
            required
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

        <button
          type="submit"
          disabled={saving}
          className="mt-7 w-full rounded-xl bg-blue-700 px-5 py-3 text-lg font-bold text-white hover:bg-blue-800 disabled:bg-blue-300"
        >
          {saving ? "Đang lưu..." : "Lưu cấu hình"}
        </button>
      </form>
    </main>
  );
}
