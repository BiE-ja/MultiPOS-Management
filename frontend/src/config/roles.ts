// src/config/roles.ts

import {paths} from "./paths";

export const roles = {
    admin: {
        label: "Administrator",
        dashboardPath: "/dashboard/admin",
        permissions: ["manage_users", "manage_roles", "view_reports"],
    },
    owner: {
        label: "Owner",
        dashboardPath: "/dashboard/owner",
        permissions: ["manage_pos", "view_sales"],
    },
    manager: {
        label: "Manager",
        dashboardPath: "/dashboard/manager",
        permissions: ["view_team", "manage_orders"],
    },
    stockKeeper: {
        label: "Stock Keeper",
        dashboardPath: "/dashboard/stock-keeper",
        permissions: ["manage_inventory"],
    },
    saler: {
        label: "Saler",
        dashboardPath: "/dashboard/saler",
        permissions: ["process_sales"],
    },
    backOffice: {
        label: "Back Office",
        dashboardPath: "/dashboard/back-office",
        permissions: ["manage_finance"],
    },
    // etc.
} as const;

// Get dashbord path for a given role
export function getDashboardPathForRole(role: string): string {
    const userRole = role as keyof typeof roles;
    return roles[userRole]?.dashboardPath || paths.dashboard.home; // fallback to root if role not found

    //role: keyof typeof roles
}

// List of all permissions
export const allPermissions = Array.from(
    new Set(Object.values(roles).flatMap((role) => role.permissions))
);

// Check if a role has a specific permission
export function roleHasPermission(
    role: keyof typeof roles,
    permission: string
) {
    return roles[role]?.permissions.includes(permission);
}

// Example usage:
// const adminPath = getDashboardPathForRole('admin'); // "/dashboard/admin"
// const hasPermission = roleHasPermission('owner', 'manage_users'); // false
