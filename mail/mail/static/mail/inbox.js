document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').onsubmit = send_mail;
  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  
  columns = [['sender'], ['subject'], ['timestamp']];
  table = document.createElement('div');
  table.classList.add("row");

  table_first_row = document.createElement('div');
  table_first_row.classList.add("first-row-container");

  columns.forEach(col => {
    table_labels = document.createElement('div');
    table_labels.classList.add("text-uppercase", "font-weight-bold", "column-label-styles");
    table_labels.innerHTML = `<p class="first-row-style">${col[0]}</p>`;
    table_first_row.append(table_labels);
  })

  table.append(table_first_row);

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
    .then(emails => {
        emails.forEach(email => {
          columns.forEach(col => {
            row_table = document.createElement('div');
            row_table.classList.add("email-list-style", email["read"] ? "email-read" : "email-unread");
            row_table.innerHTML = `<p class="email-style">${email[col[0]]}</p>`;
            row_table.addEventListener('click', () => view_email(email["id"], mailbox));
            table.append(row_table);
          })
        })
        document.querySelector('#emails-view').append(table);
    });
}

function send_mail() {
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
    })
  })
  .then(response => response.json())
  .then(result => {
    if ('message' in result) {
      load_mailbox('sent');
    } else {
      alert("Complete the receiver!!!");
    }
  });
  return false;
}

function view_email(id, mailbox) {
    // Show email view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'block';
    document.querySelector('#email-view').innerHTML= '';

    email_container = document.createElement('div');
    email_container.classList.add("email-container");
    email_from = document.createElement('p');
    email_from.classList.add("email-labels");
    email_to = document.createElement('p');
    email_to.classList.add("email-labels");
    email_subject = document.createElement('p');
    email_subject.classList.add("email-labels");
    email_timestamp = document.createElement('p');
    email_timestamp.classList.add("email-labels");
    reply_button = document.createElement('button');
    reply_button.classList.add("btn", "btn-sm", "btn-outline-success", "btn-reply");
    reply_button.innerHTML = 'Reply';
    archive_button = document.createElement('button');
    archive_button.classList.add("btn", "btn-sm", "btn-outline-warning", "btn-archive");
    hr = document.createElement('hr');
    email_message = document.createElement('p');
    email_message.classList.add("email-message");

    fetch(`/emails/${id}`)
    .then(response => response.json())
      .then(email => {
        email_from.innerHTML = `<span>From:</span> ${email.sender}`;
        email_container.append(email_from);

        email_to.innerHTML = `<span>To:</span> ${email.recipients}`;
        email_container.append(email_to);

        email_subject.innerHTML = `<span>Subject:</span> ${email.subject}`;
        email_container.append(email_subject);

        email_timestamp.innerHTML = `<span>Timestamp:</span> ${email.timestamp}`;
        email_container.append(email_timestamp);

        reply_button.addEventListener('click', () => {
          reply(email);
        })
        email_container.append(reply_button);

        archive_button.addEventListener('click', () => {
          archive_email(id, !email.archived);
        })
        if (mailbox === 'archive') {
          archive_button.innerHTML = 'Unarchive';
          email_container.append(archive_button);
        } else if (mailbox === 'inbox') {
          archive_button.innerHTML = 'Archive';
          email_container.append(archive_button);
        }

        email_container.append(hr);

        email_body = email.body;
        if (email_body.includes("---")) {
          index = email_body.indexOf("---");
          main_email = email_body.substring(0, index-2);
          re_email = email_body.substring(index, email_body.length);
          email_message.innerHTML = `${main_email}<br><br>${re_email}`;
          email_container.append(email_message);
        } else {
          email_container.append(email_body);
        }

        document.querySelector('#email-view').append(email_container);
      });

    fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
        read: true
      })
    });
}

function archive_email(id, archive) {
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: archive
    })
  }).then(() => load_mailbox("inbox"));
}

function reply(email) {
  compose_email();
  document.querySelector('#compose-recipients').value = email["sender"];
  if (email["subject"].slice(0, 4) === "Re: ") {
    document.querySelector('#compose-subject').value = email["subject"];
  } else {
    document.querySelector('#compose-subject').value = "Re: "+email["subject"];
  }
  document.querySelector('#compose-body').value = "\n\n --- On "+email["timestamp"]+" "+email["sender"]+" wrote: "+email["body"];
}
