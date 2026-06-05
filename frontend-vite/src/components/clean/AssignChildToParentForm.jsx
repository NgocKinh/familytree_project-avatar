import React, { useEffect, useState } from "react";
import axios from "axios";
import { API_BASE_URL } from "../../api/apiConfig";
import PersonDropdown from "../common/PersonDropdown";
import MarriageDropdown from "../common/MarriageDropdown";
import { formatName } from "../../utils/formatName";
import { useNavigate } from "react-router-dom";

function AssignChildToParentForm() {
  const navigate = useNavigate();

  const getAuthConfig = () => {
    const token = localStorage.getItem("token");

    return {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    };
  };

  // -----------------------------
  // DATA LISTS
  // -----------------------------
  const [persons, setPersons] = useState([]);
  const [marriages, setMarriages] = useState([]);

  // -----------------------------
  // FORM STATE
  // -----------------------------
  const [noMarriage, setNoMarriage] = useState(true);
  const [marriageId, setMarriageId] = useState("");

  const [parentId, setParentId] = useState("");
  const [type, setType] = useState("");
  const [childId, setChildId] = useState("");

  // -----------------------------
  // UI STATE
  // -----------------------------
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [lockForm, setLockForm] = useState(false);
  const [loading, setLoading] = useState(false);
  useEffect(() => {
    axios.get(`${API_BASE_URL}/person`)
      .then(res => {
        const data = res.data || [];

        const normalized = data.map(p => ({
          ...p,
          name: formatName(p)
        }));

        setPersons(normalized);
      })
      .catch(() => setPersons([]));

    axios.get(`${API_BASE_URL}/marriage`)
      .then(res => setMarriages(res.data || []))
      .catch(() => setMarriages([]));
  }, []);
  const handleSubmit = async (e) => {
    e.preventDefault();
  
    setLoading(true);
  
    setError("");
    setSuccess("");
  
    if (!childId) {
      setError("❌ Chưa chọn người con.");
      setLoading(false);
      return;
    }
  
    try {
      // ===============================
      // CASE 1: KHÔNG CÓ HÔN NHÂN
      // ===============================
      if (noMarriage) {
        if (!parentId || !type) {
          setError("❌ Thiếu cha/mẹ hoặc vai trò.");
          return;
        }

        await axios.post(
          `${API_BASE_URL}/parent_child/assign`,
          {
            child_id: Number(childId),
            parent_id: Number(parentId),
            type: type,
          },
          getAuthConfig()
        );
      }

      // ===============================
      // CASE 2: CÓ HÔN NHÂN → AUTO CHA + MẸ
      // ===============================
      else {
        const m = marriages.find(
          (x) => String(x.id) === String(marriageId)
        );

        if (!m) {
          setError("❌ Không tìm thấy hôn nhân.");
          return;
        }

        await axios.post(
          `${API_BASE_URL}/parent_child/assign`,
          {
            child_id: Number(childId),
            parent_id: m.spouse_a_id,
            type: "father",
          },
          getAuthConfig()
        );

        await axios.post(
          `${API_BASE_URL}/parent_child/assign`,
          {
            child_id: Number(childId),
            parent_id: m.spouse_b_id,
            type: "mother",
          },
          getAuthConfig()
        );
      }

      setSuccess("✅ Đã bổ sung quan hệ Cha/Mẹ & Con thành công.");
      setLockForm(true);
    } catch (err) {
      console.error(
        "❌ ASSIGN CHILD ERROR:",
        err.response?.data || err
      );
    
      const data = err.response?.data;

      setError(
        data?.message ||
        data?.detail?.message ||
        data?.detail ||
        data?.warning ||
        data?.error ||
        "❌ Lỗi hệ thống."
      );
    }
    finally {
      setLoading(false);
    }
  };
  return (
    <div className="max-w-xl mx-auto p-4 bg-white shadow rounded">
      <h3 className="text-xl font-bold text-blue-700 mb-4 text-center">
        👨‍👩‍👧 Quan Hệ Cha/Mẹ & Con
      </h3>

      {success && (
        <div className="text-green-600 mb-2">
          {success}
        </div>
      )}

      {error && (
        <div className="text-red-600 mb-2 whitespace-pre-line">
          {error}
        </div>
      )}

        <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block font-semibold">
            1️⃣ Thuộc gia đình?
          </label>

          <label className="block mb-2">
            <input
              type="checkbox"
              checked={noMarriage}
              disabled={lockForm}
              onChange={() => {
                setNoMarriage(!noMarriage);
                setMarriageId("");
                setParentId("");
                setType("");
                setError("");
                setSuccess("");
              }}
            />{" "}
            Không thuộc gia đình nào
          </label>

          {!noMarriage && (
            <MarriageDropdown
              value={marriageId}
              onChange={setMarriageId}
              marriages={marriages}
              placeholder="-- Gõ tên hoặc kéo xuống chọn Cha & Mẹ --"
              disabled={lockForm}
            />
          )}
        </div>

        {noMarriage && (
          <div>
            <label className="block font-semibold">
              2️⃣ Chọn Cha / Mẹ
            </label>

            <PersonDropdown
              label={null}
              value={parentId}
              onChange={(id) => {
                setParentId(id);
                setError("");
                setSuccess("");

                const selectedParent = persons.find(
                  (p) => String(p.person_id ?? p.id) === String(id)
                );

                if (selectedParent?.gender === "male") {
                  setType("father");
                } else if (selectedParent?.gender === "female") {
                  setType("mother");
                } else {
                  setType("");
                }
              }}
              persons={persons}
              disabled={lockForm}
              filterFn={(p) => p.gender === "male" || p.gender === "female"}
              placeholder="-- Gõ tên hoặc kéo xuống chọn Cha/Mẹ --"
            />
          </div>
        )}

        <div>
        <label className="block font-semibold">
          3️⃣ Chọn Người Con
        </label>

          <PersonDropdown
            label={null}
            value={childId}
            onChange={(id) => {
              setChildId(id);
              setError("");
              setSuccess("");
            }}
            persons={persons}
            disabled={lockForm}
            placeholder="-- Gõ tên hoặc kéo xuống chọn người con --"
          />
        </div>

        <div className="flex justify-between pt-4">
          <button
            type="button"
            className="px-4 py-2 bg-gray-400 text-white rounded"
            onClick={() => {
              setParentId("");
              setType("");
              setMarriageId("");
              setChildId("");
              setNoMarriage(true);
              setError("");
              setSuccess("");
              setLockForm(false);
            }}
          >
            ❌ Hủy
          </button>

          {!lockForm && (
            <button
              type="submit"
              disabled={loading}
              className="px-4 py-2 bg-blue-600 text-white rounded"
            >
              {loading ? "⏳ Đang lưu..." : "💾 Lưu"}
            </button>
          )}

          {lockForm && (
            <button
              type="button"
              onClick={() => navigate("/")}
              className="px-4 py-2 bg-gray-600 text-white rounded"
            >
              ⬅ Quay về Home
            </button>
          )}
        </div>
      </form>
    </div>
  );
}

export default AssignChildToParentForm;