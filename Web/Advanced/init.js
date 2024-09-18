const {MongoClient} = require("mongodb");
const uuidv4 = require("uuid").v4;

console.log(process.env)
const client = new MongoClient(process.env.MONGO_URL || "mongodb://root:example@mongo:27017");

const DBNAME = "auth"
const COLLECTION = "users"

const WEYLAND_YUTANI = "Weyland-Yutani"
const TYRELL = "Tyrell"

function getCollection() {
    return client.db(DBNAME).collection(COLLECTION)
}

function user(name, orgs, keys) {
    const uuid = uuidv4();
    return {
        name, orgs, corp_id: uuid.substring(24), api_keys: !!keys ? keys : [uuid.substring(0, 8)]
    }
}

const coll = getCollection()

Array.from([
    user("admin", WEYLAND_YUTANI, ["Barsides{sneakers}"]),
    user("trisstopher", TYRELL),
    user("trisstoph", WEYLAND_YUTANI),
    user("beatriss", WEYLAND_YUTANI),
    {name: "trissandra", orgs: WEYLAND_YUTANI, corp_id: "1337b4da55", api_keys: ["secret"]},
    user("trissabelle", TYRELL)
]).forEach(u =>
    coll.updateOne({name: u.name}, {$set: u}, {upsert: true})
        .then(data=>console.log(data)).catch(err=>console.error(err))
)
