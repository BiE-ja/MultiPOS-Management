import {setupWorker} from 'msw/browser'

const modules = import.meta.glob('../client/api/*.msw.ts',{eager:true})

const handlers = Object.values(modules).flatMap((mod: any)=>Object.values(mod))

export const worker = setupWorker(...handlers)

// For my own Mock Devtools

// worker.events.on('request:start',(req)=>{
//       window.postMessage(
//             {
//                 type: "MSW_REQUEST",
//                 playload: {
//                     method: req.request.method,
//                     url: req.request.url,  
//                     id: crypto.randomUUID(),
//                     timestamp: new Date().toISOString(), 
//                 }, 
//             },
//             '*'
//       );
//  });

// worker.events.on('request: match', (req)=>{
//     window.postMessage(
//         {
//             type: "MSW_RESPONSE",
//             paylod: {
//                 id: req.id,
//                 status: 200,
//             },
//         },
//         '*'
//     );

// });
 

