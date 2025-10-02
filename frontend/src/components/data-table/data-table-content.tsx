import {forwardRef} from "react";
import {
    CardSection,
    type CardSectionProps,
    type ElementProps,
} from "@mantine/core";

export const DataTableContent = forwardRef<
    HTMLDivElement,
    CardSectionProps & ElementProps<"div", keyof CardSectionProps>
>(({children}, ref) => <CardSection ref={ref}>{children}</CardSection>);
