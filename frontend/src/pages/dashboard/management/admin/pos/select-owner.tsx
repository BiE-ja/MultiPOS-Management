import {useUsersOwnersList} from "@client/services/users";
import {Spotlight, type SpotlightActionData} from "@mantine/spotlight";

import {PiMagnifyingGlassBold as SearchIcon, PiUser} from "react-icons/pi";
import type {UserRead} from "@client/schemas";
import {secondStore} from "layouts/dashboard/spotlightstore";

type OwnerSelectorProps = {
    onSelect: (owner: UserRead) => void;
};

export function OwnerSelector({onSelect}: OwnerSelectorProps) {
    const {data: owners} = useUsersOwnersList();

    const actions: SpotlightActionData[] = owners
        ? owners.data.map((owner: UserRead) => ({
              id: owner.id,
              label: `${owner.name} ${owner.last_name}`,
              description: `Email: ${owner.email} - Phone: ${owner.phone}`,
              leftSection: <PiUser size={24} />,
              onClick: () => onSelect(owner),
          }))
        : [];

    return (
        <Spotlight
            store={secondStore}
            actions={actions}
            nothingFound="Nothing found..."
            highlightQuery
            searchProps={{
                leftSection: <SearchIcon />,
                placeholder: "Choisir un propriétaire",
            }}
        />
    );
}
