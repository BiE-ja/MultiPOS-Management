import {createFileRoute, redirect} from "@tanstack/react-router";
import {paths} from "config/paths";
import {LazyPage} from "layouts/lazy-page";
import {isLoggedIn} from "utilities/utils";

const NotFound = LazyPage(() => import("pages/dashboard/notFound"));

export const Route = createFileRoute(paths.dashboard.notFound)({
    component: () => NotFound,
    beforeLoad: async () => {
        if (!isLoggedIn()) {
            throw redirect({
                to: paths.auth.login,
            });
        }
    },
});
