import { useEffect, useState, useMemo } from "react";
import { useParams, useNavigate } from "react-router-dom";

import { getFamilyTree } from "../api/treeApi";
import { getAvatarURL, handleAvatarError } from "../utils/avatarEngine";
import { formatName } from "../utils/formatName";

/* ================= Avatar ================= */

function Avatar({ person, size = 80, onClick }) {

  if (!person) return null;

  const src = getAvatarURL({
    ...person,
    person_id: person.person_id
  });  
  console.log("TREE PERSON:", person);
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

function Person({ person, go, size = 80 }) {

  if (!person) return null;

  const name =
    person.name ||
    person.full_name ||
    formatName(person, "full") ||
    "Không rõ";

  const onClick = person?.person_id ? () => go(person.person_id) : undefined;

  return (
    <div className="flex flex-col items-center w-[180px]">

      <Avatar person={person} size={size} onClick={onClick} />

      <p className="mt-2 font-medium text-center">
        {name}
      </p>

      <p className="text-sm text-gray-500">
        {person.birth_year ?? "?"} – {person.death_year ?? ""}
      </p>

    </div>
  );
}


/* ================= Helpers ================= */

function ensureTwo(list = []) {

  const fake = { name: "Không rõ", gender: "other" };

  if (list.length === 0) return [fake, fake];
  if (list.length === 1) return [list[0], fake];

  return list.slice(0, 2);
}


function heartIcon(status) {

  switch (status) {
    case "married": return "❤️";
    case "cohabitation": return "💛";
    case "separated": return "💚";
    case "divorced": return "💔";
    case "widowed": return "🖤";
    default: return "➕";
  }

}


/* ================= Page ================= */

export default function TreePage() {

  const { id } = useParams();
  const navigate = useNavigate();

  const [tree, setTree] = useState(null);
  const [loading, setLoading] = useState(true);

  const go = (pid) => navigate(`/tree/${pid}`);


  /* ===== Load tree ===== */

  useEffect(() => {

    let alive = true;

    const load = async () => {

      setLoading(true);

      try {

        const data = await getFamilyTree(id);

        if (!alive) return;

        setTree(data);

      } finally {

        if (alive) setLoading(false);

      }

    };

    load();

    return () => { alive = false };

  }, [id]);


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

    return [...children_common].sort(
      (a, b) => (a.birth_year || 9999) - (b.birth_year || 9999)
    );

  }, [children_common]);


  /* ===== Couple position ===== */

  const fake = { name: "Không rõ", gender: "other" };

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

    <div className="w-full flex flex-col items-center py-10 select-none">


      {/* Parents */}

      <div className="flex justify-between w-full px-32">

        <div className="flex flex-col items-center w-1/2">

          <p className="text-blue-700 font-medium mb-3 text-lg">
            Cha mẹ bên Nam
          </p>

          <div className="flex gap-10">
            {safeFather.map((p, i) => (
              <Person key={p.person_id || i} person={p} go={go} />
            ))}
          </div>

        </div>


        <div className="flex flex-col items-center w-1/2">

          <p className="text-pink-700 font-medium mb-3 text-lg">
            Cha mẹ bên Nữ
          </p>

          <div className="flex gap-10">
            {safeMother.map((p, i) => (
              <Person key={p.person_id || i} person={p} go={go} />
            ))}
          </div>

        </div>

      </div>


      {/* Couple */}

      <div className="flex items-center justify-center mt-14 gap-20">

        <Person person={left} size={140} go={go} />

        <div className="text-6xl">
          {heartIcon(marriage_status)}
        </div>

        <Person person={right} size={140} go={go} />

      </div>


      {/* Children */}

      {childrenSorted.length > 0 && (

        <>
          <h3 className="mt-16 text-lg font-semibold">
            Con
          </h3>

          <div className="flex flex-wrap justify-center gap-10 mt-8">

            {childrenSorted.map((c) => (
              <Person key={c.person_id} person={c} go={go} />
            ))}

          </div>

        </>

      )}

    </div>

  );
}