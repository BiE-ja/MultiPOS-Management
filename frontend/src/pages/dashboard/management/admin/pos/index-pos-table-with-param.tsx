import {useParams} from "@tanstack/react-router";
import {paths} from "config/paths";
import POSPage from ".";

export default function ListPos() {
    const {ownerId} = useParams({
        from: paths.dashboard.admin.management.owners.pos.withParam,
    });

    return POSPage(ownerId);
}
