import config from "../../config.json";

/**
 * Get all MetaAnyties from the backend.
 *
 * @returns
 */
export async function getAllMAnyties() {
  const URL = "meta-anyty/all";

  let mAnyties = await fetch(`${config["host-url"]}/${URL}`, {
    method: "GET",
    headers: { accept: "application/json" },
  })
    .then(async (response) => {
      return await response.json();
    })
    .catch((r) => console.error(r));
  return mAnyties;
}

/**
 * Get one MetaAnyty by its id.
 *
 * @param {number} mAnytyId
 * @returns
 */
export async function getOneMAnyty(mAnytyId) {
  const URL = `meta-anyty/${mAnytyId}`;

  let mAnyty = await fetch(`${config["host-url"]}/${URL}`, {
    method: "GET",
    headers: { accept: "application/json" },
  })
    .then(async (response) => {
      return await response.json();
    })
    .catch((r) => console.error(r));
  return mAnyty;
}
