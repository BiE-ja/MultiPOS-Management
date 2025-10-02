import {createFileRoute, redirect} from "@tanstack/react-router";
import {paths} from "config/paths";
import {LazyPage} from "layouts/lazy-page";
import {isLoggedIn} from "utilities/utils";

const Unhautorized = LazyPage(() => import("pages/dashboard/unhautorized"));

export const Route = createFileRoute(paths.dashboard.unhautorized)({
    component: () => Unhautorized,
    beforeLoad: async () => {
        if (!isLoggedIn()) {
            throw redirect({
                to: paths.auth.login,
            });
        }
    },
});
