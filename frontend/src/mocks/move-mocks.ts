/**
 * Déplace tous les fichiers mock vers une repertoire dédié
 * 
 */

import fs from 'fs'
import path from 'path'

const BASE_DIR_SERVICES = './src/client/services'
const MOCK_DIR_SERVICES = './src/client/services/mock'
const BASE_DIR_SCHEMA = './src/client/schemas'
const MOCK_DIR_SCHEMA = './src/client/schemas/mock'

fs.mkdirSync(MOCK_DIR_SERVICES, {recursive:true})

const files = fs.readdirSync(BASE_DIR_SERVICES)

for (const file of files){
    const srcPath_service = path.join(BASE_DIR_SERVICES,file)
    const destPath_service = path.join(MOCK_DIR_SERVICES, file)

    fs.renameSync(srcPath_service, destPath_service)
}

fs.mkdirSync(MOCK_DIR_SCHEMA, {recursive:true})

const files_2 = fs.readdirSync(BASE_DIR_SCHEMA)

for (const file of files_2){
    const srcPath_schema = path.join(BASE_DIR_SCHEMA,file)
    const destPath_schema = path.join(MOCK_DIR_SCHEMA, file)
    fs.renameSync(srcPath_schema, destPath_schema)

}
