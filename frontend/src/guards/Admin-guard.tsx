import {LoadingScreen} from "@components/loading-screen";
import {useLocation, Navigate} from "@tanstack/react-router";
import {app} from "config/config";
import {useAuthContext} from "hooks/useAuthContext";

import type {ReactNode} from "react";

import {paths} from "config/paths";

interface AdminGuardProps {
    children: ReactNode;
}

function getRedirectPath(search: string) {
    const REDIRECT_QUERY_PARAM_REGEX = new RegExp(
        `${app.redirectQueryParamName}=([^&]*)`
    );
    return REDIRECT_QUERY_PARAM_REGEX.exec(search)?.[1] ?? paths.dashboard.root;
}

export function AdminGuard({children}: AdminGuardProps) {
    const {pathname} = useLocation();
    const {user, isAuthenticated, isInitialized} = useAuthContext();
    //const {user} = useAuth();

    if (!isInitialized) {
        return <LoadingScreen />;
    }

    if (!isAuthenticated) {
        const redirectPath = getRedirectPath(pathname);
        return <Navigate to={redirectPath} replace />;
    }

    if (!user?.is_superuser) {
        const redirectPath = getRedirectPath(paths.dashboard.home);
        return <Navigate to={redirectPath} replace />;
    }

    return children;
}
