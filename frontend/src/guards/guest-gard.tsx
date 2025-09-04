// frontend/src/guards/guest-gard.tsx

import { LoadingScreen } from "@components/loading-screen";
import { useLocation, Navigate } from '@tanstack/react-router';
import { app } from "config/config";
import { useAuthContext } from "hooks/useAuthContext";

import type { ReactNode } from "react";

import { paths } from "config/paths";

interface GuestGuardProps {
  children: ReactNode;
}

function getRedirectPath(search: string) {
  const REDIRECT_QUERY_PARAM_REGEX = new RegExp(`${app.redirectQueryParamName}=([^&]*)`)
  return REDIRECT_QUERY_PARAM_REGEX.exec(search)?.[1] ?? paths.dashboard.root
}

export function GuestGuard({ children }: GuestGuardProps) {
  const { pathname } = useLocation();
  const { isAuthenticated, isInitialized } = useAuthContext();

  if (!isInitialized) {
    return <LoadingScreen />;
  }

  if (!isAuthenticated) {
    const redirectPath = getRedirectPath(pathname);
    return (
      <Navigate to={redirectPath} replace />
    );
  }

  return children;
}