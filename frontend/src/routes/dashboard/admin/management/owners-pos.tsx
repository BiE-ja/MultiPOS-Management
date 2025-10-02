import {createFileRoute} from "@tanstack/react-router";
import {paths} from "config/paths";
import {LazyPage} from "layouts/lazy-page";
import {AdminGuard} from "guards/Admin-guard";

const Pos = LazyPage(() => import("pages/dashboard/management/admin/pos"));
export const Route = createFileRoute(
    paths.dashboard.admin.management.owners.pos.root
)({
    component: RouteComponent,
});

function RouteComponent() {
    return <AdminGuard>{Pos}</AdminGuard>;
}
