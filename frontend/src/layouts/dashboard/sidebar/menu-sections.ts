import {paths} from "config/paths";
import type {ElementType} from "react";
import {
    PiChartLineUpDuotone,
    PiChatCenteredDotsDuotone,
    PiFilesDuotone,
    PiKanbanDuotone,
    PiLockKeyDuotone,
    PiShieldCheckDuotone,
    PiSquaresFourDuotone,
    PiStarDuotone,
    PiTableDuotone,
    PiUserPlusDuotone,
    PiUsersDuotone,
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
                name: "Documentation",
                href: paths.docs.root,
                icon: PiFilesDuotone,
            },
        ],
    },

    {
        header: "Apps",
        section: [
            {
                name: "Kanban",
                href: paths.dashboard.apps.kanban,
                icon: PiKanbanDuotone,
            },
        ],
    },

    {
        header: "Management",
        section: [
            {
                name: "Owners",
                icon: PiUsersDuotone,
                href: paths.dashboard.admin.management.owners.root,
                dropdownItems: [
                    {
                        name: "List",
                        href: paths.dashboard.admin.management.owners.list,
                    },
                    {
                        name: "Point of sale",
                        href: paths.dashboard.admin.management.owners.pos.root,
                    },
                ],
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
