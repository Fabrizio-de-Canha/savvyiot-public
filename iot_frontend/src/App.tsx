import { RequireAdminToken, RequireToken } from "./auth/auth";
import { HomePage } from "./pages/Home";
import { LoginForm } from "./pages/Login";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { NavWrapper } from "./components/wrappers/NavWrapper";
import { Products } from "./pages/Products";
import { Devices } from "./pages/Devices";
import { Users } from "./pages/admin/Users";

export default function App() {
  return (
    <div className="min-h-screen content-center items-center">
      <BrowserRouter basename="/">
        <Routes>
          <Route path="/" element={<Navigate to="/home" />} />

          <Route path="/login" element={<LoginForm />} />

          <Route
            path="/home"
            element={
              <RequireToken>
                <NavWrapper>
                  <Products />
                </NavWrapper>
              </RequireToken>
            }
          />

          <Route
            path="/users"
            element={
              <RequireAdminToken>
                <NavWrapper>
                  <Users />
                </NavWrapper>
              </RequireAdminToken>
            }
          />

          <Route
            path="/devices"
            element={
              <RequireToken>
                <NavWrapper>
                  <Devices />
                </NavWrapper>
              </RequireToken>
            }
          />

          <Route
            path="/dashboard"
            element={
              <RequireToken>
                <NavWrapper>
                  <Products />
                </NavWrapper>
              </RequireToken>
            }
          />
        </Routes>
      </BrowserRouter>
    </div>
  );
}
