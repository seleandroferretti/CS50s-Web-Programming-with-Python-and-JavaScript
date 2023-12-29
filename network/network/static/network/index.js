document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".like-button").forEach(likedPost => {
        likedPost.onclick = () => like(likedPost)
    })
})

function like(likedPost) {
    const id = likedPost.id;
    fetch(`/post_actions/${id}`, {
        method: "PUT",
        body: JSON.stringify({
            liked: true
        }),
    })
    .then(resp => resp.json())
    .then(res => {
        const likesSelector = document.querySelector(`#likes-post-${id}`);
        const likesCount = parseInt(likesSelector.innerHTML);
        likesSelector.innerHTML = parseInt(res.likes);
        likesCount > parseInt(res.likes) ? likedPost.querySelector("span").innerHTML = "&#129293;" : likedPost.querySelector("span").innerHTML = "&#10084;";
    })
}

function editPost(content) {
    content.style.display="none";
    content.nextElementSibling.style.display = "block";
    content = content.parentElement;
    content = content.previousElementSibling.firstElementChild;
    content.parentElement.classList.add("text-area-width");

    const inputText = document.createElement("textarea");
    inputText.classList.add("h-100", "w-100");
    inputText.innerHTML = content.innerHTML;

    content.parentElement.replaceChild(inputText, content);
}

function savePost(content, id) {
    content.style.display = "none";
    content.previousElementSibling.style.display = "block";
    content = content.parentElement;
    content = content.previousElementSibling.firstElementChild;
    content.parentElement.classList.remove("text-area-width");
 
    const paragraph = document.createElement("p");
    paragraph.setAttribute('id', 'post-content');
    paragraph.innerHTML = content.value;
    
    content.parentElement.replaceChild(paragraph, content);

    fetch(`/post_actions/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            change_saved: true,
            content: paragraph.innerHTML
        })
    })
}