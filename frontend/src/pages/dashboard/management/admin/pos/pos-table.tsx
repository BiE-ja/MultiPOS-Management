// src/pages/dashboard/management/admin/owner-table.tsx

import {type AreaDetails as Pos, type UserRead} from "@client/schemas/";
import {useZoneListAllByAdmin as usePosList} from "@client/services/zone";
import {DataTable} from "@components/data-table";
import {LinkChip} from "@components/link-chip";
import {Box, Group, Loader, Text} from "@mantine/core";
import {paths} from "config/paths";
import type {DataTableColumn} from "mantine-datatable";
import {useMemo, useState} from "react";
import {AddButton} from "@components/add-button";
import {formatDate} from "utilities/date";
import {AddPos} from "./add-pos";

type SortableFields = Pick<Pos, "created_at" | "name" | "location">;

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

export type PosTableProps = {
    owner: UserRead;
};

export function PosTable({owner}: PosTableProps) {
    const {data, isLoading} = usePosList(owner.id);
    const {page, limit, setLimit, setPage} = usePagination();
    const {tabs, filters, sort} = DataTable.useDataTable<SortableFields>({
        sortConfig: {
            direction: "asc",
            column: "name",
        },
        tabsConfig: {
            tabs: [
                {
                    value: "*",
                    label: "All",
                    counter: data?.length,
                    rightSection: <Loader size="xs" />,
                },
                {
                    value: "active",
                    label: "Active",
                    color: "teal",
                    //counter: metrics?.filter((pos) => pos.is_active).length,
                    rightSection: <Loader size="xs" color="teal" />,
                },

                {
                    value: "inactive",
                    label: "Inactive",
                    color: "red",
                    //counter: metrics
                    rightSection: <Loader size="xs" color="teal" />,
                },
            ],
        },
    });

    const [modalOpened, setModalOpened] = useState(false);
    const [selectedPos, setSelectedPos] = useState<Pos | undefined>();

    const openCreateModal = () => {
        setSelectedPos(undefined);
        setModalOpened(true);
    };

    const openEditModal = (pos: Pos) => {
        setSelectedPos(pos);
        setModalOpened(true);
    };

    const columns: DataTableColumn<Pos>[] = useMemo(
        () => [
            {
                accessor: "number",
                title: "Numéro",
                width: 156,
                render: (_pos, index) => (
                    <LinkChip
                        href={paths.dashboard.admin.management.owners.pos.view(
                            "" + _pos.owner_id + "",
                            "" + _pos.id + ""
                        )}>
                        {(page - 1) * limit + index + 1}
                    </LinkChip>
                ),
            },
            {
                accessor: "name",
                title: "Nom du point de vente",
                sortable: true,
                sortAccessor: "name",
                render: (pos) => (
                    <Group wrap="nowrap">
                        <Box w="16rem">
                            <Text truncate="end">{pos.name} </Text>
                            <Text size="sm" c="dimmed" truncate="end"></Text>
                        </Box>
                    </Group>
                ),
            },
            {
                accessor: "location",
                title: "Localisation",
                noWrap: true,
                width: 160,
                render: (pos) => pos.location,
            },
            {
                accessor: "employee",
                title: "Nombre d'employés'",
                width: 180,
                //sortable: true,
                render: (pos) => pos.employee_count ?? 0,
            },
            {
                accessor: "users",
                title: "Nombre d'utilisateur",
                width: 120,
                render: (pos) => pos.user_count ?? 0,
            },
            {
                accessor: "createdAt",
                title: "Créé le",
                noWrap: true,
                width: 140,
                sortable: true,
                sortAccessor: "created_at",
                render: (pos) =>
                    pos.created_at ? formatDate(pos.created_at) : "-",
            },
            {
                accessor: "actions",
                title: "Actions",
                textAlign: "right",
                width: 100,
                render: (pos) => (
                    <DataTable.Actions
                        onView={console.log}
                        onEdit={() => openEditModal(pos)}
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
                    title={`Point de vente pour ${owner.last_name}`}
                    description={
                        "Vous verrez dans le tableau ci-dessous, tous les points de vente appartenant à l'utilisateur "
                    }
                    actions={
                        <AddButton
                            variant="default"
                            size="xs"
                            onClick={openCreateModal}>
                            Add new pos
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
                        noRecordsText={DataTable.noRecordsText("pos")}
                        recordsPerPageLabel={DataTable.recordsPerPageLabel(
                            "pos"
                        )}
                        paginationText={DataTable.paginationText("pos")}
                        page={page}
                        records={data ?? []}
                        fetching={isLoading}
                        onPageChange={setPage}
                        recordsPerPage={limit}
                        totalRecords={data?.length ?? 0}
                        onRecordsPerPageChange={setLimit}
                        recordsPerPageOptions={[5, 15, 30, 40]}
                        sortStatus={sort.status}
                        onSortStatusChange={sort.change}
                        columns={columns}
                    />
                </DataTable.Content>
            </DataTable.Container>

            <AddPos
                opened={modalOpened}
                onClose={() => setModalOpened(false)}
                pos={selectedPos}
                ownerId={owner.id}
            />
        </>
    );
}
