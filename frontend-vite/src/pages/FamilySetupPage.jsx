import { useState } from "react";
import { useNavigate } from "react-router-dom";
import AssignParentForm from "../components/clean/AssignParentForm";
import AssignChildToParentForm from "../components/clean/AssignChildToParentForm";

export default function FamilySetupPage() {
  const [activeTab, setActiveTab] = useState("child_to_family");
  const navigate = useNavigate();
  return (
    <div className="max-w-6xl mx-auto p-4 bg-white shadow-md rounded-lg">
      <div className="relative mb-4">
        <button
          type="button"
          onClick={() => navigate("/")}
          className="absolute left-0 top-0 px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded"
        >
          🏠 Home
        </button>

        <h2 className="text-2xl font-bold text-center text-green-600">
          🧠 Thiết lập Quan hệ Gia đình
        </h2>
      </div>

      <div className="flex justify-center gap-3 mb-4">
        <button
          type="button"
          onClick={() => setActiveTab("child_to_family")}
          className={`px-4 py-2 rounded font-semibold ${
            activeTab === "child_to_family"
              ? "bg-green-600 text-white"
              : "bg-gray-200 text-gray-700 hover:bg-gray-300"
          }`}
        >
          👶 Quan Hệ Con & Gia Đình
        </button>

        <button
          type="button"
          onClick={() => setActiveTab("parent_to_child")}
          className={`px-4 py-2 rounded font-semibold ${
            activeTab === "parent_to_child"
              ? "bg-blue-600 text-white"
              : "bg-gray-200 text-gray-700 hover:bg-gray-300"
          }`}
        >
          👨‍👩‍👧 Quan Hệ Cha/Mẹ & Con
        </button>
      </div>

      {activeTab === "child_to_family" && <AssignParentForm />}
      {activeTab === "parent_to_child" && <AssignChildToParentForm />}
    </div>
  );
}