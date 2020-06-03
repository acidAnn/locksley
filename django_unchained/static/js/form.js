/**
 * setup JQuery's AJAX methods to setup CSRF token in the request before sending it off.
 * http://stackoverflow.com/questions/5100539/django-csrf-check-failing-with-an-ajax-post-request
 */
// CONFIG
const QUOTES_ENDPOINT = '/api/quote';
const AUTHORS_ENDPOINT = '/api/author';
const QUOTE_FORMULAR = $('#quote-form');
const QUOTE_FORMULAR_CONTENTS = document.getElementById('quote-form').innerHTML;
const AUTHOR_FORMULAR = $("#author-form");

let source = document.getElementById("entry-template").innerHTML;
let template = Handlebars.compile(source);

/* jshint esversion: 6 */
function ready(fn) {
    if (document.attachEvent ? document.readyState === "complete" : document.readyState !== "loading") {
        fn();
    } else {
        document.addEventListener("DOMContentLoaded", fn);
    }
}

ready(function () {
    updateQuotes();
});

/**
 * Cookie setting for django
 *
 * @param name  cookie name
 * @returns {*}
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            let cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

QUOTE_FORMULAR.submit(function (event) {
    event.preventDefault();
    var url = QUOTE_FORMULAR.attr('action');
    $.ajax({
        url: url,
        type: 'post',
        dataType: 'json',
        data: QUOTE_FORMULAR.serialize(),
        success: quoteSuccessProcess,
        error: displayErrorModal,
    })
});

function clearQuoteFormular() {
    QUOTE_FORMULAR.empty();
    QUOTE_FORMULAR.append(QUOTE_FORMULAR_CONTENTS);
}

function quoteSuccessProcess(data) {
    updateQuotes();
    displaySuccessModal(data);
    clearQuoteFormular();
    updateAuthors();
}

AUTHOR_FORMULAR.submit(function (event) {
    event.preventDefault();
    var url = AUTHOR_FORMULAR.attr('action');
    $.ajax({
        url: url,
        type: 'post',
        dataType: 'json',
        data: AUTHOR_FORMULAR.serialize(),
        success: authorSuccessProcess,
        error: displayErrorModal,
    })
});

function authorSuccessProcess(data) {
    updateAuthors();
    displaySuccessModal(data);
    AUTHOR_FORMULAR[0].reset();
}


function updateQuotes() {
    $.ajax({
        url: QUOTES_ENDPOINT,
        type: 'get',
        dataType: 'json',
        success: resetQuotes,
        error: displayErrorModal,
    })
}

function resetQuotes(data) {
    let quotes = $('#quotes-wrapper');
    let html = '';
    for (const context of data) {
        html += template(context);
    }
    quotes.empty();
    quotes.append(html)
}

function updateAuthors() {
    $.ajax({
        url: AUTHORS_ENDPOINT,
        type: 'get',
        dataType: 'json',
        success: resetAuthorOptions,
        error: displayErrorModal,
    })
}

function resetAuthorOptions(data) {
    let options = '<option value="" selected>---------</option>';
    for (var author of data) {
        options += '<option value="' + author.id + '">' + author.name + '</option>';
    }
    $('.author-select-box').each(function (index) {
        var selected = $(this).val();
        $(this).empty().append(options);
        $(this).val(selected);
    })
}

function displaySuccessModal(data) {
    $('#successModal').modal();
    $("#successGif").attr("src", data.url)
}

function displayErrorModal(data) {
    $('#failModal').modal();
    $("#failGif").attr("src", data.responseJSON.url)
}