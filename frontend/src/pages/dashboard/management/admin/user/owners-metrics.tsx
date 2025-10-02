import {
    //PiArchiveDuotone,
    PiPulseDuotone,
    PiUsersDuotone,
    PiShoppingBagDuotone,
} from "react-icons/pi";
import {Group, Loader, SimpleGrid} from "@mantine/core";
import {MetricCard} from "components/metric-card";
import {formatInt} from "utilities/number";
import {useUsersOwnersList} from "@client/services/users";

export function OwnerMetrics() {
    const {data: metrics, isLoading} = useUsersOwnersList();

    const cards = [
        {
            icon: PiUsersDuotone,
            title: "Total owners",
            value: metrics?.total,
            color: "blue",
        },
        {
            icon: PiPulseDuotone,
            title: "Active owners",
            value: metrics?.total_active,
            color: "teal",
        },
        {
            icon: PiShoppingBagDuotone,
            title: "Total Point of sale",
            value: metrics?.total_pos,
            color: "#009688",
        },
        /*{
            icon: PiArchiveDuotone,
            title: "Archived customers",
            value: metrics?.,
            color: "red",
        },*/
    ];

    return (
        <SimpleGrid cols={{base: 1, sm: 2, xl: 4}}>
            {cards.map((card) => (
                <MetricCard.Root key={card.title}>
                    <Group>
                        <MetricCard.Icon c={card.color}>
                            <card.icon size="2rem" />
                        </MetricCard.Icon>
                        <div>
                            <MetricCard.TextMuted>
                                {card.title}
                            </MetricCard.TextMuted>
                            <MetricCard.TextEmphasis>
                                {isLoading ? (
                                    <Loader size="sm" color={card.color} />
                                ) : (
                                    formatInt(card.value ?? 0)
                                )}
                            </MetricCard.TextEmphasis>
                        </div>
                    </Group>
                </MetricCard.Root>
            ))}
        </SimpleGrid>
    );
}
