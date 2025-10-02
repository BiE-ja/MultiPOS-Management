// src/pages/dashboard/management/admin/owner-table.tsx

import {UsersOwnersListSortBy, type UserRead as Owner} from "@client/schemas/";
import {useUsersOwnersList} from "@client/services/users";
import {DataTable} from "@components/data-table";
import {LinkChip} from "@components/link-chip";
import {Box, Group, Loader, Text} from "@mantine/core";
import {paths} from "config/paths";
import type {DataTableColumn} from "mantine-datatable";
import {useMemo, useState} from "react";
import {formatPhoneNumber} from "utilities/phone-number";

import {UserStatusBadge} from "@components/resources/customers";

import {AddButton} from "@components/add-button";
import {formatDate} from "utilities/date";
import {AddUser} from "./addUser";
import {Navigate} from "@tanstack/react-router";

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
    const {data: metrics} = useUsersOwnersList();
    const {page, limit, setLimit, setPage} = usePagination();
    const {tabs, filters, sort} = DataTable.useDataTable<SortableFields>({
        sortConfig: {
            direction: "asc",
            column: "last_name",
        },
        tabsConfig: {
            tabs: [
                {
                    value: "*",
                    label: "All",
                    counter: metrics?.total,
                    rightSection: <Loader size="xs" />,
                },
                {
                    value: "active",
                    label: "Active",
                    color: "teal",
                    counter: metrics?.total_active,
                    rightSection: <Loader size="xs" color="teal" />,
                },

                {
                    value: "inactive",
                    label: "Inactive",
                    color: "red",
                    counter: metrics
                        ? metrics.total - metrics.total_active
                        : undefined,
                    rightSection: <Loader size="xs" color="teal" />,
                },
            ],
        },
    });

    const {data, isLoading} = useUsersOwnersList({
        limit: limit,
        skip: (page - 1) * limit,
        sort_by: sort.status.columnAccessor as UsersOwnersListSortBy,
        order: sort.status.direction,
    });

    const [modalOpened, setModalOpened] = useState(false);
    const [selectedOwner, setSelectedOwner] = useState<Owner | undefined>();

    const openCreateModal = () => {
        setSelectedOwner(undefined);
        setModalOpened(true);
    };

    const openEditModal = (owner: Owner) => {
        setSelectedOwner(owner);
        setModalOpened(true);
    };

    const columns: DataTableColumn<Owner>[] = useMemo(
        () => [
            {
                accessor: "number",
                title: "Numéro",
                width: 156,
                render: (_owner, index) => (
                    <LinkChip
                        href={paths.dashboard.admin.management.owners.view(
                            "" + _owner.id + ""
                        )}>
                        {(page - 1) * limit + index + 1}
                    </LinkChip>
                ),
            },
            {
                accessor: "fullName",
                title: "Nom complet",
                sortable: true,
                sortAccessor: "last_name",
                render: (owner) => (
                    <Group wrap="nowrap">
                        <Box w="16rem">
                            <Text truncate="end">
                                {owner.last_name && owner.name}{" "}
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
                render: (owner) => owner.owned_areas?.length,
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
                accessor: "createdAt",
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
                        onView={() => (
                            <Navigate
                                to={paths.dashboard.admin.management.owners.pos.list(
                                    owner.id
                                )}
                            />
                        )}
                        onEdit={() => openEditModal(owner)}
                        onDelete={console.log}
                    />
                ),
            },
        ],
        [page, limit]
    );

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
                <DataTable.Tabs tabs={tabs.tabs} onChange={tabs.change} />
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
                        records={data?.data ?? []}
                        fetching={isLoading}
                        onPageChange={setPage}
                        recordsPerPage={limit}
                        totalRecords={data?.total ?? 0}
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
                onClose={() => setModalOpened(false)}
                owner={selectedOwner}
            />
        </>
    );
}
