const express = require("express");
const {MongoClient} = require("mongodb");
const uuidv4 = require("uuid").v4;

const client = new MongoClient(process.env.MONGO_URL || "mongodb://root:example@localhost:27017");

const DBNAME = "auth"
const COLLECTION = "users"

const WEYLAND_YUTANI = "Weyland-Yutani"
const TYRELL = "Tyrell"

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
        return res.status(400).send(errmsg(
            "Disallowed regex value(s) detected.  Please enter your API key and don't try to hack the system."
        ));
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
        res.status(500).send(err.toString())
    })
})

app.get("/users", async (req, res, next) => {
    getCollection().find({
        $or: (req.user.orgs || []).map(orgs => {
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

    if (req.body.api_key === undefined) {
        return res.status(400).send(errmsg('Field missing: api_key'))
    }

    if (!(req.body.api_key || '').match(/^[a-z0-9]{1,12}$/i)) {
        return res.status(400).send(errmsg("API key must be alphanumeric and 1 to 12 characters."))
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

        res.status(501).send(errmsg("key successfully validated. TODO: get the intern to code db write logic."))
    }).catch(
        err =>
            res.status(500).send(err.toString())
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
        res.status(500).send(err.toString())
    })
})

function user(name, orgs, keys, corp_id) {
    return {
        name, orgs, corp_id: corp_id || uuidv4().substring(24), api_keys: !!keys ? keys : [uuidv4().substring(0, 8)]
    }
}

const port = parseInt(process.env.PORT || "8000")

app.listen(port, () => {
    getCollection().drop().then(() => {
        Array.from([
            user("admin", [WEYLAND_YUTANI, TYRELL], ["Barsides{8a6e053f-ac6e-492b-b83b-72adf192482f}"]),
            user("trisstopher", [TYRELL]),
            user("trisstoph", [WEYLAND_YUTANI]),
            user("beatriss", [WEYLAND_YUTANI]),
            user("trissandra", [WEYLAND_YUTANI], undefined, "1337b4da55"),
            user("trissabelle", [TYRELL])
        ]).forEach(u =>
            getCollection().updateOne({name: u.name}, {$set: u}, {upsert: true})
                .then(data => console.log(data)).catch(err => console.error(err))
        )
        console.log("Database initialized")
    })
        .catch(err => console.error(err))
    console.log(`Server running on ${port}`)
})
