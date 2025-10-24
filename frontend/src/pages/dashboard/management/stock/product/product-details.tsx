import type {ProductRead} from "@client/schemas";
import {FormProvider} from "@components/forms/form-provider";
import {Page} from "@components/page";
import {
    Button,
    Center,
    Group,
    Stack,
    TextInput,
    Textarea,
    type StackProps,
} from "@mantine/core";
import {useState} from "react";

interface ProductDetailsProps extends Omit<StackProps, "children"> {
    product?: ProductRead;
}
export function ProductDetails({product, ...props}: ProductDetailsProps) {
    const [enable, setEnable] = useState(false);

    const activeEdition = () => {
        setEnable(true);
    };
    return (
        <Page title="product">
            <Center>
                <Stack gap="xl">
                    <Button variant="default" size="xs" onClick={activeEdition}>
                        {product ? "Edit product" : "Add new product"}
                    </Button>
                    <Stack {...props}>
                        <TextInput disabled={enable} label="Reference" />
                        <TextInput readOnly={enable} label="Name" />
                        <Textarea readOnly={enable} label="Description" />
                        <Group grow>
                            <TextInput readOnly={enable} label="Price" />
                            <TextInput
                                readOnly={enable}
                                label="Purchase price"
                            />
                        </Group>
                        <Group>
                            <TextInput
                                readOnly={enable}
                                label="Initial stock"
                            />
                            <TextInput readOnly={enable} label="Actual Stock" />
                        </Group>
                    </Stack>
                </Stack>
            </Center>
        </Page>
    );
}
