// src/pages/dashboard/management/admin/owner-table.tsx

import {UsersOwnersListSortBy, type UserRead as Owner} from "@client/schemas/";
import {useUsersOwnersList} from "@client/services/users";
import {DataTable} from "@components/data-table";
import {Box, Group, Loader, Text} from "@mantine/core";
import {buildPaths} from "config/paths";
import type {DataTableColumn} from "mantine-datatable";
import {useEffect, useMemo, useState} from "react";
import {formatPhoneNumber} from "utilities/phone-number";

import {UserStatusBadge} from "@components/resources/customers";

import {AddButton} from "@components/add-button";
import {formatDate} from "utilities/date";
import {AddUser} from "../user/addUser";
import {getUsersOwnersListQueryKey} from "client/services/users";
import {useQueryClient} from "@tanstack/react-query";
import CustomNavLink from "@components/CustomNavLink";

type SortableFields = Pick<Owner, UsersOwnersListSortBy>;

export type PaginationParams = {
    page?: number;
    limit?: number;
};

function usePagination(params?: PaginationParams) {
    const [page, setPage] = useState(params?.page ?? 1);
    const [limit, setLimit] = useState(params?.limit ?? 15);

    const onChangeLimit = (value: number) => {
        setLimit(value);
        setPage(1);
    };

    return {page, limit, setPage, setLimit: onChangeLimit};
}

