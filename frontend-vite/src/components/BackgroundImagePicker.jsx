import React from "react";


const DEFAULT_BACKGROUND_IMAGE = "/trongdong.png";
const MAX_BACKGROUND_FILE_SIZE = 2 * 1024 * 1024;
const ALLOWED_BACKGROUND_TYPES = [
  "image/jpeg",
  "image/png",
  "image/webp",
];


export default function BackgroundImagePicker({
  value,
  onChange,
  onError,
}) {
  const selectBackground = (event) => {
    const file = event.target.files?.[0];
    onError("");

    if (!file) {
      onChange(DEFAULT_BACKGROUND_IMAGE);
      return;
    }

    if (!ALLOWED_BACKGROUND_TYPES.includes(file.type)) {
      onError("Hình nền phải là tệp PNG, JPG hoặc WebP.");
      event.target.value = "";
      return;
    }

    if (file.size > MAX_BACKGROUND_FILE_SIZE) {
      onError("Hình nền không được lớn hơn 2 MB.");
      event.target.value = "";
      return;
    }

    const reader = new FileReader();

    reader.onload = () => {
      onChange(String(reader.result));
    };

    reader.onerror = () => {
      onError("Không thể đọc tệp hình nền đã chọn.");
      event.target.value = "";
    };

    reader.readAsDataURL(file);
  };

  return (
    <div>
      <span className="mb-2 block text-sm font-semibold text-gray-700">
        Hình nền trang chủ (không bắt buộc)
      </span>

      <div className="grid gap-4 rounded-xl border border-gray-200 bg-gray-50 p-4 md:grid-cols-2">
        <div>
          <input
            type="file"
            accept="image/png,image/jpeg,image/webp"
            onChange={selectBackground}
            className="block w-full text-sm text-gray-700 file:mr-4 file:rounded-lg file:border-0 file:bg-blue-100 file:px-4 file:py-2 file:font-semibold file:text-blue-800 hover:file:bg-blue-200"
          />

          <p className="mt-2 text-sm text-gray-500">
            Chấp nhận PNG, JPG hoặc WebP, tối đa 2 MB. Nếu không chọn,
            hệ thống giữ hình trống đồng mặc định.
          </p>

          {value !== DEFAULT_BACKGROUND_IMAGE && (
            <button
              type="button"
              onClick={() => onChange(DEFAULT_BACKGROUND_IMAGE)}
              className="mt-3 rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm font-semibold text-gray-700 hover:bg-gray-100"
            >
              Dùng lại hình trống đồng
            </button>
          )}
        </div>

        <img
          src={value || DEFAULT_BACKGROUND_IMAGE}
          alt="Xem trước hình nền"
          className="h-40 w-full rounded-lg border border-gray-200 object-cover"
        />
      </div>
    </div>
  );
}
