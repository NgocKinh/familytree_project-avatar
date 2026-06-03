// ===============================================================
// File: Navbar.jsx (v7.1-Polished-LoginAware)
// ===============================================================

import React from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import {
  FaHome,
  FaUsers,
  FaSearch,
  FaUserPlus,
  FaHeart,
  FaSitemap,
  FaCog,
  FaBell,
  FaBookOpen,
  FaComments,
} from "react-icons/fa";

const Navbar = ({ role, currentUser, setRole, setCurrentUser }) => {
  const location = useLocation();
  const navigate = useNavigate();

  const isLoggedIn = !!currentUser;
  const isMember = ["member_basic", "member_close", "co_operator", "admin"].includes(role);
  const isAdminArea = ["co_operator", "admin"].includes(role);

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("currentUser");
    setRole("viewer");
    setCurrentUser(null);
    navigate("/login");
  };

  const roleColors = {
    viewer: "bg-gray-200 text-gray-700",
    member_basic: "bg-blue-100 text-blue-700",
    member_close: "bg-teal-100 text-teal-700",
    co_operator: "bg-orange-100 text-orange-700",
    admin: "bg-red-100 text-red-700",
  };

  const navClass = (path) =>
    `flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-semibold transition ${
      location.pathname === path
        ? "bg-white text-gray-900 shadow"
        : "text-gray-100 hover:bg-gray-700 hover:text-yellow-300"
    }`;

  const actionClass = (path) =>
    `flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-semibold transition ${
      location.pathname === path
        ? "bg-yellow-300 text-gray-900 shadow"
        : "bg-gray-700 text-white hover:bg-gray-600"
    }`;

  return (
    <nav className="sticky top-0 z-50 bg-gray-900 text-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 py-3">
        <div className="flex items-center justify-between gap-4">

          {/* LEFT */}
          <div className="flex items-center gap-4 flex-wrap">
            <Link
              to="/"
              className="text-lg font-bold text-yellow-300 hover:text-yellow-200 whitespace-nowrap"
            >
              📜 Gia Phả Tộc Trần
            </Link>

            <div className="flex items-center gap-2 flex-wrap">
              <Link to="/" className={navClass("/")}>
                <FaHome className="text-blue-400" />
                <span>Trang chủ</span>
              </Link>

              <Link to="/help" className={navClass("/help")}>
                <FaBookOpen className="text-indigo-300" />
                <span>Hướng dẫn</span>
              </Link>

              {isLoggedIn && (
                <>
                  <Link to="/person" className={navClass("/person")}>
                    <FaUsers className="text-green-400" />
                    <span>Danh sách thành viên</span>
                  </Link>

                  <Link to="/announcement" className={navClass("/announcement")}>
                    <FaBell className="text-orange-400" />
                    <span>Thông báo</span>
                  </Link>
                </>
              )}
            </div>

            {isMember && (
              <div className="flex items-center gap-2 flex-wrap border-l border-gray-700 pl-4">
                <Link to="/person/basic" className={actionClass("/person/basic")}>
                  <FaUserPlus />
                  <span>Thêm thành viên</span>
                </Link>

                <Link to="/relation_finder" className={actionClass("/relation_finder")}>
                  <FaSearch />
                  <span>Tìm quan hệ</span>
                </Link>

                <Link to="/parent_child" className={actionClass("/parent_child")}>
                  <FaSitemap />
                  <span>Cha-Con</span>
                </Link>

                <Link to="/marriage" className={actionClass("/marriage")}>
                  <FaHeart />
                  <span>Hôn nhân</span>
                </Link>

                <Link to="/family-setup" className={actionClass("/family-setup")}>
                  <FaUsers />
                  <span>Gia đình</span>
                </Link>

                <Link to="/internal-notification" className={actionClass("/internal-notification")}>
                  <span>📢</span>
                  <span>Nội bộ</span>
                </Link>

                <Link to="/feedback" className={actionClass("/feedback")}>
                  <FaComments />
                  <span>Góp ý</span>
                </Link>
              </div>
            )}

            {isAdminArea && (
              <div className="flex items-center gap-2 flex-wrap border-l border-gray-700 pl-4">
                <Link to="/admin" className={actionClass("/admin")}>
                  <FaCog />
                  <span>Quản trị</span>
                </Link>
              </div>
            )}
          </div>

          {/* RIGHT */}
          <div className="flex items-center gap-3 shrink-0">
            {!isLoggedIn ? (
              <Link
                to="/login"
                className="px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-700 text-white text-sm font-semibold shadow"
              >
                🔐 Đăng nhập
              </Link>
            ) : (
              <>
                <span
                  className={`px-3 py-2 rounded-lg text-sm font-semibold ${
                    roleColors[role] || "bg-gray-200 text-gray-700"
                  }`}
                >
                  👤 {currentUser?.full_name || currentUser?.username || role}
                </span>

                <button
                  type="button"
                  onClick={handleLogout}
                  className="px-4 py-2 rounded-lg bg-red-500 hover:bg-red-600 text-white text-sm font-semibold shadow"
                >
                  Đăng xuất
                </button>
              </>
            )}
          </div>

        </div>
      </div>
    </nav>
  );
};

