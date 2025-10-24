import type {UserPublic, UsersOwnersListSortBy} from "@client/schemas";
import {
    getUsersFetchAllByAdminQueryKey,
    useUsersFetchAllByAdmin,
} from "@client/services/users";
import {DataTable} from "@components/data-table";
import {UserStatusBadge} from "@components/resources/customers";
import {ActionIcon, Box, Group, Loader, Text, Tooltip} from "@mantine/core";
import {useQueryClient} from "@tanstack/react-query";
import {type UserRead} from "client/schemas/userRead";
import type {DataTableColumn} from "mantine-datatable";
import {useEffect, useMemo, useState} from "react";
import {formatDate} from "utilities/date";
import {formatPhoneNumber} from "utilities/phone-number";
import {AddButton} from "@components/add-button";
import {ResetPasswordModal} from "./reset-password";
import {PiClockCounterClockwiseDuotone} from "react-icons/pi";
import {AddUser} from "./addUser";

type SortableFields = Pick<UserRead, UsersOwnersListSortBy>;

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

export function UsersTable() {
    const {page, limit, setPage, setLimit} = usePagination();

    const queryClient = useQueryClient();

    const [selectedUser, setSelectedUser] = useState<Partial<UserRead>>();

    //  pour gérer l'ouverture du modal
    const [userModalOpened, setUserModalOpened] = useState(false);
    const [resetPasswordOpened, setResetPasswordOpened] = useState(false);
    // ouverture pour visualisation ou pour édition
    const [forUserEdition, setForUserEdition] = useState(false);

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
        };
        return base;
    }, [limit, page]);

    const {data: users, isLoading} = useUsersFetchAllByAdmin(params);

    const filteredUsers = useMemo(() => {
        if (!users?.data) return [];

        switch (tabs.value) {
            case "active":
                return users.data.filter((o) => o.is_active);
            case "inactive":
                return users.data.filter((o) => !o.is_active);
            default:
                return users.data;
        }
    }, [users, tabs.value]);
    // renvoie à la 1ère page en cas de changement de valeur du tabs
    useEffect(() => {
        setPage(1);
    }, [tabs.value, setPage]);

    // tri local
    const sortedUsers = useMemo(() => {
        if (!filteredUsers.length) return [];

        const {columnAccessor, direction} = sort.status;
        if (!columnAccessor) return filteredUsers;

        const sorted = [...filteredUsers].sort((a, b) => {
            const aValue = a[columnAccessor as keyof UserPublic];
            const bValue = b[columnAccessor as keyof UserPublic];

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
    }, [filteredUsers, sort.status]);

    // gestion fenêtre modal
    const openCreateModal = () => {
        setSelectedUser(undefined);
        setForUserEdition(false);
        setUserModalOpened(true);
    };

    const openEditModal = (user: UserPublic, edition: boolean = true) => {
        setSelectedUser(user);
        setForUserEdition(edition);
        setUserModalOpened(true);
    };

    const openResetPasswordModal = (user: UserPublic) => {
        setSelectedUser(user);
        setResetPasswordOpened(true);
    };

    const columns: DataTableColumn<UserPublic>[] = useMemo(
        () => [
            {
                accessor: "number",
                title: "Numéro",
                width: 100,
                render: (user, index) => (page - 1) * limit + index + 1,
            },
            {
                accessor: "last_name",
                title: "Nom complet",
                sortable: true,
                sortAccessor: "last_name",
                render: (user) => (
                    <Group wrap="nowrap">
                        <Box w="16rem">
                            <Text truncate="end">
                                {user.last_name} {user.name}
                            </Text>
                            <Text size="sm" c="dimmed" truncate="end">
                                {user.email}
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
                render: (user) =>
                    user.phone ? formatPhoneNumber(user.phone) : "-",
            },
            {
                accessor: "status",
                title: "Status",
                width: 120,
                render: (user) => (
                    <UserStatusBadge status={user.is_active} w="100%" />
                ),
            },
            {
                accessor: "created_at",
                title: "Créé le",
                noWrap: true,
                width: 140,
                sortable: true,
                sortAccessor: "created_at",
                render: (user) =>
                    user.created_at ? formatDate(user.created_at) : "-",
            },
            {
                accessor: "reset_password",
                title: "Reset Password",
                //width: 140,
                render: (user) => (
                    <Tooltip label="Restore password">
                        <ActionIcon
                            variant="default"
                            size="xs"
                            onClick={() => openResetPasswordModal(user)}>
                            <PiClockCounterClockwiseDuotone size="1rem" />
                        </ActionIcon>
                    </Tooltip>
                ),
            },
            {
                accessor: "actions",
                title: "Actions",
                textAlign: "right",
                width: 100,
                render: (user) => (
                    <DataTable.Actions
                        onView={() => openEditModal(user, false)}
                        onEdit={() => openEditModal(user)}
                        onDelete={() => console.log(user.name)}
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
            counter: users?.count,
            rightSection: <Loader size="xs" />,
        },
        {
            value: "active",
            label: "Active",
            color: "teal",
            counter: users ? users.data.filter((o) => o.is_active).length : 0,
            rightSection: <Loader size="xs" color="teal" />,
        },

        {
            value: "inactive",
            label: "Inactive",
            color: "red",
            counter: users ? users.data.filter((o) => !o.is_active).length : 0,
            rightSection: <Loader size="xs" color="teal" />,
        },
    ];

    return (
        <>
            <DataTable.Container>
                <DataTable.Title
                    title="Users"
                    description="List of all users"
                    actions={
                        <AddButton
                            variant="default"
                            size="xs"
                            onClick={openCreateModal}>
                            Add new user
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
                        records={sortedUsers}
                        fetching={isLoading}
                        onPageChange={setPage}
                        recordsPerPage={limit}
                        totalRecords={sortedUsers.length}
                        onRecordsPerPageChange={setLimit}
                        recordsPerPageOptions={[5, 15, 30, 40]}
                        sortStatus={sort.status}
                        onSortStatusChange={sort.change}
                        columns={columns}
                    />
                </DataTable.Content>
            </DataTable.Container>

            <AddUser
                opened={userModalOpened}
                view={forUserEdition}
                onClose={() => {
                    setUserModalOpened(false);
                    setForUserEdition(false);
                    setSelectedUser(undefined);
                }}
                user={selectedUser}
                onSuccess={() =>
                    queryClient.invalidateQueries({
                        queryKey: getUsersFetchAllByAdminQueryKey(),
                    })
                }
            />

            <ResetPasswordModal
                opened={resetPasswordOpened}
                onClose={() => {
                    setResetPasswordOpened(false);
                    setSelectedUser(undefined);
                }}
                user={selectedUser}
            />
        </>
    );
}
