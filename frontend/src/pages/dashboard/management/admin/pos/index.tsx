import {Grid} from "@mantine/core";
import {Page} from "components/page";
import {PageHeader} from "components/page-header";

import {paths} from "config/paths";
import {PosTable} from "./pos-table";
import type {UserRead} from "@client/schemas";
import {OwnerSelector} from "./select-owner";
import {useState} from "react";
import {SpotlightSearchBarButton} from "@components/spotlight-search-bar-button";
import {SecondSpotlight} from "layouts/dashboard/spotlightstore";
import {useParams} from "@tanstack/react-router";

const breadcrumbs = [
    {label: "Dashboard", href: paths.dashboard.root},
    {label: "Management", href: paths.dashboard.admin.management.root},
    {
        label: "Manage owners",
        href: paths.dashboard.admin.management.owners.root,
    },
    {label: "Manage point of sale"},
];

export default function POSPage() {
    const [selectedOwner, setSelectedOwner] = useState<UserRead | null>(null);
    //const ownerId = useParams(paths.dashboard.admin.management.owners.pos.root);

    return (
        <Page title="Pos List">
            <PageHeader title="Point of sale list" breadcrumbs={breadcrumbs} />
            <Grid>
                <Grid.Col span={12}>
                    <SpotlightSearchBarButton
                        placeholder="Choisir un propriétaire"
                        spotlight={
                            <OwnerSelector
                                onSelect={(owner) => setSelectedOwner(owner)}
                            />
                        }
                        open={SecondSpotlight.open}
                    />
                </Grid.Col>
                <Grid.Col span={12}>
                    {selectedOwner && <PosTable owner={selectedOwner} />}
                </Grid.Col>
            </Grid>
        </Page>
    );
}
