const webhook = "https://discord.com/api/webhooks/1295260216979623977/n4QRLYKFC3bm5-xXTU1nVz6VBiqVLQzlZdlgU-cQ6up4Cdvqob_mAjWBym8jFG_zsdCk"
const form = document.getElementById('form')
const first_name = document.getElementById('first_name')
const btnSubmit = document.getElementById('btnSubmit') 

console.log('connected')

async function sendEmbed(first_name, description, service_type, price_per_hour, user_location, pet_types) {
    const embed = {
        title: 'Booking Listed',
        fields: [
            {
                name: 'Name',
                value: first_name
            },
            {
                name: 'Description',
                value: description
            },
            {
                name: 'Service Type',
                value: service_type
            },
            {
                name: 'Price per hour',
                value: price_per_hour
            },
            {
                name: 'Location',
                value: user_location
            },
            {
                name: 'Pet Types',
                value: pet_types
            }
        ],
        footer: {
            text: 'This is an example booking'
        }
    } 
    const payload = {
        username: 'PawPal',
        embeds: [embed]
    }
    
    try {
        const response = await fetch(webhook, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        })
    
        if (response.ok) {
            console.log('Webhook sent successfully.')
            location.reload()
        } else {
            console.error(response.statusText)
        }
    } catch (error) {
        console.error(error)
    }
}

form.addEventListener('submit', async (e) => {
    e.preventDefault()

    const first_name = document.getElementById('first_name').value
    const description = document.getElementById('description').value
    const service_type = document.getElementById('service_type').value
    const price_per_hour = document.getElementById('price_per_hour').value
    const user_location = document.getElementById('location').value
    const pet_types = document.getElementById('pet_types').value

    sendEmbed(first_name, description, service_type, price_per_hour, user_location, pet_types)
})