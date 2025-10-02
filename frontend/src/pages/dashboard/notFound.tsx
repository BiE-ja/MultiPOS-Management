import {NothingFoundBackground} from "@components/404/NotFoundBackground";
import classes from "./home.module.css";
import {Page} from "components/page";

export default function NotFoundPage() {
    return (
        <Page title="404" className={classes.root}>
            <NothingFoundBackground />
        </Page>
    );
}
