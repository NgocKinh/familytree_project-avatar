import maleAvatar from "../assets/male.png";
import femaleAvatar from "../assets/female.png";
import otherAvatar from "../assets/other.png";

const BASE = "http://localhost:8010/static/avatars/";

// ======================================================
// Chuẩn hóa giới tính
// ======================================================
function normalizeGender(gender) {
  const g = (gender || "").toString().toLowerCase();

  if (g === "male" || g === "m") return "male";
  if (g === "female" || g === "f") return "female";

  return "other";
}

// ======================================================
// Lấy URL avatar theo filename từ DB
// ======================================================
export function getAvatarURL(avatar, gender) {
  if (!avatar || typeof avatar !== "string") {
    return fallbackAvatar(gender);
  }

  if (avatar.startsWith("http://") || avatar.startsWith("https://")) {
    return avatar;
  }

  return BASE + avatar;
}

// ======================================================
// Fallback theo giới tính
// ======================================================
export function fallbackAvatar(gender) {
  const g = normalizeGender(gender);

  if (g === "male") return maleAvatar;
  if (g === "female") return femaleAvatar;

  return otherAvatar;
}

// ======================================================
// Nếu ảnh thật lỗi → fallback
// ======================================================
export function handleAvatarError(e, avatar, gender) {
  if (!e || !e.target) return;

  e.target.onerror = null;
  e.target.src = fallbackAvatar(gender);
}