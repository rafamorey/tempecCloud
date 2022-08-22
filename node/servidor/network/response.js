exports.success = function(req, res, message, status)
{
    res.status(status).send({
        error: "",
        body: message
    })
}

exports.error = function(req, res, message, status, details) {
    console.error('[response error]' + details)
    res.status(status || 500).send({
        error: message,
        body: ""
    })
}