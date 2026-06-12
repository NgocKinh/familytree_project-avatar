export function handleAuthError(err) {
    if (err?.response?.status !== 401) {
      return false;
    }
  
    alert("Phiên đăng nhập không hợp lệ. Cần đăng nhập lại.");
  
    localStorage.removeItem("token");
  
    window.location.href = "/";
  
    return true;
  }