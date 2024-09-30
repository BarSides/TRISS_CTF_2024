const express = require("express");
const {MongoClient} = require("mongodb");
const uuidv4 = require("uuid").v4;

const client = new MongoClient(process.env.MONGO_URL || "mongodb://root:example@localhost:27017");

const DBNAME = "auth"
const COLLECTION = "users"

function getCollection() {
    return client.db(DBNAME).collection(COLLECTION)
}

const messages = {
    logged_in: "Logged in!",
    invalid_credentials: "Ah ah ah you didn't say the magic word",
    internal_error: "Internal server error",
    not_found: "Resource not found."
}

function errmsg(message) {
    return {message}
}

const app = express()

app.use(express.json())
app.use(express.urlencoded({extended: true}))

const ID_LEN = 24

app.use(async (req, res, next) => {
    const api_key = req.headers["x-api-key"]

    if (!api_key) {
        return res.status(401).send(errmsg(messages.invalid_credentials))
    }

    const [corp_id, key_name] = api_key.split(':', 2)

    if (!corp_id || !key_name) {
        return res.status(401).send(errmsg(messages.invalid_credentials))
    }

    if (key_name.match(/[\(\)\.\*\+\{\}\\]+/ig)) {
        return res.status(400).send(errmsg("Whatchu tryin' to pull, anyway?"));
    }

    getCollection().findOne({
        corp_id, api_keys: {$regex: `^${key_name}$`}
    }).then((data) => {
        if (!!data) {
            console.log(`User found: ${data}`)
            req.user = {orgs: data.orgs, name: data.name, corp_id: data.corp_id}
            next()
        } else {
            console.log(`User not found ${api_key.substring(0, ID_LEN)}`)
            res.status(401).send(errmsg(messages.invalid_credentials))
        }
    }).catch((err) => {
        console.error(err)
        res.status(500).send(messages.internal_error)
    })
})

app.get("/users", async (req, res, next) => {
    getCollection().find({
        $or: req.user.orgs.map(orgs => {
            return {orgs}
        })
    }).project({_id: 0, orgs: 1, corp_id: 1, name: 1}).toArray().then((data) => {
        res.send(data)
    }).catch((err) => {
        res.status(500).send(err)
    })
})

app.post("/apikeys/:corp_id", async (req, res, next) => {
    if (req.params.corp_id !== req.user.corp_id) {
        return res.status(401).send(errmsg(messages.invalid_credentials))
    }

    if (!(req.body.api_key || '').match(/^[a-z0-9]{1,12}$/i)) {
        return res.status(400).send(errmsg("Invalid api key"))
    }

    getCollection().findOne({
        corp_id: req.params.corp_id,
    }).then(data => {
        if (!data) {
            return res.status(404).send(errmsg(messages.not_found))
        }
        if (data.api_keys.includes(req.body.api_key)) {
            return res.status(409).send()
        }
        getCollection().updateOne({
            _id: data._id
        }, {
            $push: {api_keys: req.body.api_key}
        }).then(data => {
            res.status(201).send()
        }).catch(
            err =>
                res.status(500).send(err)
        )
    }).catch(
        err =>
            res.status(500).send(err)
    )
})

app.get("/users/:corp_id", async (req, res, next) => {
    getCollection().findOne({
        $where: `(this.corp_id == '${req.user.corp_id}' && this.corp_id == '${req.params.corp_id}')`
    }).then(data => {
        if (!data) {
            return res.status(404).send(errmsg(messages.not_found))
        }
        if (req.user.orgs) {

        }
        return res.send(data)
    }).catch(err => {
        res.status(500).send(messages.internal_error)
    })
})

function user(name, orgs, keys) {
    const uuid = uuidv4();
    return {
        name, orgs, corp_id: uuid.substring(24), api_keys: !!keys ? keys : [uuid.substring(0, 8)]
    }
}

app.listen(8000, () => {
    const coll = getCollection()

    const WEYLAND_YUTANI = "Weyland-Yutani"
    const TYRELL = "Tyrell"

    Array.from([
        user("admin", [WEYLAND_YUTANI, TYRELL], ["Barsides{da87220bbb1245eb9cedd527c1c5544f}"]),
        user("trisstopher", [TYRELL]),
        user("trisstoph", [WEYLAND_YUTANI]),
        user("beatriss", [WEYLAND_YUTANI]),
        user("trissandra", [WEYLAND_YUTANI]),
        user("trissabelle", [TYRELL])
    ]).forEach(u =>
        coll.updateOne({name: u.name}, {$set: u}, {upsert: true})
            .then(data => console.log(data)).catch(err => console.error(err))
    )
    console.log("Database initialized")
    console.log("Server running on port 8000")
})
