import maleAvatar from "../assets/default_male.png";
import femaleAvatar from "../assets/default_female.png";
import otherAvatar from "../assets/default_other.png";

const API = "http://localhost:8010";

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

  if (person.avatar) {
    return `${API}/cdn/avatar/${person.person_id}?t=${Date.now()}`;
  }

  return fallbackAvatar(person.gender);
}

/* error handler */
export function handleAvatarError(e, gender) {

  e.target.onerror = null;
  e.target.src = fallbackAvatar(gender);

}