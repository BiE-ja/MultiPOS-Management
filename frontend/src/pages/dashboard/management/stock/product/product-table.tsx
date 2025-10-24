import {useMemo, useState} from "react";
import {type ProductRead} from "client/schemas/productRead";
import {useRouter} from "@tanstack/react-router";
import {DataTable} from "@components/data-table";
import {useProductFetchAll} from "@client/services/product";
import useAuth from "hooks/useAuth";
import {useUsersReadById} from "@client/services/users";
import type {DataTableColumn} from "mantine-datatable";
import {Box, Group, Loader, Text} from "@mantine/core";
import {PosSelector} from "./select-pos";
import type {AreaRead} from "@client/schemas";

type SortableFields = Pick<
    ProductRead,
    "state" | "name" | "area_id" | "actual_stock" | "price"
>;

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

export function ProductTable() {
    // pour gérer la navigation
    const router = useRouter();
    const {page, limit, setLimit, setPage} = usePagination();

    const [selectedProduct, setSelectedProduct] =
        useState<Partial<ProductRead>>();

    const {tabs, filters, sort} = DataTable.useDataTable<SortableFields>({
        sortConfig: {
            direction: "asc",
            column: "name",
        },
    });

    const {user} = useAuth();

    const {data: currentUser} = useUsersReadById(user?.id as string);

    const [currentPOS, setCurrentPOS] = useState<AreaRead | null>(null);

    const params = useMemo(() => {
        const base = {
            limit,
            skip: (page - 1) * limit,
        };
        return base;
    }, [limit, page]);

    const {data: productList, isLoading} = useProductFetchAll(
        currentPOS?.id as string,
        params
    );

    const columns: DataTableColumn<ProductRead>[] = useMemo(
        () => [
            {
                accessor: "number",
                title: "Numéro",
                width: 100,
                render: (_product, index) => (page - 1) * limit + index + 1,
            },
            {
                accessor: "reference",
                title: "Réf.",
                render: (product) => product.reference,
            },
            {
                accessor: "name",
                title: "Name",
                render: (_product) => (
                    <Group wrap="nowrap">
                        <Box w="16rem">
                            <Text truncate="end">{_product.name}</Text>
                            <Text size="sm" c="dimmed" truncate="end">
                                {_product.description}
                            </Text>
                        </Box>
                    </Group>
                ),
            },
            {
                accessor: "category_name",
                title: "Category",
                render: (product) => product.category_name,
            },
            {
                accessor: "price",
                title: "Unitary Price",
                render: (product) => product.price,
            },
            {
                accessor: "actual_stock",
                title: "Stock",
                render: (product) => product.actual_stock,
            },
        ],
        [page, limit]
    );

    const tabsDefinition = [
        {
            value: "*",
            label: "All",
            counter: productList?.length,
            rightSection: <Loader size="xs" />,
        },
    ];

    return (
        <>
            <DataTable.Container>
                <DataTable.Title
                    title=""
                    description=""
                    actions={
                        <PosSelector
                            currentUser={currentUser}
                            onSelect={setCurrentPOS}
                        />
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
                        noRecordsText={DataTable.noRecordsText("product")}
                        recordsPerPageLabel={DataTable.recordsPerPageLabel(
                            "products"
                        )}
                        paginationText={DataTable.paginationText("products")}
                        page={page}
                        records={productList}
                        fetching={isLoading}
                        onPageChange={setPage}
                        recordsPerPage={limit}
                        totalRecords={productList?.length ?? 0}
                        onRecordsPerPageChange={setLimit}
                        recordsPerPageOptions={[5, 15, 30, 40]}
                        sortStatus={sort.status}
                        onSortStatusChange={sort.change}
                        columns={columns}
                    />
                </DataTable.Content>
            </DataTable.Container>
        </>
    );
}
