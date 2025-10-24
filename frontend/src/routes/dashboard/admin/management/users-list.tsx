import {createFileRoute} from "@tanstack/react-router";
import {paths} from "config/paths";
import {LazyPage} from "layouts/lazy-page";
import {AdminGuard} from "guards/Admin-guard";

const User = LazyPage(() => import("pages/dashboard/management/admin/user"));
export const Route = createFileRoute(paths.dashboard.admin.management.users)({
    component: RouteComponent,
});

function RouteComponent() {
    return <AdminGuard>{User}</AdminGuard>;
}
