import config from "../config.json";
import { Anyty, AnytyDTO } from "../types/Anyty";

/**
 * Create a new Anyty in the application database.
 * 
 * @param anyty 
 */
export async function createAnyty(anytyDTO: AnytyDTO) {
    const URL = "anyty/create"

    return await fetch(`${config["host-url"]}/${URL}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(anytyDTO)
    }).then((response) => response);
}

/**
 * Get all anyties of the MetaAnyty specified by its
 * 
 * @param metaAnytyId 
 * @returns 
 */
export async function getAllAnyties(metaAnytyId: number): Promise<Anyty[]> {
    const URL = `anyty/${metaAnytyId}/all`

    let anyties = await fetch(`${config["host-url"]}/${URL}`, {
        method: 'GET',
        headers: { accept: 'application/json' }
    }).then(async (response) => {
        return await response.json();
    }).catch((r) => console.log(r))

    return anyties;
}