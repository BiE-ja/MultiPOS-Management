//import docs from 'pages/docs/paths';

import type {ZodInt, ZodNumber} from "zod";

export const paths = {
    //docs,
    index: {
        root: "/",
        home: "/home",
        about: "/about",
        contact: "/contact",
        terms: "/terms",
        privacy: "/privacy",
        faq: "/faq",
    },

    auth: {
        root: "/auth",
        login: "/auth/login",
        register: "/auth/register",
        forgotPassword: "/auth/forgot-password",
        resetPassword: "/auth/reset-password",
        otp: "/auth/otp",
        terms: "/auth/terms",
        privacy: "/auth/privacy",
    },

    dashboard: {
        root: "/dashboard",
        home: "/dashboard/home",

        admin: {
            root: "/dashboard/admin",
            home: "/dashboard/admin/home",
            management: {
                root: "dashboard/admin/management",
                owners: {
                    root: "/dashboard/admin/management/owners",
                    list: "/dashboard/admin/management/owners/list",
                    create: "/dashboard/admin/management/owners/create",
                    edit: (ownerId: string) =>
                        `/dashboard/admin/management/owners/${ownerId}/edit`,
                    view: (ownerId: string) =>
                        `/dashboard/admin/management/owners/${ownerId}`,
                    delete: (ownerId: string) =>
                        `/dashboard/admin/management/owners/${ownerId}/delete`,
                    pos: {
                        root: (ownerId: string) =>
                            `/dashboard/admin/management/owners/${ownerId}/pos`,
                        list: (ownerId: string) =>
                            `/dashboard/admin/management/owners/${ownerId}/pos/list`,
                        create: (ownerId: string) =>
                            `/dashboard/admin/management/owners/${ownerId}/pos/create`,
                        edit: (ownerId: string, posId: string) =>
                            `/dashboard/admin/management/owners/${ownerId}/pos/${posId}/edit`,
                        view: (ownerId: string, posId: string) =>
                            `/dashboard/admin/management/owners/${ownerId}/pos/${posId}`,
                        delete: (ownerId: string, posId: string) =>
                            `/dashboard/admin/management/owners/${ownerId}/pos/${posId}/delete`,
                        users: {
                            root: (ownerId: string, posId: string) =>
                                `/dashboard/admin/management/owners/${ownerId}/pos/${posId}/users`,
                            list: (ownerId: string, posId: string) =>
                                `/dashboard/admin/management/owners/${ownerId}/pos/${posId}/users/list`,
                            create: (ownerId: string, posId: string) =>
                                `/dashboard/admin/management/owners/${ownerId}/pos/${posId}/users/create`,
                            edit: (
                                ownerId: string,
                                posId: string,
                                userId: string
                            ) =>
                                `/dashboard/admin/management/owners/${ownerId}/pos/${posId}/users/${userId}/edit`,
                            view: (
                                ownerId: string,
                                posId: string,
                                userId: string
                            ) =>
                                `/dashboard/admin/management/owners/${ownerId}/pos/${posId}/users/${userId}`,
                            delete: (
                                ownerId: string,
                                posId: string,
                                userId: string
                            ) =>
                                `/dashboard/admin/management/owners/${ownerId}/pos/${posId}/users/${userId}/delete`,
                        },
                    },
                },
            },

            settings: {
                root: "/dashboard/admin/settings",
                general: "/dashboard/admin/settings/general",
                security: "/dashboard/admin/settings/security",
                notifications: "dashboard/admin/settings/notifications",
            },
        },

        owner: {
            root: "/dashboard/owner",
            home: "/dashboard/owner/home",
            pos: {
                root: "/dashboard/owner/pos",
                list: "/dashboard/owner/pos/list",
                create: "dashboard/owner/pos/create",
                edit: (posId: string) => `/owner/pos/${posId}/edit`,
                view: (posId: string) => `/owner/pos/${posId}`,
                delete: (posId: string) => `/owner/pos/${posId}/delete`,
            },
        },

        apps: {
            root: "/dashboard/apps",
            kanban: "/dashboard/apps/kanban",
        },
        widgets: {
            root: "/dashboard/widgets",
            metrics: "/dashboard/widgets/metrics",
            charts: "/dashboard/widgets/charts",
            tables: "/dashboard/widgets/tables",
        },
    },
};
