import {createFileRoute, Outlet} from "@tanstack/react-router";

import {AdminGuard} from "guards/Admin-guard";

export const Route = createFileRoute("/dashboard/admin")({
    component: () => (
        <AdminGuard>
            <Outlet />
        </AdminGuard>
    ),
});
