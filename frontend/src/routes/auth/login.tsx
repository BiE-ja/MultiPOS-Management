// frontend/src/routes/auth/login.tsx

import {createFileRoute, redirect} from "@tanstack/react-router";
import {isLoggedIn} from "hooks/useAuth";
import {LazyPage} from "routes/lazy-page";
import {paths} from "config/paths";

const LoginPage = LazyPage(() => import("pages/auth"));

export const Route = createFileRoute(paths.auth.login)({
    component: () => LoginPage,
    beforeLoad: async () => {
        if (isLoggedIn()) {
            throw redirect({
                to: paths.dashboard.home,
            });
        }
    },
});
