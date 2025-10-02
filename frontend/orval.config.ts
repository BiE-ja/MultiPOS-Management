import {defineConfig} from "orval";
import dotenv from "dotenv";

dotenv.config();

export default defineConfig({
    api: {
        input: "./openapi.json",
        output: {
            target: "./src/client/services",
            schemas: "./src/client/schemas",
            client: "react-query",
            mode: "tags",
            override: {
                mutator: {
                    path: "./src/client/custom-client.ts", // optionnel si tu veux un axios préconfiguré
                    name: "customAxios",
                },
                query: {
                    useQuery: true,
                    useMutation: true,
                    useInfinite: true,
                },
                useDates: true,
            },
            //mock: true, // generate mock data (simulate backend responses)
        },
    },
    petstoreZod: {
        input: "./openapi.json",
        output: {
            mode: "tags",
            target: "./src/client/schemas/zod",
            client: "zod",
            fileExtension: ".zod.ts",
        },
    },
});
