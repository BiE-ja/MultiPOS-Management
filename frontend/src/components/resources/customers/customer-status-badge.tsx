import {Badge, type BadgeProps} from "@mantine/core";

import {match} from "utilities/match";
import type {UserRead} from "@client/schemas";

interface UserStatusBadgeProps extends Omit<BadgeProps, "children" | "color"> {
    status: UserRead["is_active"];
}

export function UserStatusBadge({
    status,
    variant = "outline",
    ...props
}: UserStatusBadgeProps) {
    const color = match(
        [(status = true), "teal"],
        [(status = false), "orange"]
        //[status === "archived", "red"],
        //[true, "gray"]
    );

    return (
        <Badge color={color} variant={variant} {...props}>
            {status}
        </Badge>
    );
}
