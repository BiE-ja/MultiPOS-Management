import type {AreaRead, UserRead} from "@client/schemas";

import {
    CloseButton,
    Combobox,
    ComboboxChevron,
    Group,
    InputBase,
    useCombobox,
    Text,
    Input,
} from "@mantine/core";
import {useEffect, useState} from "react";

type POSSelectorProps = {
    currentUser: UserRead | undefined;
    onSelect: (area: AreaRead | null) => void;
};

function SelectOption(pos: AreaRead) {
    return (
        <Group>
            <div>
                <Text fz="sm" fw={500}>
                    {pos.name}
                </Text>
                <Text fz="xs" opacity={0.6}>
                    {pos.location}
                </Text>
            </div>
        </Group>
    );
}

export function PosSelector({currentUser, onSelect}: POSSelectorProps) {
    const combobox = useCombobox({
        onDropdownClose: () => {
            combobox.resetSelectedOption();
        },
    });
    const [value, setValue] = useState<string | null>(null);
    //const {data: areaScope} = useUsersAreaScope(currentUser?.id as string);

    const selectedOption =
        currentUser?.owned_areas?.find((pos) => pos.id === value) ?? null;
    const options = currentUser?.owned_areas?.map((pos) => {
        <Combobox.Option value={pos.id} key={pos.id}>
            <SelectOption {...pos} />
        </Combobox.Option>;
    });

    useEffect(() => {
        if (!currentUser?.owned_areas) return;
        onSelect(selectedOption);
    }, [currentUser, onSelect, selectedOption]);

    return (
        <Combobox
            onOptionSubmit={(val) => {
                setValue(val);
                combobox.closeDropdown();
            }}
            withinPortal={false}
            store={combobox}>
            <Combobox.Target>
                <InputBase
                    component="button"
                    type="button"
                    pointer
                    onClick={() => combobox.toggleDropdown()}
                    rightSectionPointerEvents={value === null ? "none" : "all"}
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
                        <Input.Placeholder>Pick POS value</Input.Placeholder>
                    ) : (
                        selectedOption && <SelectOption {...selectedOption} />
                    )}
                </InputBase>
            </Combobox.Target>
            <Combobox.Dropdown>{options?.length}</Combobox.Dropdown>
        </Combobox>
    );
}
