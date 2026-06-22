import { useEffect, useState, useMemo } from "react";
import { useParams, useNavigate } from "react-router-dom";

import { getFamilyTree } from "../api/treeApi";
import { getAvatarURL, handleAvatarError } from "../utils/avatarEngine";
import { formatName } from "../utils/formatName";
import { API_BASE_URL } from "../api/apiConfig";
/* ================= Avatar ================= */

function Avatar({ person, size = 80, onClick }) {

  if (!person) return null;

  /* ✅ [CHANGE 1]: Dùng trực tiếp person để avatarEngine tự xử lý id/person_id*/
  const src = getAvatarURL(person);
  
  const onError = (e) => {
    handleAvatarError(e, person?.gender);
  };

  return (
    <img
      src={src}
      onError={onError}
      onClick={onClick} 
      loading="lazy"
      className="rounded-full shadow-md cursor-pointer hover:scale-105 transition bg-white"
      style={{ width: size, height: size, objectFit: "cover" }}
      alt=""
    />
  );
}

/* ================= Person ================= */

function Person({ person, go, size = 60 }) {

  if (!person) return null;

  const name =
      formatName(person, { mode: "full", showAlias: false }) ||
      person.name ||
      person.full_name ||
      "Không rõ";

  const onClick = person?.person_id ? () => go(person.person_id) : undefined;

  return (
    <div className="flex flex-col items-center w-[150px]">

      <Avatar person={person} size={size} onClick={onClick} />

      <p className="mt-2 text-sm font-medium text-center leading-tight break-words w-full">
        {name}
      </p>

      {(person.birth_year || person.death_year) && (
        <p className="text-sm text-gray-500">
          {person.birth_year || "?"} – {person.death_year || "?"}
        </p>
      )}
    </div>
  );
}

/* ================= Helpers ================= */

function ensureTwo(list = []) {

  const fake = { person_id: "fake_unknown", name: "Không rõ", gender: "other" };

  if (list.length === 0) return [fake, fake];
  if (list.length === 1) return [list[0], fake];

  return list.slice(0, 2);
}

function heartIcon(status) {

  switch (status) {
    case "married": return "❤️";
    case "separated": return "💚";
    case "divorced": return "💔";
    case "widowed": return "🖤";
    default: return "➕";
  }

}

/* ================= Page ================= */

export default function TreePage() {

  const { personId } = useParams();
  const navigate = useNavigate();

  const [tree, setTree] = useState(null);
  const [loading, setLoading] = useState(true);

  const go = async (pid) => {
    if (!pid) return;
  
    try {
      const token = localStorage.getItem("token");
  
      const res = await fetch(`${API_BASE_URL}/auth/check-near-access`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          target_person_id: pid,
          action: "tree:view",
        }),
      });
  
      const data = await res.json();
  
      if (res.ok && data.allowed) {
        navigate(`/tree/${pid}`);
        return;
      }
  
      alert("Bạn chỉ được xem cây gia phả của người thân gần.");
    } catch (err) {
      console.error("❌ Không kiểm tra được quyền xem cây:", err);
      alert("Không kiểm tra được quyền truy cập cây gia phả.");
    }
  };
  /* ===== Load tree ===== */
  useEffect(() => {
    let alive = true;
    const load = async () => {
      setLoading(true);
      try {
        const data = await getFamilyTree(personId);
        if (!alive) return;
        setTree(data);
      } finally {
        if (alive) setLoading(false);
      }
    };
    load();
    return () => { alive = false };
  }, [personId]);

  /* ===== Extract data safely ===== */

  const {
    center,
    spouse,
    marriage_status,
    father_parents = [],
    mother_parents = [],
    children_common = []
  } = tree || {};

  /* ===== Parents ===== */

  const safeFather = useMemo(
    () => ensureTwo(father_parents),
    [father_parents]
  );

  const safeMother = useMemo(
    () => ensureTwo(mother_parents),
    [mother_parents]
  );

  /* ===== Sort children ===== */

  const childrenSorted = useMemo(() => {
    return [...children_common].sort((a, b) => {
      const yearA = a.birth_year ?? 9999;
      const yearB = b.birth_year ?? 9999;
  
      if (yearA !== yearB) {
        return yearA - yearB;
      }
  
      const boA = a.birth_order ?? 9999;
      const boB = b.birth_order ?? 9999;
  
      return boA - boB;
    });
  }, [children_common]);

  /* ===== Couple position ===== */

  const fake = { person_id: "fake_spouse", name: "Không rõ", gender: "other" };

  const spouseObj = spouse || fake;

  const left =
    center?.gender === "female"
      ? spouseObj
      : center;

  const right =
    center?.gender === "female"
      ? center
      : spouseObj;


  /* ===== Loading ===== */

  if (loading || !tree)
    return (
      <p className="p-5 text-center">
        Đang tải dữ liệu…
      </p>
    );


  /* ================= Render ================= */

  return (

    <div className="w-full min-h-screen flex flex-col items-center py-6 select-none relative bg-slate-50">

      {/* 🔵 [ADDED]: Nút quay về Trang chủ */}
      <button
        onClick={() => navigate("/")}
        className="absolute top-4 left-4 bg-white px-3 py-1 rounded shadow hover:bg-gray-100"
      >
        🏠 Home
      </button>

      {/* ================= Parents ================= */}

      <div className="flex justify-between w-full max-w-6xl px-10">

        {/* Bên Nam */}
        <div className="flex flex-col items-center w-1/2">

          <p className="text-blue-700 font-medium mb-3 text-lg">
            Cha mẹ bên Nam
          </p>

          <div className="flex gap-6">
            {safeFather.map((p, i) => (
              <Person key={p.person_id || i} person={p} go={go} />
            ))}
          </div>

        </div>

        {/* Bên Nữ */}
        <div className="flex flex-col items-center w-1/2">

          <p className="text-pink-700 font-medium mb-3 text-lg">
            Cha mẹ bên Nữ
          </p>

          <div className="flex gap-6">
            {safeMother.map((p, i) => (
              <Person key={p.person_id || i} person={p} go={go} />
            ))}
          </div>

        </div>

      </div>
      {/* 🔵 [ADDED]: Đường nối từ cha mẹ xuống cặp vợ chồng */}
      <div className="w-px h-4 bg-gray-300 mt-4"></div>
      {/* ================= Couple ================= */}

      <div className="flex items-center justify-center mt-2 gap-14">

        <Person person={left} size={100} go={go} />

        <div className="text-4xl">
          {heartIcon(marriage_status)}
        </div>

        <Person person={right} size={100} go={go} />

      </div>
      {/* 🔵 [ADDED]: Đường nối từ vợ chồng xuống con */}
      {childrenSorted.length > 0 && (
        <div className="w-px h-4 bg-gray-300 mt-4"></div>
      )}
      {/* ================= Children ================= */}

      {childrenSorted.length > 0 && (

        <>
          <h3 className="mt-2 text-lg font-semibold text-gray-700">
            Con
          </h3>

          <div className="flex flex-wrap justify-center gap-x-10 gap-y-8 mt-6 max-w-5xl">

            {childrenSorted.map((c) => (
              <Person key={c.person_id} person={c} go={go} />
            ))}

          </div>
        </>

      )}

    </div>

  );
}     