export function OwnersTable() {
    // pour mettre à jour de la page si le nombre total de propriétaires change
    const queryClient = useQueryClient();
    //  pour gérer l'ouverture du modal
    const [modalOpened, setModalOpened] = useState(false);
    const [selectedOwner, setSelectedOwner] = useState<Partial<Owner>>();
    const [viewOwner, setViewOwner] = useState<boolean | undefined>(undefined);

    const {page, limit, setLimit, setPage} = usePagination();

    const {tabs, filters, sort} = DataTable.useDataTable<SortableFields>({
        sortConfig: {
            direction: "asc",
            column: "last_name",
        },
    });

    const params = useMemo(() => {
        const base = {
            limit,
            skip: (page - 1) * limit,
            /*
             * Pour trie côté serveur - Désactivé pour le moment
             *sort_by: sort.status.columnAccessor as UsersOwnersListSortBy,
            order: sort.status.direction,*/
        };
        return base;
    }, [limit, page /*sort.status*/]);

    // récupération des owners avec les nouveaux paramètres
    const {data: owners, isLoading} = useUsersOwnersList(params);
    // === Nouveau : filtrage local selon onglet sélectionné === //
    const filteredOwners = useMemo(() => {
        if (!owners?.data) return [];

        switch (tabs.value) {
            case "active":
                return owners.data.filter((o) => o.is_active);
            case "inactive":
                return owners.data.filter((o) => !o.is_active);
            default:
                return owners.data;
        }
    }, [owners, tabs.value]);

    // renvoie à la 1ère page en cas de changement de valeur du tabs
    useEffect(() => {
        setPage(1);
    }, [tabs.value, setPage]);

    // tri local
    const sortedOwners = useMemo(() => {
        if (!filteredOwners.length) return [];

        const {columnAccessor, direction} = sort.status;
        if (!columnAccessor) return filteredOwners;

        const sorted = [...filteredOwners].sort((a, b) => {
            const aValue = a[columnAccessor as keyof Owner];
            const bValue = b[columnAccessor as keyof Owner];

            if (aValue == null) return 1;
            if (bValue == null) return -1;

            if (typeof aValue === "string" && typeof bValue === "string") {
                return direction === "asc"
                    ? aValue.localeCompare(bValue)
                    : bValue.localeCompare(aValue);
            }
            return 0;
        });
        return sorted;
    }, [filteredOwners, sort.status]);

    // gestion fenêtre modal
    const openCreateModal = () => {
        setSelectedOwner(undefined);
        setViewOwner(undefined);
        setModalOpened(true);
    };

    const openEditModal = (owner: Owner) => {
        setSelectedOwner(owner);
        setViewOwner(undefined);
        setModalOpened(true);
    };

    const openViewModal = (owner: Owner) => {
        setSelectedOwner(owner);
        setViewOwner(true);
        setModalOpened(true);
    };

    const columns: DataTableColumn<Owner>[] = useMemo(
        () => [
            {
                accessor: "number",
                title: "Numéro",
                width: 100,
                render: (_owner, index) => (page - 1) * limit + index + 1,
            },
            {
                accessor: "last_name",
                title: "Nom complet",
                sortable: true,
                sortAccessor: "last_name",
                render: (owner) => (
                    <Group wrap="nowrap">
                        <Box w="16rem">
                            <Text truncate="end">
                                {owner.last_name} {owner.name}
                            </Text>
                            <Text size="sm" c="dimmed" truncate="end">
                                {owner.email}
                            </Text>
                        </Box>
                    </Group>
                ),
            },
            {
                accessor: "phoneNumber",
                title: "Téléphone",
                noWrap: true,
                width: 160,
                render: (owner) =>
                    owner.phone ? formatPhoneNumber(owner.phone) : "-",
            },
            {
                accessor: "pos",
                title: "Nombre de boutiques",
                width: 180,
                //sortable: true,
                render: (owner) => (
                    <CustomNavLink
                        to={buildPaths.posList(owner.id)}
                        label={owner.owned_areas?.length.toString() ?? "0"}
                    />
                ),
            },
            {
                accessor: "status",
                title: "Status",
                width: 120,
                render: (owner) => (
                    <UserStatusBadge status={owner.is_active} w="100%" />
                ),
            },
            {
                accessor: "created_at",
                title: "Créé le",
                noWrap: true,
                width: 140,
                sortable: true,
                sortAccessor: "created_at",
                render: (owner) =>
                    owner.created_at ? formatDate(owner.created_at) : "-",
            },
            {
                accessor: "actions",
                title: "Actions",
                textAlign: "right",
                width: 100,
                render: (owner) => (
                    <DataTable.Actions
                        onView={() => openViewModal(owner)}
                        onEdit={() => openEditModal(owner)}
                        onDelete={() => console.log(owner.name)}
                    />
                ),
            },
        ],
        [page, limit]
    );

    const tabsDefinition = [
        {
            value: "*",
            label: "All",
            counter: owners?.total,
            rightSection: <Loader size="xs" />,
        },
        {
            value: "active",
            label: "Active",
            color: "teal",
            counter: owners?.total_active,
            rightSection: <Loader size="xs" color="teal" />,
        },

        {
            value: "inactive",
            label: "Inactive",
            color: "red",
            counter: owners ? owners.total - owners.total_active : undefined,
            rightSection: <Loader size="xs" color="teal" />,
        },
    ];

    return (
        <>
            <DataTable.Container>
                <DataTable.Title
                    title="Owners"
                    description="List of all owners"
                    actions={
                        <AddButton
                            variant="default"
                            size="xs"
                            onClick={openCreateModal}>
                            Add new owner
                        </AddButton>
                    }
                />
                <DataTable.Tabs tabs={tabsDefinition} onChange={tabs.change} />
                <DataTable.Filters
                    filters={filters.filters}
                    onClear={filters.clear}
                />
                <DataTable.Content>
                    <DataTable.Table
                        minHeight={240}
                        noRecordsText={DataTable.noRecordsText("owner")}
                        recordsPerPageLabel={DataTable.recordsPerPageLabel(
                            "owners"
                        )}
                        paginationText={DataTable.paginationText("owners")}
                        page={page}
                        records={sortedOwners}
                        fetching={isLoading}
                        onPageChange={setPage}
                        recordsPerPage={limit}
                        totalRecords={sortedOwners.length}
                        onRecordsPerPageChange={setLimit}
                        recordsPerPageOptions={[5, 15, 30, 40]}
                        sortStatus={sort.status}
                        onSortStatusChange={sort.change}
                        columns={columns}
                    />
                </DataTable.Content>
            </DataTable.Container>

            <AddUser
                opened={modalOpened}
                onClose={() => {
                    setModalOpened(false);
                    setSelectedOwner(undefined);
                    setViewOwner(false);
                }}
                view={viewOwner}
                user={selectedOwner}
                onSuccess={() =>
                    queryClient.invalidateQueries({
                        queryKey: getUsersOwnersListQueryKey(),
                    })
                }
            />
        </>
    );
}
