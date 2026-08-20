import React, { useState } from "react";
import axios from "axios";

import { makeApiUrl } from "../api/apiConfig";


const initialForm = {
  family_code: "FamilyTree",
  family_name: "",
  signboard: "",
  subtitle: "G?n Gi? C?i Ngu?n",
  slogan_line_1: "K?t N?i C?c Th? H?",
  slogan_line_2: "G?n Gi? Truy?n Th?ng",
  origin_line: "",
  welcome_title: "Ch?o m?ng b?n ??n v?i h? th?ng gia ph?",
  welcome_text:
    "N?i l?u gi? truy?n th?ng, k?t n?i c?c th? h? v? t?n vinh c?i ngu?n.",
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


export default function SetupPage({ onCompleted }) {
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
      setError("Hai l?n nh?p m?t kh?u ch?a gi?ng nhau.");
      return;
    }

    setLoading(true);

    try {
      await axios.post(
        makeApiUrl("/setup/complete"),
        form,
        {
          headers: {
            "X-Setup-Token": setupToken,
          },
        }
      );

      if (onCompleted) {
        onCompleted();
      }

      window.location.replace("/login");
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
            "Kh?ng th? ho?n t?t thi?t l?p. Vui l?ng ki?m tra l?i th?ng tin."
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
            Thi?t l?p Gia Ph? l?n ??u
          </h1>
          <p className="mt-2 text-gray-600">
            Nh?p th?ng tin d?ng h? v? t?o t?i kho?n Admin ??u ti?n.
          </p>
        </div>

        {error && (
          <div className="mb-6 rounded-lg bg-red-100 px-4 py-3 text-red-700">
            {error}
          </div>
        )}

        <section className="mb-8">
          <h2 className="mb-4 border-b pb-2 text-xl font-bold text-gray-800">
            1. Th?ng tin d?ng h?
          </h2>

          <div className="grid gap-4 md:grid-cols-2">
            <Field
              label="M? d?ng h?"
              name="family_code"
              value={form.family_code}
              onChange={updateForm}
              required
              placeholder="V? d?: TocLe"
            />
            <Field
              label="T?n hi?n th?"
              name="family_name"
              value={form.family_name}
              onChange={updateForm}
              required
              placeholder="V? d?: Gia Ph? T?c L?"
            />
            <Field
              label="T?n b?ng hi?u"
              name="signboard"
              value={form.signboard}
              onChange={updateForm}
              required
              placeholder="V? d?: GIA PH? T?C L?"
            />
            <Field
              label="D?ng ph?"
              name="subtitle"
              value={form.subtitle}
              onChange={updateForm}
            />
            <Field
              label="C?u gi?i thi?u 1"
              name="slogan_line_1"
              value={form.slogan_line_1}
              onChange={updateForm}
            />
            <Field
              label="C?u gi?i thi?u 2"
              name="slogan_line_2"
              value={form.slogan_line_2}
              onChange={updateForm}
            />
            <div className="md:col-span-2">
              <Field
                label="T?n d?ng h? ? Qu? qu?n"
                name="origin_line"
                value={form.origin_line}
                onChange={updateForm}
                placeholder="V? d?: T?c L? ? Qu?ng Nam"
              />
            </div>
            <div className="md:col-span-2">
              <Field
                label="Ti?u ?? l?i ch?o"
                name="welcome_title"
                value={form.welcome_title}
                onChange={updateForm}
              />
            </div>
            <label className="block md:col-span-2">
              <span className="mb-1 block text-sm font-semibold text-gray-700">
                N?i dung l?i ch?o
              </span>
              <textarea
                name="welcome_text"
                value={form.welcome_text}
                onChange={updateForm}
                rows="3"
                className="w-full rounded-lg border border-gray-300 px-3 py-2 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
              />
            </label>
          </div>
        </section>

        <section className="mb-8">
          <h2 className="mb-4 border-b pb-2 text-xl font-bold text-gray-800">
            2. T?i kho?n Admin ??u ti?n
          </h2>

          <div className="grid gap-4 md:grid-cols-2">
            <Field
              label="H? t?n Admin"
              name="admin_full_name"
              value={form.admin_full_name}
              onChange={updateForm}
              required
            />
            <Field
              label="T?n ??ng nh?p"
              name="admin_username"
              value={form.admin_username}
              onChange={updateForm}
              required
              placeholder="Ch? d?ng ch?, s?, d?u ch?m, g?ch ngang"
            />
            <Field
              label="M?t kh?u"
              name="admin_password"
              value={form.admin_password}
              onChange={updateForm}
              required
              type="password"
            />
            <Field
              label="Nh?p l?i m?t kh?u"
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
            3. X?c nh?n thi?t l?p
          </h2>

          <Field
            label="M? thi?t l?p m?t l?n"
            name="setup_token"
            value={setupToken}
            onChange={(event) => setSetupToken(event.target.value)}
            required
            type="password"
            placeholder="M? n?y ???c c?p khi tri?n khai h? th?ng"
          />

          <p className="mt-2 text-sm text-gray-500">
            M? thi?t l?p kh?ng ph?i m?t kh?u Admin v? ch? ???c d?ng m?t l?n.
          </p>
        </section>

        <button
          type="submit"
          disabled={loading}
          className="w-full rounded-xl bg-blue-700 px-5 py-3 text-lg font-bold text-white transition hover:bg-blue-800 disabled:bg-blue-300"
        >
          {loading ? "?ang thi?t l?p..." : "Ho?n t?t thi?t l?p"}
        </button>
      </form>
    </main>
  );
}
