const { generate } = require('youtube-po-token-generator')
const fs = require('fs')

function Write(x){
    console.log(x)
    let data = '{"access_token": null, "refresh_token": null, "expires":  null, "visitorData": '+'"'+x.visitorData+'", "po_token": '+x.poToken+'"}'
    fs.writeFile('Mytokens.txt', data, function (err) {
        if (err) {
            return console.error(err);
        }

        // If no error the remaining code executes
        console.log(" Finished writing ");
    })
}


generate().then(Write, console.error)