// ======================================================
// File: src/api/treeApi.js
// ======================================================

import axios from "axios";
import { API_BASE_URL } from "./apiConfig";

const API_BASE = "http://localhost:8000/api/tree";

export async function getFamilyTree(id) {
  if (!id) {
    throw new Error("ID is required");
  }

  try {
    const res = await axios.get(`${API_BASE}/${id}`);
    const data = res.data || {};

    // Chuẩn hoá dữ liệu cho TreePage
    return {
      center: data.center,
      spouse: data.spouse,
      marriage_status: data.marriage_status,
      father_parents: data.father_parents || [],
      mother_parents: data.mother_parents || [],
      children_common: data.children_common || [],
      children_father_separate: data.children_father_separate || [],
      children_mother_separate: data.children_mother_separate || [],
    };
  } catch (err) {
    console.error("❌ Lỗi API getFamilyTree:", err);
    throw err;
  }
}