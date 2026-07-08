import maleAvatar from "../assets/default_male.png";
import femaleAvatar from "../assets/default_female.png";
import otherAvatar from "../assets/default_other.png";
import { API_BASE_URL } from "../api/apiConfig";

const API = API_BASE_URL.replace("/api", "");

/* fallback avatar */
export function fallbackAvatar(gender) {

  const g = (gender || "").toLowerCase();

  if (g === "male") return maleAvatar;
  if (g === "female") return femaleAvatar;

  return otherAvatar;
}

/* avatar url */
export function getAvatarURL(person) {
  if (!person) return otherAvatar;

  const id = person.id ?? person.person_id;

  if (person.avatar) {
    if (person.avatar.startsWith("http")) {
      return person.avatar;
    }

    if (person.avatar.startsWith("/")) {
      return `${API}${person.avatar}`;
    }

    return `${API}/static/avatars/${person.avatar}?v=${person.updated_at || id}`;
  }

  if (!id) return fallbackAvatar(person.gender);

  return `${API}/static/avatars/${id}.jpg?v=${id}`;
}

/* error handler */
export function handleAvatarError(e, gender) {
  const img = e.target;
  const src = img.src || "";

  if (src.includes(".jpg")) {
    img.src = src.replace(".jpg", ".png");
    return;
  }

  img.onerror = null;
  img.src = fallbackAvatar(gender);
}