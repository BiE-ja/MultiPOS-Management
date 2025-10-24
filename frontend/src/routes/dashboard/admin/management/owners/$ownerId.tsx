import {createFileRoute} from "@tanstack/react-router";
import {paths} from "config/paths";

export const Route = createFileRoute(
    paths.dashboard.admin.management.owners.withParam
)({
    component: RouteComponent,
});

function RouteComponent() {
    return <div>Hello "/dashboard/admin/home"!</div>;
}
