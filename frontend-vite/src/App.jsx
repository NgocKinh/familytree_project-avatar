// ======================================================
// File: src/App.jsx (v3.0-FINAL-CLEAN)
// ======================================================

import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from "react-router-dom";
import ProtectedRouteV6 from "./components/ProtectedRouteV6";
import Navbar from "./components/Navbar";

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

function AppContent() {
  const [role, setRole] = useState(localStorage.getItem("role") || "viewer");
  const location = useLocation();
  const hideNavbarRoutes = [
    "/person",
    "/parent_child",
    "/marriage",
    "/relation_finder",
    "/person/basic/",
    "/announcement",
    "/internal-notification",
    "/feedback",
    "/admin/feedback",
  ];
  
  const shouldHideNavbar =
    location.pathname.startsWith("/tree") ||
    hideNavbarRoutes.some((route) =>
      location.pathname.startsWith(route)
    );

  return (
    <>
      {!shouldHideNavbar && (
        <Navbar role={role} setRole={setRole} />
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

          {/* RELATION FINDER */}

          <Route
            path="/relation_finder"
            element={
              <ProtectedRouteV6
                role={role}
                allowRoles={["member_basic", "member_close", "co_operator", "admin"]}
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
                allowRoles={["co_operator", "admin"]}
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
                allowRoles={["co_operator", "admin"]}
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
                allowRoles={["co_operator", "admin"]}
                redirectTo="/"
              >
                <AdminFeedbackPage />
              </ProtectedRouteV6>
            }
          />
          <Route
            path="/internal-notification"
            element={
              <ProtectedRouteV6
                role={role}
                allowRoles={["member_basic", "member_close", "co_operator", "admin"]}
                redirectTo="/"
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
                allowRoles={["member_basic", "member_close", "co_operator", "admin"]}
                redirectTo="/"
              >
                <FeedbackPage />
              </ProtectedRouteV6>
            }
          />
          {/* PERSON LIST */}
          <Route path="/person" element={<PersonList role={role} />} />

          {/* ADD / EDIT PERSON */}
          <Route
            path="/person/basic"
            element={
              <ProtectedRouteV6
                role={role}
                allowRoles={["member_basic", "member_close", "co_operator", "admin"]}
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
                allowRoles={["member_basic", "member_close", "co_operator", "admin"]}
                redirectTo="/"
              >
                <AddPersonPage role={role} />
              </ProtectedRouteV6>
            }
          />

          {/* DETAIL */}
          <Route path="/person/detail/:id" element={<PersonDetailPage />} />

          {/* TREE VIEW */}
          <Route path="/tree/:personId" element={<TreePage />} />  {/* ✔ PARAM FIXED */}

          {/* ANNOUNCEMENT */}
          <Route path="/announcement" element={<AnnouncementPage />} />

          {/* RELATIONS */}
          <Route
            path="/marriage"
            element={
              <ProtectedRouteV6
                role={role}
                allowRoles={["member_close", "co_operator", "admin"]}
                redirectTo="/"
              >
                <MarriagePage />
              </ProtectedRouteV6>
            }
          />

          <Route
            path="/parent_child"
            element={
              <ProtectedRouteV6
                role={role}
                allowRoles={["member_close", "co_operator", "admin"]}
                redirectTo="/"
              >
                <ParentChildPage />
              </ProtectedRouteV6>
            }
          />

          <Route
            path="/family-setup"
            element={
              <ProtectedRouteV6
                role={role}
                allowRoles={["member_close", "co_operator", "admin"]}
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
                allowRoles={["member_close", "co_operator", "admin"]}
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
                allowRoles={["member_close", "co_operator", "admin"]}
                redirectTo="/"
              >
                <PendingReviewPage role={role} />
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
