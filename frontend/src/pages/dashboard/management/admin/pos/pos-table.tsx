// src/pages/dashboard/management/admin/owner-table.tsx

import {type AreaDetails as Pos, type UserRead} from "@client/schemas/";
import {
    getZoneListAllByAdminQueryKey,
    useZoneListAllByAdmin as usePosList,
} from "@client/services/zone";
import {DataTable} from "@components/data-table";

import {Box, Group, Loader, Text} from "@mantine/core";

import type {DataTableColumn} from "mantine-datatable";
import {useEffect, useMemo, useState} from "react";
import {AddButton} from "@components/add-button";
import {formatDate} from "utilities/date";
import {AddPos} from "./add-pos";
import {useQueryClient} from "@tanstack/react-query";

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
    owner?: UserRead;
};

export function PosTable({owner}: PosTableProps) {
    // pour mettre à jour de la page si le nombre total de propriétaires change
    const queryClient = useQueryClient();
    //  pour gérer l'ouverture du modal
    const [modalOpened, setModalOpened] = useState(false);
    const [selectedPos, setSelectedPos] = useState<Pos | undefined>();
    // pagination
    const {page, limit, setLimit, setPage} = usePagination();

    const {tabs, filters, sort} = DataTable.useDataTable<SortableFields>({
        sortConfig: {
            direction: "asc",
            column: "name",
        },
    });

    // Définition des paramètres de la requête
    const params = useMemo(() => {
        return owner?.id;
    }, [owner?.id]);

    // Récupération des données avec les nouveaux paramètres
    const {data: listPos, isLoading} = usePosList(params as string);

    const filteredPos = useMemo(() => {
        if (!listPos?.data) return [];

        switch (tabs.value) {
            case "inactive":
                return listPos.data.filter((pos) => pos.state === "inactive");
            case "active":
                return listPos.data.filter((pos) => pos.state === "active");
            case "archived":
                return listPos.data.filter((pos) => pos.state === "archived");
            default:
                return listPos.data;
        }
    }, [listPos, tabs.value]);

    // renvoie à la 1ère page en cas de changement de valeur du tabs
    useEffect(() => {
        setPage(1);
    }, [tabs.value, setPage]);

    const sortedPos = useMemo(() => {
        if (!filteredPos.length) return [];

        const {columnAccessor, direction} = sort.status;
        if (!columnAccessor) return filteredPos;

        const sorted = [...filteredPos].sort((a, b) => {
            const aValue = a[columnAccessor as keyof Pos];
            const bValue = b[columnAccessor as keyof Pos];

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
    }, [filteredPos, sort.status]);

    // gestion ouverture/fermeture modal
    const openCreateModal = () => {
        setSelectedPos(undefined);
        setModalOpened(true);
    };

    const openEditModal = (pos: Pos) => {
        setSelectedPos(pos);
        setModalOpened(true);
    };

    const tabsDefinitions = [
        {
            value: "*",
            label: "All",
            counter: listPos?.data.length,
            rightSection: <Loader size="xs" />,
        },
        {
            value: "active",
            label: "Active",
            color: "teal",
            counter: 0,
            rightSection: <Loader size="xs" color="teal" />,
        },

        {
            value: "inactive",
            label: "Inactive",
            color: "red",
            counter: 0,
            rightSection: <Loader size="xs" color="teal" />,
        },
    ];

    const columns: DataTableColumn<Pos>[] = useMemo(
        () => [
            {
                accessor: "number",
                title: "Numéro",
                width: 120,
                render: (_pos, index) => (page - 1) * limit + index + 1,
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
                        </Box>
                    </Group>
                ),
            },
            {
                accessor: "location",
                title: "Localisation",
                noWrap: true,
                width: 160,
                render: (pos) => (
                    <Text aria-multiline={true} truncate="end">
                        {pos.location}
                    </Text>
                ),
            },
            {
                accessor: "employee",
                title: "Nombre d'employés",
                width: 180,
                //sortable: true,
                render: (pos) => pos.employee_count ?? 0,
            },
            {
                accessor: "users",
                title: "Nombre d'utilisateur",
                width: 180,
                render: (pos) => pos.user_count ?? 0,
            },
            {
                accessor: "created_at",
                title: "Créé le",
                noWrap: true,
                width: 130,
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
                    title={
                        owner ? `Point de vente pour ${owner.last_name}` : ""
                    }
                    description={
                        owner
                            ? "Vous verrez dans le tableau ci-dessous, tous les points de vente appartenant à l'utilisateur "
                            : "Veuillez sélectionner un propriétaire!"
                    }
                    actions={
                        owner && (
                            <AddButton
                                variant="default"
                                size="xs"
                                onClick={openCreateModal}>
                                Add new pos
                            </AddButton>
                        )
                    }
                />
                <DataTable.Tabs tabs={tabsDefinitions} onChange={tabs.change} />
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
                        records={sortedPos}
                        fetching={isLoading}
                        onPageChange={setPage}
                        recordsPerPage={limit}
                        totalRecords={sortedPos.length}
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
                onClose={() => {
                    setModalOpened(false);
                    setSelectedPos(undefined);
                }}
                pos={selectedPos}
                ownerId={owner?.id}
                onSuccess={() =>
                    queryClient.invalidateQueries({
                        queryKey: getZoneListAllByAdminQueryKey(),
                    })
                }
            />
        </>
    );
}
