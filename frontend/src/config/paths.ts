//import docs from 'pages/docs/paths';

import type {FileRoutesByPath} from "@tanstack/react-router";

export const paths = {
    docs: {
        root: "/docs" as keyof FileRoutesByPath,
        introduction: "/docs/introduction" as keyof FileRoutesByPath,
        gettingStarted: "/docs/getting-started" as keyof FileRoutesByPath,
    },
    index: {
        root: "/" as keyof FileRoutesByPath,
        home: "/home" as keyof FileRoutesByPath,
        about: "/about" as keyof FileRoutesByPath,
        contact: "/contact" as keyof FileRoutesByPath,
        terms: "/terms" as keyof FileRoutesByPath,
        privacy: "/privacy" as keyof FileRoutesByPath,
        faq: "/faq" as keyof FileRoutesByPath,
    },

    auth: {
        root: "/auth" as keyof FileRoutesByPath,
        login: "/auth/login" as keyof FileRoutesByPath,
        register: "/auth/register" as keyof FileRoutesByPath,
        forgotPassword: "/auth/forgot-password" as keyof FileRoutesByPath,
        resetPassword: "/auth/reset-password" as keyof FileRoutesByPath,
        otp: "/auth/otp" as keyof FileRoutesByPath,
        terms: "/auth/terms" as keyof FileRoutesByPath,
        privacy: "/auth/privacy" as keyof FileRoutesByPath,
    },

    dashboard: {
        root: "/dashboard" as keyof FileRoutesByPath,
        home: "/dashboard/home" as keyof FileRoutesByPath,
        unhautorized: "/unauthorized" as keyof FileRoutesByPath,
        notFound: "/not-found" as keyof FileRoutesByPath,
        admin: {
            root: "/dashboard/admin" as keyof FileRoutesByPath,
            home: "/dashboard/admin/home" as keyof FileRoutesByPath,
            management: {
                root: "dashboard/admin/management" as keyof FileRoutesByPath,
                users: "/dashboard/admin/management/users-list" as keyof FileRoutesByPath,
                owners: {
                    root: "/dashboard/admin/management/owners-list" as keyof FileRoutesByPath,
                    withParam:
                        "/dashboard/admin/management/owners/$ownerId" as keyof FileRoutesByPath,
                    //list: "/dashboard/admin/management/owners-list" as keyof FileRoutesByPath,
                    create: "/dashboard/admin/management/owners/create" as keyof FileRoutesByPath,
                    edit: "/dashboard/admin/management/owners/$ownerId/edit" as keyof FileRoutesByPath,
                    delete: "/dashboard/admin/management/owners/$ownerId/delete" as keyof FileRoutesByPath,
                    pos: {
                        root: "/dashboard/admin/management/owners-pos" as keyof FileRoutesByPath,
                        withParam:
                            "dashboard/admin/management/owners/pos/$ownerId" as keyof FileRoutesByPath,
                        users: {
                            list: "/dashboard/admin/management/owners/$ownerId/pos/$posId/users" as keyof FileRoutesByPath,
                        },
                    },
                },
            },

            settings: {
                root: "/dashboard/admin/settings" as keyof FileRoutesByPath,
                general:
                    "/dashboard/admin/settings/general" as keyof FileRoutesByPath,
                security:
                    "/dashboard/admin/settings/security" as keyof FileRoutesByPath,
                notifications:
                    "dashboard/admin/settings/notifications" as keyof FileRoutesByPath,
            },
        },

        owner: {
            root: "/dashboard/owner" as keyof FileRoutesByPath,
            home: "/dashboard/owner/home" as keyof FileRoutesByPath,
            pos: {
                root: "/dashboard/owner/pos" as keyof FileRoutesByPath,
                list: "/dashboard/owner/pos/list" as keyof FileRoutesByPath,
                create: "dashboard/owner/pos/create" as keyof FileRoutesByPath,
                edit: (posId: string) =>
                    `/owner/pos/${posId}/edit` as keyof FileRoutesByPath,
                view: (posId: string) =>
                    `/owner/pos/${posId}` as keyof FileRoutesByPath,
                delete: (posId: string) =>
                    `/owner/pos/${posId}/delete` as keyof FileRoutesByPath,
            },
        },

        stock: {
            root: "/dashboard/stock/product" as keyof FileRoutesByPath,
            movement: "/dashboard/stock/movement" as keyof FileRoutesByPath,
            invotory: "/dashboard/stock/inventory" as keyof FileRoutesByPath,
        },

        apps: {
            root: "/dashboard/apps" as keyof FileRoutesByPath,
            kanban: "/dashboard/apps/kanban" as keyof FileRoutesByPath,
        },
        widgets: {
            root: "/dashboard/widgets" as keyof FileRoutesByPath,
            metrics: "/dashboard/widgets/metrics" as keyof FileRoutesByPath,
            charts: "/dashboard/widgets/charts" as keyof FileRoutesByPath,
            tables: "/dashboard/widgets/tables" as keyof FileRoutesByPath,
        },
    },
};

export const buildPaths = {
    editOwner: (ownerId: string) =>
        `/dashboard/admin/management/owners/${ownerId}/edit`,
    viewOwner: (ownerId: string) =>
        `/dashboard/admin/management/owners/${ownerId}`,
    deleteOwner: (ownerId: string) =>
        `/dashboard/admin/management/owners/${ownerId}/delete`,
    posList: (ownerId: string) =>
        `/dashboard/admin/management/owners/pos/${ownerId}`,
    posUserList: (ownerId: string, posId: string) =>
        `/dashboard/admin/management/owners/${ownerId}/pos/${posId}/users`,
    viewPos: (ownerId: string, posId: string) =>
        `/dashboard/admin/management/owners/${ownerId}/pos/${posId}/`,
};
