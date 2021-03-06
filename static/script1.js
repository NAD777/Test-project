window.onload = function () {
    setInterval(() => {
        if (location.href.indexOf('/status') != -1) {
            let status_id = document.querySelectorAll('.status_id');
            let status_text = document.querySelectorAll('.status_text');
            let data = {'id': []};
            for (let i = 0; i < status_text.length; i++) {
                if (status_text[i].textContent.toLowerCase() == 'run') {
                    data['id'].push(status_id[i].textContent);
                }
            }
            // console.log(data);
            ajax('post', '/status_reload', JSON.stringify(data), handler);
        }
    }, 5000);
};

function ajax(method, url, data, callback) {
    let xhr = new XMLHttpRequest();
    xhr.open(method, url, true);
    xhr.addEventListener('readystatechange', () => {
        if (xhr.readyState == 4 && xhr.status == 200) {
            callback(xhr.responseText)
        }
    });
    if (method == 'post') {
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-url');
    }
    xhr.send(data);

}

function handler(text) {
    let data = JSON.parse(text)['data'];
    let status_id = document.querySelectorAll('.status_id');
    let status_text = document.querySelectorAll('.status_text');
    // console.log(data);
    for (let i = 0; i < data.length; i++) {
        for (let j = 0; j < status_text.length; j++) {
            if (status_id[j].textContent == data[i]['id']) {
                if (data[i]['status'] == 'ac') {
                    status_text[j].innerHTML = 'Accepted';
                    status_text[j].classList.add('accepted');
                    status_text[j].classList.remove('uppercase');
                    status_text[j].classList.remove('wa');
                } else {
                    status_text[j].innerHTML = data[i]['status']
                }
                break;
            }
        }
    }
}
