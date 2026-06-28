import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { makeApiUrl } from "../api/apiConfig";

function displayName(p) {
  if (!p) return "Chưa có dữ liệu";

  const parts = [
    p.sur_name,
    p.last_name,
    p.middle_name,
    p.first_name,
  ].filter(Boolean);

  return parts.join(" ") || p.full_name_vn || `ID ${p.id}`;
}

function birthText(p) {
  if (!p?.birth_date) return "";
  return ` (${p.birth_date.slice(0, 4)})`;
}

function PersonLine({ person }) {
  if (!person) return null;

  return (
    <li className="py-1">
      <span className="font-medium">
        {displayName(person)}
      </span>
      <span className="text-gray-500">
        {birthText(person)}
      </span>
    </li>
  );
}

function EmptyNote({ text = "🌼 Không có dữ liệu." }) {
  return (
    <div className="text-gray-500 italic text-sm py-2">
      {text}
    </div>
  );
}

export default function PersonFamilyOverviewPage() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadFamilyOverview();
  }, [id]);

  const loadFamilyOverview = async () => {
    try {
      setLoading(true);
      setError("");

      const res = await fetch(
        makeApiUrl(`/parent_child/person/${id}/family`),
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );

      if (!res.ok) {
        throw new Error("Không tải được chi tiết gia đình.");
      }

      const json = await res.json();
      setData(json);
    } catch (err) {
      console.error(err);
      setError(err.message || "Không tải được chi tiết gia đình.");
    } finally {
      setLoading(false);
    }
  };

  const special = data?.special_siblings || {};

  return (
    <div className="max-w-5xl mx-auto p-4 bg-white">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold text-blue-700">
          👪 Chi tiết gia đình
        </h1>

        <button
          onClick={() => navigate("/person")}
          className="px-4 py-2 bg-gray-700 text-white rounded hover:bg-gray-800"
        >
          ⬅️ Quay lại
        </button>
      </div>

      {loading && (
        <div className="text-center text-gray-600 py-6">
          Đang tải dữ liệu...
        </div>
      )}

      {error && (
        <div className="mb-4 p-3 bg-red-100 text-red-700 rounded">
          {error}
        </div>
      )}

      {!loading && data && (
        <>
          <div className="mb-4 p-4 border rounded bg-blue-">
            <div className="text-sm text-gray-500">Thành viên trung tâm</div>
            <div className="text-xl font-bold">
              {data.person?.gender === "female" ? "👩 " : "👨 "}
                {displayName(data.person)}
              <span className="text-gray-500 font-normal">
                {birthText(data.person)}
              </span>
            </div>
          </div>

          <section className="mb-6 border rounded p-4 bg-pink-50">
            <h2 className="text-xl font-bold mb-3 text-green-700">
              1. Hôn nhân và con cái
            </h2>

            {data.marriages?.length > 0 ? (
              <div className="space-y-4">
                {data.marriages.map((m, index) => (
                  <div
                    key={m.marriage_id}
                    className="border rounded p-3 bg-white shadow-sm"
                  >
                    <div className="font-semibold mb-2">
                    💍 Gia đình {index + 1}
                    </div>

                    <div className="mb-2">
                      <span className="text-gray-600">
                      ➕ Người phối ngẫu:{" "}
                      </span>
                      <span className="font-medium">
                        {displayName(m.spouse)}
                      </span>
                      <span className="text-gray-500">
                        {birthText(m.spouse)}
                      </span>
                    </div>

                    <div>
                      <div className="text-gray-600 mb-1">
                      👶 Các con
                      </div>

                      {m.children?.length > 0 ? (
                        <ul className="list-disc list-inside">
                          {m.children.map((child) => (
                            <PersonLine
                              key={child.id}
                              person={child}
                            />
                          ))}
                        </ul>
                      ) : (
                        <EmptyNote text="Chưa có dữ liệu con chung." />
                      )}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <EmptyNote text="Chưa có dữ liệu hôn nhân." />
            )}
          </section>

          <section className="border rounded p-4 bg-green-50">
            <h2 className="text-xl font-bold mb-3 text-purple-700">
                🌿 Quan hệ anh chị em khác nhánh
            </h2>

            <div className="grid md:grid-cols-2 gap-4">
              <div className="border rounded p-3">
                <h3 className="font-semibold mb-2">
                    👨 Cùng cha khác mẹ
                </h3>
                {special.same_father_different_mother?.length > 0 ? (
                  <ul className="list-disc list-inside">
                    {special.same_father_different_mother.map((p) => (
                      <PersonLine key={p.id} person={p} />
                    ))}
                  </ul>
                ) : (
                  <EmptyNote />
                )}
              </div>

              <div className="border rounded p-3">
                <h3 className="font-semibold mb-2">
                    👩 Cùng mẹ khác cha
                </h3>
                {special.same_mother_different_father?.length > 0 ? (
                  <ul className="list-disc list-inside">
                    {special.same_mother_different_father.map((p) => (
                      <PersonLine key={p.id} person={p} />
                    ))}
                  </ul>
                ) : (
                  <EmptyNote />
                )}
              </div>

              <div className="border rounded p-3">
                <h3 className="font-semibold mb-2">
                    👨❓ Chỉ biết cùng cha
                </h3>
                {special.known_same_father_only?.length > 0 ? (
                  <ul className="list-disc list-inside">
                    {special.known_same_father_only.map((p) => (
                      <PersonLine key={p.id} person={p} />
                    ))}
                  </ul>
                ) : (
                  <EmptyNote />
                )}
              </div>

              <div className="border rounded p-3">
                <h3 className="font-semibold mb-2">
                    👩❓ Chỉ biết cùng mẹ
                </h3>
                {special.known_same_mother_only?.length > 0 ? (
                  <ul className="list-disc list-inside">
                    {special.known_same_mother_only.map((p) => (
                      <PersonLine key={p.id} person={p} />
                    ))}
                  </ul>
                ) : (
                  <EmptyNote />
                )}
              </div>
            </div>
          </section>
        </>
      )}
    </div>
  );
}