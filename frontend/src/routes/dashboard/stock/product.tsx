import {createFileRoute, redirect} from "@tanstack/react-router";
import {paths} from "config/paths";
import {LazyPage} from "layouts/lazy-page";
import {isLoggedIn} from "utilities/utils";

const ProductTable = LazyPage(
    () => import("pages/dashboard/management/stock/product")
);

export const Route = createFileRoute(paths.dashboard.stock.root)({
    component: () => ProductTable,
    beforeLoad: async () => {
        if (!isLoggedIn()) {
            throw redirect({
                to: paths.auth.login,
            });
        }
    },
});
