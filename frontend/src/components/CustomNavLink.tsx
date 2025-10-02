import {NavLink} from "@mantine/core";
import {Link, useMatchRoute} from "@tanstack/react-router";

function CustomNavLink({to, label}: {to: string; label: string}) {
    const matchRoute = useMatchRoute();
    const isActive = !!matchRoute({to, fuzzy: true});

    return <NavLink component={Link} to={to} active={isActive} label={label} />;
}
export default CustomNavLink;
