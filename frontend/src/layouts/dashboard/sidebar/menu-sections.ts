import {paths} from "config/paths";
import type {ElementType} from "react";
import {
    PiArrowsInDuotone,
    PiChartLineUpDuotone,
    PiChatCenteredDotsDuotone,
    PiLayoutDuotone,
    PiLockKeyDuotone,
    PiPackageDuotone,
    PiShieldCheckDuotone,
    PiSquaresFourDuotone,
    PiStarDuotone,
    PiStorefrontDuotone,
    PiTableDuotone,
    PiUserPlusDuotone,
    PiUsersDuotone,
    PiWarehouseDuotone,
} from "react-icons/pi";

interface MenuItem {
    header: string;
    section: {
        name: string;
        href: string;
        icon: ElementType;
        dropdownItems?: {
            name: string;
            href: string;
            badge?: string;
        }[];
    }[];
}

export const menu: MenuItem[] = [
    {
        header: "Overview",
        section: [
            {
                name: "Welcome",
                href: paths.dashboard.home,
                icon: PiStarDuotone,
            },
            {
                name: "Dashboard",
                href: paths.dashboard.root,
                icon: PiLayoutDuotone,
            },
        ],
    },

    {
        header: "Stock",
        section: [
            {
                name: "Products",
                href: paths.dashboard.stock.root,
                icon: PiPackageDuotone,
            },
            {
                name: "Stock Movement",
                href: paths.dashboard.apps.kanban,
                icon: PiArrowsInDuotone,
            },
            {
                name: "Invotory",
                href: paths.dashboard.apps.kanban,
                icon: PiWarehouseDuotone,
            },
        ],
    },

    {
        header: "General Administration",
        section: [
            {
                name: "Users Management",
                icon: PiUsersDuotone,
                href: paths.dashboard.admin.management.owners.root,
                dropdownItems: [
                    {
                        name: "Owners Management",
                        href: paths.dashboard.admin.management.owners.root,
                    },
                    {
                        name: "User & Roles",
                        href: paths.dashboard.admin.management.users,
                    },
                ],
            },
            {
                name: "Point of Sales",
                href: paths.dashboard.admin.management.owners.pos.root,
                icon: PiStorefrontDuotone,
            },
        ],
    },

    {
        header: "Widgets",
        section: [
            {
                name: "Charts",
                href: paths.dashboard.widgets.charts,
                icon: PiChartLineUpDuotone,
            },
            {
                name: "Metrics",
                href: paths.dashboard.widgets.metrics,
                icon: PiSquaresFourDuotone,
            },
            {
                name: "Tables",
                href: paths.dashboard.widgets.tables,
                icon: PiTableDuotone,
            },
        ],
    },

    {
        header: "Authentication",
        section: [
            {
                name: "Register",
                href: paths.auth.register,
                icon: PiUserPlusDuotone,
            },
            {
                name: "Login",
                href: paths.auth.login,
                icon: PiShieldCheckDuotone,
            },
            {
                name: "Forgot Password",
                href: paths.auth.forgotPassword,
                icon: PiLockKeyDuotone,
            },
            {
                name: "OTP",
                href: paths.auth.otp,
                icon: PiChatCenteredDotsDuotone,
            },
        ],
    },
];
