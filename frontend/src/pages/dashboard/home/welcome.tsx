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
                Raha hijery tolotra hafa inoana fa hanamora ny fiainanao +
                Tsidiho{" "}
                <Anchor href="https://zita-products-list.mg/" size="lg">
                    Tolotra novokarin'i Zita
                </Anchor>
                . Vonona hatrany izahay hanome fahafaham-po anao.
            </Text>
        </>
    );
}
