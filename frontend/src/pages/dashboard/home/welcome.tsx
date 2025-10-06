import {Anchor, Text, Title} from "@mantine/core";
import classes from "./welcome.module.css";

export function Welcome() {
    return (
        <>
            <Title className={classes.title} ta="center" mt={100}>
                Tongasoa eto amin'ny{" "}
                <Text
                    inherit
                    variant="gradient"
                    component="span"
                    gradient={{from: "pink", to: "yellow"}}>
                    Tantana Boutik'
                </Text>
            </Title>
            <Text c="dimmed" ta="center" size="lg" maw={580} mx="auto" mt="xl">
                Hitanao amin'ito rohy manaraka ito ireo{" "}
                <Anchor href="https://zita-products-list.mg/" size="lg">
                    Tolotra vokarin'i Zita Company
                </Anchor>
                . Vonona hatrany izahay hanome fahafaham-po anao.
            </Text>
        </>
    );
}
