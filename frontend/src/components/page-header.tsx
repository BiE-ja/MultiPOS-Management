import {type ReactNode} from "react";

import {
    type GroupProps,
    type ElementProps,
    Title,
    Breadcrumbs,
    Anchor,
    Text,
    Group,
} from "@mantine/core";
import CustomNavLink from "./CustomNavLink";

interface PageHeaderProps
    extends Omit<GroupProps, "title">,
        ElementProps<"header", keyof GroupProps> {
    title: ReactNode;
    breadcrumbs?: {label: string; href?: string}[];
}

export function PageHeader({
    children,
    title,
    breadcrumbs,
    className,
    mb = "xl",
    ...props
}: PageHeaderProps) {
    return (
        <Group
            component="header"
            justify="space-between"
            className={className}
            mb={mb}
            {...props}>
            <div>
                <Title component="h2" order={2}>
                    {title}
                </Title>

                {breadcrumbs && (
                    <Breadcrumbs mt="sm">
                        {breadcrumbs.map((breadcrumb) =>
                            breadcrumb.href ? (
                                <Anchor
                                    fz="sm"
                                    underline="never"
                                    c="inherit"
                                    component={CustomNavLink}
                                    key={breadcrumb.label}
                                    to={breadcrumb.href}
                                    label={breadcrumb.label}
                                />
                            ) : (
                                <Text key={breadcrumb.label} c="dimmed" fz="sm">
                                    {breadcrumb.label}
                                </Text>
                            )
                        )}
                    </Breadcrumbs>
                )}
            </div>

            {children}
        </Group>
    );
}