export default Navbar;

// // ===============================================================
// // File: Navbar.jsx (v6.5.1-CompactRoles-NoPending)
// // Mô tả:
// //   - Giữ nguyên giao diện 100%
// //   - 🟡 [REMOVED]: Nút "📥 Chờ Duyệt"
// // ===============================================================

// import React from "react";
// import { Link, useLocation, useNavigate } from "react-router-dom";
// import {
//   FaHome,
//   FaUsers,
//   FaSearch,
//   FaUserPlus,
//   FaHeart,
//   FaSitemap,
//   FaCog,
//   FaBell,
// } from "react-icons/fa";
// import { hasKey } from "../utils/permissions";
// import { ROLE_KEYS } from "../roleKeys";

// const Navbar = ({ role, currentUser, setRole, setCurrentUser }) => {
//   const location = useLocation();
//   const navigate = useNavigate();

//   const handleLogout = () => {
//     localStorage.removeItem("token");
//     localStorage.removeItem("currentUser");
//     setRole("viewer");
//     setCurrentUser(null);
//     navigate("/login");
//   };
//   const roleColors = {
//     viewer: "bg-gray-200 text-gray-700",
//     member_basic: "bg-blue-100 text-blue-600",
//     member_close: "bg-teal-100 text-teal-600",
//     co_operator: "bg-orange-100 text-orange-600",
//     admin: "bg-red-100 text-red-600",
//   };


//   return (
//     <nav className="sticky top-0 z-50 bg-gray-800 text-white shadow-md">
//       <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">

//         {/* Logo */}
//         <Link to="/" className="font-bold text-lg hover:text-yellow-400">
//           📜 Gia Phả Tộc Trần
//         </Link>

//         {/* Menu chính */}
//         <div className="flex flex-wrap items-center gap-5 font-medium">

//           {/* Trang chủ */}
//           <Link
//             to="/"
//             className={`flex items-center gap-2 hover:text-yellow-400 transition ${location.pathname === "/" ? "underline underline-offset-4" : ""
//               }`}
//           >
//             <FaHome className="text-blue-400" />
//             <span>Trang Chủ</span>
//           </Link>

//           {/* 🔔 Thông báo */}
//           <Link
//             to="/announcement"
//             className={`flex items-center gap-2 hover:text-yellow-400 transition ${location.pathname === "/announcement"
//               ? "underline underline-offset-4"
//               : ""
//               }`}
//           >
//             <FaBell className="text-orange-400" />
//             <span>Thông Báo</span>
//           </Link>
//           {/* 📢 Thông báo nội bộ */}
//           {["member_basic", "member_close", "co_operator", "admin"].includes(role) && (
//             <Link
//               to="/internal-notification"
//               className={`flex items-center gap-2 hover:text-yellow-400 transition ${
//                 location.pathname === "/internal-notification"
//                   ? "underline underline-offset-4"
//                   : ""
//               }`}
//             >
//               <span className="text-blue-400">📢</span>
//               <span>Nội Bộ</span>
//             </Link>
//           )}
//           {/* 👥 Danh sách thành viên */}
//           <Link
//             to="/person"
//             className={`flex items-center gap-2 hover:text-yellow-400 transition ${location.pathname === "/person"
//               ? "underline underline-offset-4"
//               : ""
//               }`}
//           >
//             <FaUsers className="text-green-400" />
//             <span>Danh Sách Thành Viên</span>
//           </Link>

