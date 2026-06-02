import React from "react";
import { useNavigate } from "react-router-dom";

export default function AdminHeader({ title }) {
  const navigate = useNavigate();

  return (
    <div className="sticky top-0 z-50 bg-white border-b py-3 mb-4">
      <div className="flex justify-between items-center">
        <button
          onClick={() => navigate("/admin")}
          className="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700"
        >
          ⬅️ Admin
        </button>

        <button
          onClick={() => navigate("/")}
          className="px-4 py-2 rounded bg-gray-700 text-white hover:bg-gray-800"
        >
          🏠 Home
        </button>
      </div>

      <h2 className="text-2xl font-bold text-center mt-3">
        {title}
      </h2>
    </div>
  );
}