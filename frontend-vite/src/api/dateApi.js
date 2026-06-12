// ======================================================================
// File: src/api/dateApi.js  (v1.1-FIXED)
// ======================================================================

import axios from "axios";
import { API_BASE_URL } from "./apiConfig";
const API_BASE = API_BASE_URL.replace("/api", "");

// 🔹 Convert solar → lunar using backend Flask API
export async function convertSolarToLunar(solarDate) {
  if (!solarDate) return "";

  try {
    const res = await axios.post(`${API_BASE}/convert_lunar`, {
      birth_date: solarDate,
    });

    return res.data.lunar_date || "";
  } catch (err) {
    console.error("❌ convertSolarToLunar ERROR:", err);
    return "";
  }
}