import {createFileRoute} from "@tanstack/react-router";
import {paths} from "config/paths";
import {LazyPage} from "layouts/lazy-page";
import {AdminGuard} from "guards/Admin-guard";

const Owners = LazyPage(() => import("pages/dashboard/management/admin/owner"));
export const Route = createFileRoute(
    paths.dashboard.admin.management.owners.root
)({
    component: RouteComponent,
});

function RouteComponent() {
    return <AdminGuard>{Owners}</AdminGuard>;
}
