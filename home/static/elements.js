function chat_element(message) {
    var have_last_message = false;
    var last_message_content;
    var sender;
    var time = new Date(message.created_time);
    var room_name = message.name.slice(5);
    var image_last_sender;
    if (message.last_message.content) {
        have_last_message = true;
        last_message_content = message.last_message.content;
        sender = message.last_message.__str__;
        time = new Date(message.last_message.timestamp);
        image_last_sender = message.last_message.author
    }
    var container = document.createElement('div');
    container.classList.add('container');
    container.classList.add('darker');
    if (have_last_message) {
        var img = document.createElement('img');
        img.src = image_last_sender;
        img.classList.add('right');
        img.style = "width: 100%";
        container.appendChild(img);
    }

    var chname = document.createElement('p');
    chname.style = "font-weight: bold; font-size: 20px;";
    chname.appendChild(document.createTextNode(room_name));
    container.appendChild(chname);
    if (have_last_message) {
        var msgcontent = document.createElement('p');

        msgcontent.appendChild(document.createTextNode(sender + '\t:\t' + last_message_content));
        container.appendChild(msgcontent);

    }
    var msgtime = document.createElement('span');
    msgtime.classList.add("time-left");
    msgtime.appendChild(document.createTextNode((time.getHours().toString().padStart(2, '0')) + ':' + time.getMinutes().toString().padStart(2, '0')));
    container.appendChild(msgtime);
    // var msg_info = document.createElement('div');
    // msg_info.classList.add('msg-info');
    // var msg_info_name = document.createElement('div');
    // msg_info_name.classList.add('msg-info-name');
    // msg_info_name.appendChild(document.createTextNode(sender));
    // var msg_info_time = document.createElement('div');
    // msg_info_time.classList.add('msg-info-time');
    // msg_info_time.appendChild(document.createTextNode((time.getHours().toString().padStart(2, '0')) + ':' + time.getMinutes().toString().padStart(2, '0')));
    // msg_info.appendChild(msg_info_name);
    // msg_info.appendChild(msg_info_time);
    // msg_bubble.appendChild(msg_info)

    // var msg_text = document.createElement('div');
    // msg_text.classList.add('msg-text');
    // msg_text.appendChild(document.createTextNode(message_content));
    // msg_bubble.appendChild(msg_text);

    // msg.appendChild(msg_bubble);


    // return (msg);
    return container
}