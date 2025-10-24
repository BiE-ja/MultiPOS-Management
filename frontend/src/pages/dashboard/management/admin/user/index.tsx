import {Grid} from "@mantine/core";
import {Page} from "components/page";
import {PageHeader} from "components/page-header";

import {paths} from "config/paths";
import {UsersTable} from "./user-table";

const breadcrumbs = [
    {label: "Dashboard", href: paths.dashboard.root},
    {label: "Management", href: paths.dashboard.admin.management.root},
    {
        label: "Manage Users",
        href: paths.dashboard.admin.management.users,
    },
    {label: "List"},
];

export default function ListUsersPage() {
    return (
        <Page title="List Users">
            <PageHeader title="List users" breadcrumbs={breadcrumbs} />

            <Grid>
                <Grid.Col span={12}>{/*<OwnerMetrics />*/}</Grid.Col>

                <Grid.Col span={12}>
                    <UsersTable />
                </Grid.Col>
            </Grid>
        </Page>
    );
}
