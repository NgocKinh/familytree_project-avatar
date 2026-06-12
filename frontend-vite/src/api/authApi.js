import axios from "axios";
import { makeApiUrl } from "./apiConfig";
const API_URL = makeApiUrl("/auth");

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