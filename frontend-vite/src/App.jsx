// ======================================================
// File: src/App.jsx (v3.0-FINAL-CLEAN)
// ======================================================

import React, { useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from "react-router-dom";
import ProtectedRouteV6 from "./components/ProtectedRouteV6";
import Navbar from "./components/Navbar";
import axios from "axios";
import { API_BASE_URL } from "./api/apiConfig";

// Pages
import Home from "./pages/Home";
import PersonList from "./pages/PersonList.jsx";
import AddPersonPage from "./pages/AddPersonPage.jsx";

import TreePage from "./pages/TreePage.jsx";   // ✔ ONLY ONE IMPORT – FIXED
import RelationFinder from "./pages/RelationFinder";
import RelationFinderPage from "./pages/RelationFinderPage.jsx";

import LinePage from "./pages/LinePage";
import AdminPage from "./pages/AdminPage";
import AnnouncementPage from "./pages/AnnouncementPage";
import AnnouncementAdminPage from "./pages/AnnouncementAdminPage";
import InternalNotificationPage from "./pages/InternalNotificationPage";
import AdminFeedbackPage from "./pages/AdminFeedbackPage";
import FeedbackPage from "./pages/FeedbackPage";
import MarriagePage from "./pages/MarriagePage";
import ParentChildPage from "./pages/ParentChildPage";

import PendingPage from "./pages/PendingPage.jsx";
import PendingReviewPage from "./pages/PendingReviewPage.jsx";

import PersonDetailPage from "./pages/PersonDetailPage.jsx";

import FamilySetupPage from "./pages/FamilySetupPage";
import LoginPage from "./pages/LoginPage.jsx";
import AdminUsersPage from "./pages/AdminUsersPage.jsx";
import HelpPage from "./pages/HelpPage.jsx";
// ======================================================
// App
// ======================================================
export default function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}
// ======================================================
// ACL GROUPS
// ======================================================

const ALL_LOGIN_ROLES = [
  "viewer",
  "member_basic",
  "co_operator",
  "admin",
];

const MEMBER_ROLES = [
  "member_basic",
  "co_operator",
  "admin",
];

const ADMIN_AREA_ROLES = [
  "co_operator",
  "admin",
];

