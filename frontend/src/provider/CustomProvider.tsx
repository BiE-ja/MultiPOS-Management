import "@mantine/carousel/styles.layer.css";
import "@mantine/charts/styles.layer.css";
import "@mantine/code-highlight/styles.layer.css";
import "@mantine/core/styles.layer.css";
import "@mantine/dates/styles.layer.css";
import "@mantine/dropzone/styles.layer.css";
import "@mantine/notifications/styles.layer.css";
import "@mantine/nprogress/styles.layer.css";
import "@mantine/spotlight/styles.layer.css";
import "@mantine/tiptap/styles.layer.css";
import "mantine-datatable/styles.layer.css";
import "global.css";

import {MantineProvider} from "@mantine/core";
import {ModalsProvider} from "@mantine/modals";
import {Notifications} from "@mantine/notifications";
import {NavigationProgress} from "@mantine/nprogress";

import {theme} from "@theme/index";
import type {PropsWithChildren} from "react";
import {AuthProvider} from "./auth-provider";

export function CustomProvider(props: PropsWithChildren) {
    return (
        <AuthProvider>
            <MantineProvider theme={theme}>
                <Notifications position="bottom-center" />
                <NavigationProgress />
                <ModalsProvider>{props.children}</ModalsProvider>
            </MantineProvider>
        </AuthProvider>
    );
}

export default CustomProvider;
