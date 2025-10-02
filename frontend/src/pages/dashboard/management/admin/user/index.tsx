import {Grid} from "@mantine/core";
import {Page} from "components/page";
import {PageHeader} from "components/page-header";

import {paths} from "config/paths";
import {OwnerMetrics} from "./owners-metrics";
import {OwnersTable} from "./owner-table";

const breadcrumbs = [
    {label: "Dashboard", href: paths.dashboard.root},
    {label: "Management", href: paths.dashboard.admin.management.root},
    {label: "Owners", href: paths.dashboard.admin.management.owners.root},
    {label: "List"},
];

export default function ListOwnersPage() {
    return (
        <Page title="List owners">
            <PageHeader title="List owners" breadcrumbs={breadcrumbs} />

            <Grid>
                <Grid.Col span={12}>
                    <OwnerMetrics />
                </Grid.Col>

                <Grid.Col span={12}>
                    <OwnersTable />
                </Grid.Col>
            </Grid>
        </Page>
    );
}
