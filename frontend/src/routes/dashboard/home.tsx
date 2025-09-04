import {createFileRoute, redirect} from "@tanstack/react-router";
import {paths} from "config/paths";
import {LazyPage} from "routes/lazy-page";
import {isLoggedIn} from "utilities/utils";

const home = LazyPage(() => import("pages/dashboard/home"));

export const Route = createFileRoute(paths.dashboard.home)({
    component: () => home,
    beforeLoad: async () => {
        if (!isLoggedIn()) {
            throw redirect({
                to: paths.auth.login,
            });
        }
    },
});
