import { useNavigate } from "react-router-dom";

import ParentChildList from "../components/ParentChildList";

export default function ParentChildPage({ role }) {
  const navigate = useNavigate();

  return (
    <div className="w-full p-4 bg-white">
      <div className="sticky top-0 z-50 bg-white border-b py-1 mb-0">
        <div className="grid grid-cols-3 items-center">
          <button
            onClick={() => navigate("/")}
            className="justify-self-start px-4 py-2 rounded bg-gray-700 text-white hover:bg-gray-800"
          >
            🏠 Home
          </button>

          <h2 className="justify-self-center text-2xl font-bold text-blue-600 whitespace-nowrap">
            👨‍👩‍👧‍👦 Quản Lý Quan Hệ Cha – Con
          </h2>

          <div />
        </div>
      </div>

      <ParentChildList role={role} />
    </div>
  );
}