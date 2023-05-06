function chat_element(message, me) {
    var sender = message['__str__'];
    var sender_photo_url = message['author'];
    var time = new Date(message['timestamp']);
    var message_content = message['content'];
    var mode = message['mode']
    var msg = document.createElement('div');

    if (mode == 's') {
        msg.classList.add('center-message');
        var msg_child = document.createElement('div');
        msg_child.appendChild(document.createTextNode(message_content));
        msg.appendChild(msg_child);
    }

    if (mode == 'n') {
        msg.classList.add('msg');
        if (sender != me) {
            msg.classList.add('left-msg');
        } else {
            msg.classList.add('right-msg');
        }
        var a_tag = document.createElement('a');
        a_tag.href = sender_photo_url;
        a_tag.target = '_blank';
        var img = document.createElement('div');
        img.classList.add('msg-img');
        img.style = "background-image: url(" + sender_photo_url + ")";
        a_tag.appendChild(img);
        msg.appendChild(a_tag);

        var msg_bubble = document.createElement('div');
        msg_bubble.classList.add('msg-bubble');
        var msg_info = document.createElement('div');
        msg_info.classList.add('msg-info');
        if (sender != me) {
            var msg_info_name = document.createElement('div');
            msg_info_name.classList.add('msg-info-name');
            msg_info_name.appendChild(document.createTextNode(sender));
            msg_info.appendChild(msg_info_name);
        }
        var msg_info_time = document.createElement('div');
        msg_info_time.classList.add('msg-info-time');
        msg_info_time.appendChild(document.createTextNode((time.getHours().toString().padStart(2, '0')) + ':' + time.getMinutes().toString().padStart(2, '0')));

        msg_info.appendChild(msg_info_time);
        msg_bubble.appendChild(msg_info)

        var msg_text = document.createElement('div');
        msg_text.classList.add('msg-text');
        msg_text.appendChild(document.createTextNode(message_content));
        msg_bubble.appendChild(msg_text);

        msg.appendChild(msg_bubble);
    }

    return (msg);
}