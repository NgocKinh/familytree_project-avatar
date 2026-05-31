import axios from "axios";

const API_URL = "http://localhost:8000/api/auth";

export async function checkNearAccess(targetPersonId) {
  const token = localStorage.getItem("token");

  const res = await axios.post(
    `${API_URL}/check-near-access`,
    {
      target_person_id: Number(targetPersonId),
    },
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  return res.data;
}