function AppContent() {
  const [role, setRole] = useState("viewer");
  const [currentUser, setCurrentUser] = useState(null);
  const [authLoading, setAuthLoading] = useState(true);
  const location = useLocation();
  useEffect(() => {
    const token = localStorage.getItem("token");
  
    if (!token) {
      setRole("viewer");
      setCurrentUser(null);
      setAuthLoading(false);
      return;
    }
  
    axios
      .get(`${API_BASE_URL}/auth/me`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .then((res) => {
        setRole(res.data?.role || "viewer");
        setCurrentUser(res.data || null);
      })
      .catch((err) => {
        if (err?.response?.status === 401) {
          alert("Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại.");
      
          localStorage.removeItem("token");
          setCurrentUser(null);
          setRole("viewer");
      
          window.location.replace("/");
          return;
        }
      
        console.error("Lỗi kiểm tra đăng nhập:", err);
      
        localStorage.removeItem("token");
        setCurrentUser(null);
        setRole("viewer");
        window.location.replace("/");
      })
      .finally(() => {
        setAuthLoading(false);
      });
  }, []);
  const hideNavbarRoutes = [
    "/person",
    "/parent_child",
    "/marriage",
    "/relation_finder",
    "/person/basic/",
    "/announcement",
    "/internal-notification",
    "/feedback",
    "/admin",
    "/pending",
    "/help",
    "/family-setup",
  ];
  
  const shouldHideNavbar =
    location.pathname.startsWith("/tree") ||
    hideNavbarRoutes.some((route) =>
      location.pathname.startsWith(route)
    );
  if (authLoading) {
    return (
      <div className="p-6 text-center text-gray-600">
        ⏳ Đang kiểm tra quyền truy cập...
      </div>
    );
  }
  return (
    <>
      {!shouldHideNavbar && (
        <Navbar
          role={role}
          currentUser={currentUser}
          setRole={setRole}
          setCurrentUser={setCurrentUser}
        />
      )}

      <div
        className={
          location.pathname.startsWith("/tree")
            ? "w-full p-0 m-0"
            : shouldHideNavbar
            ? "w-full p-4"
            : "container mx-auto p-4"
        }
      >
        <Routes>

          {/* HOME */}
          <Route path="/" element={<Home role={role} />} />
          <Route path="/home" element={<Home role={role} />} />
          <Route
            path="/login"
            element={
              currentUser
                ? <Navigate to="/" replace />
                : (
                    <LoginPage
                      setRole={setRole}
                      setCurrentUser={setCurrentUser}
                    />
                  )
            }
          />
          {/* RELATION FINDER */}

          <Route
            path="/relation_finder"
            element={
              <ProtectedRouteV6
                role={role}
                allowRoles={MEMBER_ROLES}
                currentUser={currentUser}
                redirectTo="/"
              >
                <RelationFinderPage />
              </ProtectedRouteV6>
            }
          />

          {/* LINEAGE */}
          <Route path="/line" element={<LinePage />} />

          {/* ADMIN */}
          <Route
            path="/admin"
            element={
              <ProtectedRouteV6
                role={role}
                allowRoles={ADMIN_AREA_ROLES}
                currentUser={currentUser}
                redirectTo="/"
              >
                <AdminPage />
              </ProtectedRouteV6>
            }
          />
          <Route
            path="/admin/announcement"
            element={
              <ProtectedRouteV6
                role={role}
                allowRoles={ADMIN_AREA_ROLES}
                currentUser={currentUser}
                redirectTo="/"
              >
                <AnnouncementAdminPage />
              </ProtectedRouteV6>
            }
          />
          <Route
            path="/admin/feedback"
            element={
              <ProtectedRouteV6
                role={role}
                allowRoles={ADMIN_AREA_ROLES}
                currentUser={currentUser}
                redirectTo="/"
              >
                <AdminFeedbackPage />
              </ProtectedRouteV6>
            }
          />
          <Route
            path="/admin/users"
            element={
              <ProtectedRouteV6
                role={role}
                allowRoles={["admin"]}
                currentUser={currentUser}
                redirectTo="/"
              >
                <AdminUsersPage currentUser={currentUser} />
              </ProtectedRouteV6>
            }
          />
          <Route
            path="/internal-notification"
            element={
              <ProtectedRouteV6
                role={role}
                allowRoles={MEMBER_ROLES}
                currentUser={currentUser}
              >
                <InternalNotificationPage />
              </ProtectedRouteV6>
            }
          />
          <Route
            path="/feedback"
            element={
              <ProtectedRouteV6
                role={role}
                allowRoles={MEMBER_ROLES}
                currentUser={currentUser}
                redirectTo="/"
              >
                <FeedbackPage />
              </ProtectedRouteV6>
            }
          />
          {/* PERSON LIST */}
          <Route
            path="/person"
            element={
              <ProtectedRouteV6
                role={role}
                allowRoles={ALL_LOGIN_ROLES}
                currentUser={currentUser}
                redirectTo="/"
              >
                <PersonList role={role} />
              </ProtectedRouteV6>
            }
          />

          {/* ADD / EDIT PERSON */}
          <Route
            path="/person/basic"
            element={
              <ProtectedRouteV6
                role={role}
                allowRoles={MEMBER_ROLES}
                currentUser={currentUser}
                redirectTo="/"
              >
                <AddPersonPage role={role} />
              </ProtectedRouteV6>
            }
          />

          <Route
            path="/person/basic/:id"
            element={
              <ProtectedRouteV6
                role={role}
                allowRoles={MEMBER_ROLES}
                currentUser={currentUser}
                redirectTo="/"
              >
                <AddPersonPage role={role} />
              </ProtectedRouteV6>
            }
          />

          {/* DETAIL */}
          <Route
            path="/person/detail/:id"
            element={
              <ProtectedRouteV6
                role={role}
                allowRoles={ALL_LOGIN_ROLES}
                currentUser={currentUser}
                redirectTo="/"
              >
                <PersonDetailPage />
              </ProtectedRouteV6>
            }
          />

          {/* TREE VIEW */}
          <Route
            path="/tree/:personId"
            element={
              <ProtectedRouteV6
                role={role}
                allowRoles={ALL_LOGIN_ROLES}
                currentUser={currentUser}
                redirectTo="/"
              >
                <TreePage />
              </ProtectedRouteV6>
            }
          />

          {/* ANNOUNCEMENT */}
          <Route
            path="/announcement"
            element={
              <ProtectedRouteV6
                role={role}
                allowRoles={ALL_LOGIN_ROLES}
                currentUser={currentUser}
                redirectTo="/"
              >
                <AnnouncementPage />
              </ProtectedRouteV6>
            }
          />

          {/* RELATIONS */}
          <Route
            path="/marriage"
            element={
              <ProtectedRouteV6
                role={role}
                allowRoles={MEMBER_ROLES}
                currentUser={currentUser}
                redirectTo="/"
              >
                <MarriagePage role={role} />
              </ProtectedRouteV6>
            }
          />

          <Route
            path="/parent_child"
            element={
              <ProtectedRouteV6
                role={role}
                allowRoles={MEMBER_ROLES}
                currentUser={currentUser}
                redirectTo="/"
              >
                <ParentChildPage role={role} />
              </ProtectedRouteV6>
            }
          />

          <Route
            path="/family-setup"
            element={
              <ProtectedRouteV6
                role={role}
                allowRoles={MEMBER_ROLES}
                currentUser={currentUser}
                redirectTo="/"
              >
                <FamilySetupPage />
              </ProtectedRouteV6>
            }
          />
            
          {/* PENDING APPROVAL */}
          <Route
            path="/pending"
            element={
              <ProtectedRouteV6
                role={role}
                allowRoles={MEMBER_ROLES}
                currentUser={currentUser}
                redirectTo="/"
              >
                <PendingPage role={role} />
              </ProtectedRouteV6>
            }
          />

          <Route
            path="/pending/review/:id"
            element={
              <ProtectedRouteV6
                role={role}
                allowRoles={MEMBER_ROLES}
                currentUser={currentUser}
                redirectTo="/"
              >
                <PendingReviewPage role={role} />
              </ProtectedRouteV6>
            }
          />
          {/* HELP */}
          <Route
            path="/help"
            element={
              <ProtectedRouteV6
                role={role}
                allowRoles={ALL_LOGIN_ROLES}
                currentUser={currentUser}
                redirectTo="/"
              >
                <HelpPage />
              </ProtectedRouteV6>
            }
          />
          {/* 404 */}
          <Route path="*" element={<Navigate to="/" />} />

        </Routes>
      </div>
    </>
  );
}
