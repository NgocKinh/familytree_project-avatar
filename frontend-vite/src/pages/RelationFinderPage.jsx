import React, { useState, useEffect } from "react";
import axios from "axios";
import { makeApiUrl, API_BASE_URL } from "../api/apiConfig";
import PersonDropdown from "../components/common/PersonDropdown";
import { useNavigate } from "react-router-dom";
import { handleAuthError } from "../utils/authErrorHandler";
const BACKEND_BASE_URL = API_BASE_URL.replace("/api", "");
function RelationFinderPage() {
  const navigate = useNavigate();
  const [persons, setPersons] = useState([]);
  const [personA, setPersonA] = useState("");
  const [personB, setPersonB] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // ================================================================
  // 🔹 Lấy danh sách person từ backend
  // ================================================================
  useEffect(() => {
    async function fetchPersons() {
      try {
        const res = await axios.get(
          makeApiUrl("/person/")
        );
        const rawPersons = Array.isArray(res.data)
          ? res.data
          : Array.isArray(res.data?.data)
          ? res.data.data
          : Array.isArray(res.data?.persons)
          ? res.data.persons
          : [];

        const personsActive = rawPersons.map((p) => ({
          ...p,
          person_id: p.person_id ?? p.id,
          full_name_vn: p.full_name_vn || buildFullName(p),
        }));

        const sortedPersons = [...personsActive].sort((a, b) => {
          if (!a.birth_date && !b.birth_date) {
            return a.full_name_vn.localeCompare(b.full_name_vn, "vi");
          }

          if (!a.birth_date) return 1;
          if (!b.birth_date) return -1;

          if (a.birth_date !== b.birth_date) {
            return new Date(b.birth_date) - new Date(a.birth_date);
          }

          return a.full_name_vn.localeCompare(b.full_name_vn, "vi");
        });

        setPersons(sortedPersons);
      } catch (err) {
        if (handleAuthError(err)) {
          return;
        }
      
        console.error("❌ Lỗi khi tải danh sách:", err);
        setError("Không thể tải danh sách thành viên.");
      }
    }

    fetchPersons();
  }, []);
  // ================================================================
  // 🔹 Reset kết quả khi thay đổi lựa chọn
  // ================================================================
  useEffect(() => {
    setResult(null);
    setError("");
  }, [personA, personB]);
  // ================================================================
  // 🔹 Ghép họ tên
  // ================================================================
  const buildFullName = (p) => {
    return `${p.sur_name || ""} ${p.last_name || ""} ${p.middle_name || ""} ${p.first_name || ""
      }`
      .replace(/\s+/g, " ")
      .trim();
  };

  // ================================================================
  // 🔹 Gửi yêu cầu phân tích quan hệ
  // ================================================================
  const handleAnalyze = async () => {
    if (!personA || !personB) {
      setError("Vui lòng chọn đủ hai người để phân tích!");
      return;
    }

    if (personA === personB) {
      setError("Hai người không thể là cùng một cá nhân!");
      return;
    }

    setError("");
    setResult(null);
    setLoading(true);

    try {
      const res = await axios.get(
        makeApiUrl(
          `/relationship?source_id=${parseInt(personA)}&target_id=${parseInt(personB)}`
        )
      );

      setResult(res.data);
    } catch (err) {
      if (handleAuthError(err)) {
        return;
      }
    
      console.error("❌ Lỗi khi phân tích quan hệ:", err);
      setError("Đã xảy ra lỗi khi truy vấn máy chủ.");
    } finally {
      setLoading(false);
    }
  };

  // ================================================================
  // 🔹 Giao diện hiển thị
  // ================================================================
  const selectedA = persons.find(
    (p) => p.person_id === Number(personA)
  );

  const selectedB = persons.find(
    (p) => p.person_id === Number(personB)
  );
  
  return (
    <div className="w-full p-4 bg-white">
      
      {/* ====================================================== */}
      {/* STICKY HEADER */}
      {/* ====================================================== */}
      <div className="sticky top-0 z-50 bg-white border-b py-2 mb-4">
        <div className="grid grid-cols-3 items-center min-h-[52px]">
  
          <button
            onClick={() => navigate("/")}
            className="justify-self-start px-4 py-2 rounded bg-gray-700 text-white hover:bg-gray-800 leading-none"
          >
            🏠 Home
          </button>
  
          <h1 className="justify-self-center text-2xl font-bold text-indigo-700 whitespace-nowrap leading-none">
            🔍 TÌM MỐI QUAN HỆ
          </h1>
  
          <div />
        </div>
      </div>
  
      {/* ====================================================== */}
      {/* WORKSPACE */}
      {/* ====================================================== */}
      <div className="max-w-5xl mx-auto bg-white border rounded-xl shadow-sm p-4">
  
        {/* SELECTORS */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
  
          <PersonDropdown
            label="Người A:"
            value={personA}
            onChange={setPersonA}
            persons={persons}
            placeholder="-- Gõ tên hoặc kéo xuống Chọn Người A --"
          />
  
          <PersonDropdown
            label="Người B:"
            value={personB}
            onChange={setPersonB}
            persons={persons}
            placeholder="-- Gõ tên hoặc kéo xuống Chọn Người B --"
          />
        </div>
  
        {/* ACTION BUTTONS */}
        <div className="flex justify-center gap-3 mb-4">
  
          <button
            onClick={handleAnalyze}
            disabled={loading}
            className={`px-6 py-2 rounded-lg font-semibold text-white transition ${
              loading
                ? "bg-gray-400 cursor-not-allowed"
                : "bg-blue-600 hover:bg-blue-700"
            }`}
          >
            {loading ? "Đang phân tích..." : "🔍 Phân Tích"}
          </button>
  
          <button
            onClick={() => {
              setPersonA("");
              setPersonB("");
              setResult(null);
              setError("");
            }}
            className="px-6 py-2 rounded-lg font-semibold bg-gray-200 hover:bg-gray-300"
          >
            Reset
          </button>
  
        </div>
  
        {/* ERROR */}
        {error && (
          <div className="mb-4 p-3 rounded-lg border border-red-300 bg-red-50 text-red-700 text-center">
            {error}
          </div>
        )}
  
  {/* RESULT */}
  {result && !error && (
    <div className="mt-4 border border-indigo-100 rounded-xl bg-white overflow-hidden shadow-sm">

      {/* HEADER */}
      <div className="bg-indigo-600 text-white px-4 py-3 font-bold text-lg">
        ✅ Kết Quả Phân Tích Quan Hệ
      </div>

      {/* BODY */}
      <div className="p-5 space-y-4 bg-indigo-50/40">

        {/* MAIN RELATION */}
        <div className="text-center">

          <div className="text-gray-500 text-sm mb-1">
            Quan hệ xác định
          </div>

          <div className="text-2xl font-bold text-slate-800">
          {/*
            {selectedA && (
              <img
                src={getAvatarURL(selectedA)}
                onError={(e) => handleAvatarError(e, selectedA?.gender)}
                className="w-20 h-20 rounded-full object-cover mx-auto mb-2 border"
              />
            )}
            */}    
            {selectedA?.full_name_vn}
          </div>

          <div className="text-lg my-2 text-gray-700">
            là
          </div>

          <div className="inline-block px-5 py-2 rounded-full bg-emerald-600 text-white text-xl font-bold shadow">
          {
            result.relation ||
            result.result?.relation ||
            result.relationship ||
            "Chưa xác định quan hệ"
          }
          </div>

          <div className="text-lg my-2 text-gray-700">
            của
          </div>

          <div className="text-2xl font-bold text-slate-800">
          {/*
            {selectedB && (
              <img
                src={getAvatarURL(selectedB)}
                onError={(e) => handleAvatarError(e, selectedB?.gender)}
                className="w-20 h-20 rounded-full object-cover mx-auto mb-2 border"
              />
            )}
            */}
            {selectedB?.full_name_vn}
          </div>
        
        </div>

        {/* EXTRA INFO */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">

          {/* CONFIDENCE */}
          <div className="border rounded-lg bg-white p-4">
            <div className="text-sm text-gray-500 mb-1">
              Độ tin cậy
            </div>

            <div className="text-lg font-semibold text-gray-800">
              {result.confidence || "N/A"}
            </div>
          </div>

          {/* RELATION TYPE */}
          <div className="border rounded-lg bg-white p-4">
            <div className="text-sm text-gray-500 mb-1">
              Relationship Type
            </div>

            <div className="text-lg font-semibold text-gray-800">
              {result.relation_basic || "N/A"}
            </div>
          </div>

        </div>

      </div>
    </div>
  )}
  
      </div>
    </div>
  );
}

export default RelationFinderPage;
