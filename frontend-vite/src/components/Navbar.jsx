// ===============================================================
// File: Navbar.jsx (v7.1-Polished-LoginAware)
// ===============================================================

import React, { useEffect, useState } from "react";
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
  FaBars,
  FaTimes,
} from "react-icons/fa";

const Navbar = ({ role, currentUser, setRole, setCurrentUser }) => {
  const location = useLocation();
  const navigate = useNavigate();

  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    setMenuOpen(false);
  }, [location.pathname]);

  const isLoggedIn = !!currentUser;
  const isMember = ["member_basic", "co_operator", "admin"].includes(role);
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
        <div className="flex flex-wrap items-center justify-between gap-4">

          {/* LEFT */}
          <div className="flex w-full min-w-0 items-center justify-between gap-4 flex-wrap md:flex-1 md:justify-start">
            <Link
              to="/"
              className="text-lg font-bold text-yellow-300 hover:text-yellow-200 whitespace-nowrap"
            >
              📜 Gia Phả Tộc Trần
            </Link>
            <button
              type="button"
              onClick={() => setMenuOpen((open) => !open)}
              className="md:hidden flex items-center gap-2 rounded-lg bg-gray-700 px-3 py-2 text-sm font-semibold text-white"
              aria-expanded={menuOpen}
              aria-label={menuOpen ? "Đóng menu" : "Mở menu"}
            >
              {menuOpen ? <FaTimes /> : <FaBars />}
              <span>Menu</span>
            </button>
            <div
              className={`${
                menuOpen ? "flex" : "hidden"
              } w-full flex-col items-stretch gap-2 md:flex md:w-auto md:flex-row md:items-center md:flex-wrap`}
            >
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
              <div
                className={`${
                  menuOpen ? "flex" : "hidden"
                } w-full flex-col items-stretch gap-2 border-t border-gray-700 pt-3 md:flex md:w-auto md:flex-row md:items-center md:flex-wrap md:border-l md:border-t-0 md:pl-4 md:pt-0`}
              >
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
              <div
                className={`${
                  menuOpen ? "flex" : "hidden"
                } w-full flex-col items-stretch gap-2 border-t border-gray-700 pt-3 md:flex md:w-auto md:flex-row md:items-center md:flex-wrap md:border-l md:border-t-0 md:pl-4 md:pt-0`}
              >
                <Link to="/admin" className={actionClass("/admin")}>
                  <FaCog />
                  <span>Quản trị</span>
                </Link>
              </div>
            )}
          </div>

          {/* RIGHT */}
          <div
            className={`${
              menuOpen ? "flex" : "hidden"
            } w-full flex-col gap-2 border-t border-gray-700 pt-3 md:flex md:w-auto md:flex-row md:items-center md:border-t-0 md:pt-0 md:shrink-0`}
          >
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
