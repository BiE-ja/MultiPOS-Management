import {Grid} from "@mantine/core";
import {Page} from "components/page";
import {PageHeader} from "components/page-header";

import {paths} from "config/paths";
import {PosTable} from "./pos-table";
import type {UserRead} from "@client/schemas";
import {OwnerSelector} from "./select-owner";
import {useEffect, useState} from "react";
//import {SpotlightSearchBarButton} from "@components/spotlight-search-bar-button";
//import {SecondSpotlight} from "layouts/dashboard/spotlightstore";

import {useUsersReadById, useUsersReadOwnerMe} from "@client/services/users";
import useAuth from "hooks/useAuth";

const breadcrumbs = [
    {label: "Dashboard", href: paths.dashboard.root},
    {label: "Management", href: paths.dashboard.admin.management.root},
    {
        label: "Manage owners",
        href: paths.dashboard.admin.management.owners.root,
    },
    {label: "Manage point of sale"},
];

interface POSPageProps {
    ownerId?: string;
}

export default function POSPage({ownerId}: POSPageProps) {
    const [selectedOwner, setSelectedOwner] = useState<UserRead | null>(null);

    const {data: owner} = useUsersReadById(ownerId as string);

    const {user} = useAuth();

    const {data: ownerMe} = useUsersReadOwnerMe();

    useEffect(() => {
        // si user n'est pas instancié, on ne fait rien
        if (!user) return;
        // si c'est un superuser
        if (user.is_superuser) {
            // si un ownerId est fourni et qu'aucun propriétaire n'est sélectionné, on ne fait rien
            if (!ownerId && !selectedOwner) return;
            // si un ownerId est fourni
            if (ownerId) {
                // si le propriétaire sélectionné est différent de celui fourni, on met à jour
                if (owner && selectedOwner?.id !== owner.id)
                    setSelectedOwner(owner);
            } else {
                // si ce n'est pas un superuser
                // si aucun propriétaire n'est sélectionné, on met à jour
                if (!selectedOwner) setSelectedOwner(null);
            }
        } else {
            // si ce n'est pas un superuser, on est obligé d'avoir un propriétaire
            if (!user.is_owner && !selectedOwner) return;
            // on met à jour avec le propriétaire connecté
            if (ownerMe) {
                setSelectedOwner(ownerMe);
            }
        }
    }, [ownerId, user, owner, ownerMe, selectedOwner]);

    return (
        <Page title="Pos List">
            <PageHeader title="Point of sale list" breadcrumbs={breadcrumbs} />
            <Grid>
                <Grid.Col span={12}>
                    {/*<SpotlightSearchBarButton
                        placeholder="Choisir un propriétaire"
                        spotlight={
                            <OwnerSelector
                                onSelect={(owner) => setSelectedOwner(owner)}
                            />
                        }
                        open={SecondSpotlight.open}
                    />*/}
                    {user?.is_superuser && (
                        <OwnerSelector
                            onSelect={(owner) => setSelectedOwner(owner)}
                        />
                    )}
                </Grid.Col>
                <Grid.Col span={12}>
                    {/*selectedOwner && <PosTable owner={selectedOwner} />*/}
                    {selectedOwner ? (
                        <PosTable owner={selectedOwner} />
                    ) : (
                        <PosTable />
                    )}
                </Grid.Col>
            </Grid>
        </Page>
    );
}
