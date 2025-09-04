import { LoadingScreen } from "@components/loading-screen";
import { Navigate, Outlet, useLocation } from "@tanstack/react-router";
import { app } from "config/config";
import { useAuthContext } from "hooks/useAuthContext";

import { paths } from "config/paths";

interface AuthGuardProps {
  children: ReactNode;
}


export function AuthGuard({ children }: AuthGuardProps) {
  const { pathname } = useLocation();
  const { isAuthenticated, isInitialized } = useAuthContext();

  if (!isInitialized) {
    return <LoadingScreen />;
  }

  if (!isAuthenticated) {
    return (
      <Navigate to={`${paths.auth.login}?${app.redirectQueryParamName}=${pathname}`} replace />
    );
  }

  return children;
}