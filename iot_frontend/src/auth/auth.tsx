import { useLocation, Navigate } from "react-router-dom";
import { jwtDecode, JwtPayload } from "jwt-decode";

interface customJWT extends JwtPayload {
  admin?: boolean;
  superuser?: boolean;
}
export const setToken = (token: string) => {
  localStorage.setItem("token_local", token);
};

export const fetchToken = () => {
  return localStorage.getItem("token_local");
};

export function RequireToken({ children }: any) {
  let auth = fetchToken();
  let location = useLocation();

  if (!auth) {
    return <Navigate to="/login" state={{ from: location }} />;
  }

  return children;
}

export function RequireAdminToken({ children }: any) {
  let auth = fetchToken();
  let location = useLocation();

  if (!auth) {
    return <Navigate to="/login" state={{ from: location }} />;
  } else {
    const jwt: customJWT = jwtDecode(auth);
    if (!jwt.admin) {
      return <Navigate to="/home" state={{ from: location }} />;
    }
  }

  return children;
}
