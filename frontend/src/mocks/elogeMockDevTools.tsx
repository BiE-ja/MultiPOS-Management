/**
 * One Basic Devtools for Mock
 * Use for Dev only
 * Add the component in main or your global layout
 * Integration in MSW is necessary
 * worker.events.on('request:start,(req)=>{
 *      window.postMessage(
 *          {
 *              type: "MSW_REQUEST",
 *              playload: {
 *                  method: req.method,
 *                  url: req.url.href,    
 *              },
 *          }
 *      );
 * });
 */

import{
    Box, Badge, Button, 
    Drawer, DrawerBody, DrawerContent, DrawerHeader, DrawerOverlay,
    IconButton, Text, VStack, useDisclosure
}from '@chakra-ui/react';

import { useEffect, useState } from 'react';
import { set } from 'react-hook-form';
import { LuMonitor } from 'react-icons/lu';

type MockRequest = {
    id: string;
    method: string
    url: string;
    timestamp: string;
    status?:number
};

type ElogeMockDevtoolsProps = {
    hastoolsleft?: boolean;
    hastoolsright?: boolean;
};


export function ElogeMockDevtolls ({
    hastoolsleft = false,
    hastoolsright = false,
    }:ElogeMockDevtoolsProps){
        const {open, onOpen, onClose} =useDisclosure();
        const [requests, setRequests] = useState<MockRequest>([]);

        useEffect(()=>{
            const listener = (event: any)=>{
                if (event.data?.type === "MSW_REQUEST"){
                    const {id, method, url, timestamp} = event.data.playload;
                    setRequests((prev)=>[
                        {id,method,url,timestamp},
                        ...prev,
                    ]);
                }
                if (event.data?.type === "MSW_RESPENSE"){
                    const {id, status} = event.data.playload;
                    setRequests((prev)=>prev.timestamp((req)=>req.id === id? {...req, status}:req));
                }
            };
            window.addEventListener("message", listener);
            return ()=> window.removeEventListener("message", listener);
        },[]);

        return(
        <>
            <IconButton
                aria-label='Eloge Mock Devtools'
                icon = {<LuMonitor/>}
                position ="fixed"
                bottom = {hasQueryDevtools || hasRouterDevtools? "4rem":"1rem"}
                right = "1rem"
                zIndex = {9999}
                colorScheme="teal"
                borderRadius="full"
                boxShadow="lg"
                onClick={onOpen}
            />
            <Drawer isOpen={open} placement="right" onClose={onClose} size = "sm">
                <DrawerOverlay/>
                <DrawerContent>
                    <DrawerHeader bg="teal.500" color="white">
                        Eloge Mock Devtools
                    </DrawerHeader>
                    <DrawerBody>
                        <VStack align="stretch" spacing={3}>
                            {requests.length === 0 &&(
                                <Text color="gray.500">No Mock request yet.</Text>
                            )}
                            {requests.map((req)=>(
                                <Box key={req.id} p={3} borderWidth={1} borderRadius={lg}>
                                    <Badge colorScheme="purple" mr={2}>{req.method}</Badge>
                                    <Text fontSize="sm" isTruncated>{req.url}</Text>
                                    <Text fontSize="xs" color="gray.500">{req.timestamp}</Text>
                                    {req.status!==undefined && (
                                        <Badge mt="1" colorScheme={req.status<300?"green":"red"}>{req.status}</Badge>
                                    )}
                                </Box>
                            ))}    
                        </VStack>       
                    </DrawerBody>
                </DrawerContent>
            </Drawer>
        </>  
        );
    }
)
    