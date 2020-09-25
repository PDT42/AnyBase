// Auth: PDT
// Since: 2020/09/20
//
// This is an implementation of observableFromUrl. It
// does exactly what the name suggests. It opens an
// EventSource for the url passed to the function,
// that listens to the channel provided in  channel.

function observableFromUrl(channel, url) {

    let result = {
        'event_source': new EventSource(url),
        'subscribers': [],
        'items': [],
        'item_count': null,
    }

    result.event_source.addEventListener(channel, (event) => {

        let stream_data = JSON.parse(event.data.replace(/'/g, '"'))[0];

        result.items.push(...stream_data['items']);
        result.item_count = stream_data['item_count'];

        // Call each subscriber
        result.subscribers.forEach((subscriber) => {
            subscriber(stream_data['items']);
        }, { once: true });

        // Closing the connection, once all items were received.
        if (result.item_count === result.items.length) {
            result.event_source.close();
        }
    });

    return result;
}