//           {/* 🔍 Tìm Mối Quan Hệ */}
//           {role !== "viewer" && (
//             <Link
//               to="/relation_finder"
//               className={`flex items-center gap-2 hover:text-yellow-400 transition ${location.pathname === "/relation_finder"
//                 ? "underline underline-offset-4"
//                 : ""
//                 }`}
//             >
//               <FaSearch className="text-orange-400" />
//               <span>Tìm Mối Quan Hệ</span>
//             </Link>
//           )}

//           {/* 🟩 Thêm Thành Viên */}
//           {["member_basic", "member_close", "co_operator", "admin"].includes(role) && (
//             <Link
//               to="/person/basic"
//               className={`flex items-center gap-2 bg-green-500 hover:bg-green-600 text-white px-3 py-1.5 rounded-lg shadow-md transition ${location.pathname === "/person/add"
//                 ? "ring-2 ring-green-300"
//                 : ""
//                 }`}
//             >
//               <FaUserPlus />
//               <span>Thêm Thành Viên</span>
//             </Link>
//           )}

//           {/* 🟡 [REMOVED] Nút Chờ Duyệt */}
//           {/* 
//           {["member_close", "co_operator", "admin"].includes(role) && (
//             <Link
//               to="/pending"
//               className="flex items-center gap-2 bg-purple-600 hover:bg-purple-700 text-white px-3 py-1.5 rounded shadow transition"
//             >
//               <span>📥 Chờ Duyệt</span>
//             </Link>
//           )}
//           */}

//           {/* 🟨 Cha–Con + 🩷 Hôn Nhân */}
//           {["member_basic", "member_close", "co_operator", "admin"].includes(role) && (
//             <>
//               <Link
//                 to="/parent_child"
//                 className={`flex items-center gap-2 bg-amber-500 hover:bg-amber-600 text-white px-3 py-1.5 rounded-lg shadow-md transition ${location.pathname === "/parent_child"
//                   ? "ring-2 ring-amber-300"
//                   : ""
//                   }`}
//               >
//                 <FaSitemap />
//                 <span>Quan Hệ Cha–Con</span>
//               </Link>

//               <Link
//                 to="/marriage"
//                 className={`flex items-center gap-2 bg-rose-500 hover:bg-rose-600 text-white px-3 py-1.5 rounded-lg shadow-md transition ${location.pathname === "/marriage"
//                   ? "ring-2 ring-rose-300"
//                   : ""
//                   }`}
//               >
//                 <FaHeart />
//                 <span>Quan Hệ Hôn Nhân</span>
//               </Link>
//             </>
//           )}

//           {["member_basic", "member_close", "co_operator", "admin"].includes(role) && (
//             <Link
//               to="/family-setup"
//               className={`flex items-center gap-2 bg-emerald-500 hover:bg-emerald-600 text-white px-3 py-1.5 rounded-lg shadow-md transition ${location.pathname === "/family-setup"
//                   ? "ring-2 ring-emerald-300"
//                   : ""
//                 }`}
//             >
//               <FaUsers />
//               <span>Thiết lập Gia đình</span>
//             </Link>
//           )}


//           {/* ⚙️ Quản trị */}
//           {["co_operator", "admin"].includes(role) && (
//             <Link
//               to="/admin"
//               className={`flex items-center gap-2 hover:text-yellow-400 transition ${location.pathname === "/admin"
//                 ? "underline underline-offset-4"
//                 : ""
//                 }`}
//             >
//               <FaCog className="text-gray-300" />
//               <span>Quản Trị</span>
//             </Link>
//           )}
//         </div>

//         {/* Login / Logout */}
//         <div className="flex items-center gap-3">
//           {role === "viewer" ? (
//             <Link
//               to="/login"
//               className="px-3 py-1.5 rounded bg-blue-600 hover:bg-blue-700 text-white text-sm font-semibold"
//             >
//               Đăng nhập
//             </Link>
//           ) : (
//             <>
//               <span
//                 className={`px-2 py-1 rounded text-sm font-semibold ${
//                   roleColors[role] || "bg-gray-200 text-gray-700"
//                 }`}
//               >
//                 {currentUser?.full_name || currentUser?.username || role.toUpperCase()}
//               </span>

//               <button
//                 onClick={handleLogout}
//                 className="px-3 py-1.5 rounded bg-red-500 hover:bg-red-600 text-white text-sm font-semibold"
//               >
//                 Đăng xuất
//               </button>
//             </>
//           )}
//         </div>
//       </div>
//     </nav>
//   );
// };

// export default Navbar;
