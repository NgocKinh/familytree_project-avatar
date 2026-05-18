// ==========================================================
// File: formatName.js
// Version: PROJECT-STANDARD
// Mục tiêu:
//   - Dùng chung toàn project
//   - sur_name = tên hiệu / pháp danh / tên thánh
//   - last_name + middle_name + first_name = tên chính
// ==========================================================

export function formatName(person, options = {}) {
  if (!person) return "";

  const {
    sur_name = "",
    last_name = "",
    middle_name = "",
    first_name = "",
  } = person;

  const {
    mode = "full",        // full | short
    showAlias = false,    // bật/tắt tên hiệu
  } = options;

  // =========================
  // NORMALIZE INPUT
  // =========================
  const clean = (val) => (val ? String(val).trim() : "");

  const ln = clean(last_name);
  const mn = clean(middle_name);
  const fn = clean(first_name);

  // =========================
  // FULL NAME
  // =========================
  const full = [ln, mn, fn]
    .filter(Boolean)
    .join(" ")
    .trim();

  // =========================
  // SHORT NAME
  // =========================
  const short = [
    ln ? ln.charAt(0).toUpperCase() + "." : "",
    mn ? mn.charAt(0).toUpperCase() + "." : "",
    fn,
  ]
    .filter(Boolean)
    .join(" ")
    .trim();

  let name = mode === "short" ? short : full;

  // =========================
  // SUR NAME (đứng đầu)
  // =========================
  if (showAlias && clean(sur_name)) {
    name = `${clean(sur_name)} ${name}`.trim();
  }
  
  return name.trim();
}
