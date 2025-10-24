import {useUsersOwnersList} from "@client/services/users";
//import {Spotlight, type SpotlightActionData} from "@mantine/spotlight";

import {PiMagnifyingGlassBold as SearchIcon, PiUser} from "react-icons/pi";
import type {UserRead} from "@client/schemas";
//import {secondStore} from "layouts/dashboard/spotlightstore";
import {
    Combobox,
    Group,
    useCombobox,
    Text,
    InputBase,
    CloseButton,
    ComboboxChevron,
    Input,
} from "@mantine/core";
import {useEffect, useState} from "react";

type OwnerSelectorProps = {
    onSelect: (owner: UserRead | null) => void;
};

function SelectOption(owner: UserRead) {
    return (
        <Group>
            <PiUser size={24} />
            <div>
                <Text fz="sm" fw={500}>
                    {owner.last_name} {owner.name}
                </Text>
                <Text fz="xs" opacity={0.6}>
                    {owner.email}
                </Text>
            </div>
        </Group>
    );
}

export function OwnerSelector({onSelect}: OwnerSelectorProps) {
    const {data: owners} = useUsersOwnersList();

    /*const actions: SpotlightActionData[] = owners
        ? owners.data.map((owner: UserRead) => ({
              id: owner.id,
              label: `${owner.name} ${owner.last_name}`,
              description: `Email: ${owner.email} - Phone: ${owner.phone}`,
              leftSection: <PiUser size={24} />,
              onClick: () => onSelect(owner),
          }))
        : [];*/
    const [search, setSearch] = useState("");
    const combobox = useCombobox({
        onDropdownClose: () => {
            combobox.resetSelectedOption();
            combobox.focusTarget();
            setSearch("");
        },
        onDropdownOpen: () => {
            combobox.focusSearchInput();
        },
    });

    const [value, setValue] = useState<string | null>(null);

    const shouldFilteredOptions =
        owners?.data.every(
            (owner) =>
                owner.last_name !== search &&
                owner?.name !== search &&
                owner.email !== search
        ) ?? false;

    const filteredOptions = shouldFilteredOptions
        ? owners
            ? owners.data.filter(
                  (owner) =>
                      owner.last_name
                          .toLowerCase()
                          .includes(search.toLowerCase().trim()) ||
                      owner.name
                          ?.toLocaleLowerCase()
                          .includes(search.toLowerCase().trim())
              )
            : undefined
        : owners?.data;

    const selectedOption =
        owners?.data.find((owner) => owner.last_name === value) ??
        owners?.data.find((owner) => owner.email === value) ??
        owners?.data.find((owner) => owner?.name === value) ??
        null;

    const options = filteredOptions?.map((owner) => (
        <Combobox.Option
            value={owner.last_name && (owner?.name as string)}
            key={owner.id}>
            <SelectOption {...owner} />
        </Combobox.Option>
    ));

    // Find in the data the user ('owner') selected in the combobox
    useEffect(() => {
        if (!owners?.data) return;
        onSelect(selectedOption);
    }, [selectedOption, onSelect, owners]);

    return (
        /*<Spotlight
            store={secondStore}
            actions={actions}
            nothingFound="Nothing found..."
            highlightQuery
            searchProps={{
                leftSection: <SearchIcon />,
                placeholder: "Choisir un propriétaire",
            }}
        />*/
        <Combobox
            onOptionSubmit={(val) => {
                setValue(val);
                setSearch(val);
                combobox.closeDropdown();
            }}
            withinPortal
            store={combobox}>
            <Combobox.Target>
                <InputBase
                    component="button"
                    type="button"
                    pointer
                    onClick={() => combobox.toggleDropdown()}
                    rightSectionPointerEvents={value === null ? "none" : "all"}
                    multiline
                    leftSection={value === null && <SearchIcon />}
                    rightSection={
                        value !== null ? (
                            <CloseButton
                                size="sm"
                                onMouseDown={(event) => event.preventDefault()}
                                onClick={() => setValue(null)}
                                aria-label="Clear value"
                            />
                        ) : (
                            <ComboboxChevron />
                        )
                    }>
                    {value === null ? (
                        <Input.Placeholder>Pick owner value</Input.Placeholder>
                    ) : (
                        selectedOption && <SelectOption {...selectedOption} />
                    )}
                </InputBase>
            </Combobox.Target>
            <Combobox.Dropdown>
                <Combobox.Search
                    value={search}
                    onChange={(event) => setSearch(event.currentTarget.value)}
                    placeholder="Search a owner"
                />
                <Combobox.Options>
                    {options?.length ? (
                        options.length > 0 ? (
                            options
                        ) : (
                            <Combobox.Empty>Nothing found</Combobox.Empty>
                        )
                    ) : (
                        <Combobox.Empty>Nothing found</Combobox.Empty>
                    )}
                </Combobox.Options>
            </Combobox.Dropdown>
        </Combobox>
    );
}
