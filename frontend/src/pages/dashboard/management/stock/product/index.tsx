import {Grid, Tabs, Stack} from "@mantine/core";
import {ProductDetails} from "./product-details";
import {CategoriesTable} from "./categories";
import {ProductTable} from "./product-table";

export default function ProductListPage() {
    return (
        <Tabs defaultValue="list">
            <Tabs.List>
                <Tabs.Tab value="list">Product list</Tabs.Tab>
                <Tabs.Tab value="product">Product details</Tabs.Tab>
                <Tabs.Tab value="category">Categories</Tabs.Tab>
            </Tabs.List>
            <Tabs.Panel value="list">
                <Stack gap={4}>
                    <Grid>
                        <Grid.Col span={12}></Grid.Col>
                        <Grid.Col span={12}>
                            <ProductTable />
                        </Grid.Col>
                    </Grid>
                </Stack>
            </Tabs.Panel>
            <Tabs.Panel value="product">
                <Grid>
                    <Grid.Col span={12}></Grid.Col>
                    <Grid.Col span={12}>
                        <ProductDetails />
                    </Grid.Col>
                </Grid>
            </Tabs.Panel>
            <Tabs.Panel value="category">
                <CategoriesTable />
            </Tabs.Panel>
        </Tabs>
    );
}
