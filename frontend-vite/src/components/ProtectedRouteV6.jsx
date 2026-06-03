import React from "react";
import { Navigate } from "react-router-dom";

/**
 * ProtectedRouteV6
 * - Chuẩn React Router v6 (children-based)
 * - Phân biệt viewer chưa đăng nhập và viewer đã đăng nhập
 * - Chỉ làm 1 việc: cho qua hoặc redirect
 */
const ProtectedRouteV6 = ({
  role,
  allowRoles,
  currentUser = null,
  redirectTo = "/",
  children,
}) => {
  if (!currentUser) {
    return <Navigate to={redirectTo} replace />;
  }

  if (!allowRoles.includes(role)) {
    return <Navigate to={redirectTo} replace />;
  }

  return <>{children}</>;
};

export default ProtectedRouteV6;

