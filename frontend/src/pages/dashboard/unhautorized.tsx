import classes from "./home.module.css";
import {Page} from "components/page";
import {UnhautorizedBackground} from "@components/404/Unhautorized";

export default function UnhautorizedPage() {
    return (
        <Page title="Unhautorized" className={classes.root}>
            <UnhautorizedBackground />
        </Page>
    );
}
