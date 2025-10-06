import {createFileRoute, Outlet} from "@tanstack/react-router";

import {AdminGuard} from "guards/Admin-guard";
import {LazyPage} from "layouts/lazy-page";

const NotFound = LazyPage(() => import("pages/dashboard/notFound"));

export const Route = createFileRoute("/dashboard/admin")({
    component: () => (
        <AdminGuard>
            <Outlet />
        </AdminGuard>
    ),
    notFoundComponent: () => NotFound,
});
