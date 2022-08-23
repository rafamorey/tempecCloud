// exportamos las respuestas de success y error

// la funcion responde con una peticion req, una respuesta res, un mensaje y el status de la respuesta

exports.success = function(req, res, message, status)
{   
    // la respuesta incluye el status y se envia un objeto indicando que no hubo error y un body con el mensaje de la respuesta
    res.status(status).send({
        error: "",
        body: message
    })
}

// la funcion responde con una peticion req, una respuesta res, un mensaje, el status de la respuesta y los detalles del error encontrado

exports.error = function(req, res, message, status, details) {

    // imprimo los detalles del error para intentar hubicarlo
    console.error('[response error]' + details)
    // respondemos el status del error y en caso de no encontrarlo mandamos un 500 default, con el mensaje como error y el body vacio
    res.status(status || 500).send({
        error: message,
        body: ""
    })
}