import {createFileRoute, redirect} from "@tanstack/react-router";
import {paths} from "config/paths";
import {DashboardLayout} from "layouts/dashboard";
import {isLoggedIn} from "utilities/utils";

export const Route = createFileRoute(paths.dashboard.root)({
    component: () => <DashboardLayout />,
    beforeLoad: async () => {
        if (!isLoggedIn()) {
            throw redirect({
                to: paths.auth.login,
            });
        }
    },
});
