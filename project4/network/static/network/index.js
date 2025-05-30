document.addEventListener("DOMContentLoaded", function() {
    const follow_btn = document.querySelector("#follow_btn");
    const followers = document.querySelector("#followers");
    follow_btn.addEventListener("click", function() {
        let username = document.querySelector("#profile").innerHTML;
        console.log(username);
        fetch(`/get/${username}/`)
        .then(response => {
            return response.json();
        })
        .then(data => {
            console.log(data);
            fetch('/follow/', {
                method: 'POST',
                body: JSON.stringify({
                    user: data.user,
                    cur: data.cur,
                    follow: data.is_following ? false : true
                })
            })
            .then(response => {
                console.log(response);
                if (response.ok) {
                    console.log("OK");
                } else {
                    console.log("Error: ", response.statusText);
                }
                return response.json();
            })
            .then(() => {
                let x = followers.innerHTML, a = followers.innerHTML;
                console.log(x.substring(0, 11));
                if (data.is_following) {
                    follow_btn.innerHTML = "Follow";
                    x = a.substring(0, 10) + " " + (parseInt(a.substring(10, a.length)) - 1);
                } else {
                    follow_btn.innerHTML = "Unfollow";
                    x = a.substring(0, 10) + " " + (parseInt(a.substring(10, a.length)) + 1);
                }
                console.log(x);
                followers.innerHTML = x;
            })
        })
    });
});

function pagination(posts) {
    let first = 0, last = 9;
    last = min(posts.length, last);
    const posts_div = document.querySelector("#posts");
    for(let i = first; i <= last; i++) {
        const post = document.createElement("div");
        post.className = "post";
        post.innerHTML = `
            <div id="username"><a href="{% url 'profile' post.owner %}">${posts[i].owner}</a></div>
            {% if request.user == post.owner %}
                <a class="nav-link" style="padding: 0px !important;" href="#">Edit</a>
            {% endif %}
            <div id="content">${posts[i].body}</div>
            <div id="time">${posts[i].created_at}</div>
            <div id="likes">
                <img style="width: 24px; height: 22px; margin-bottom: 3px;" src="data:image/png;base64,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" alt="">
                <span class="like">0</span>
            </div>
        `;
        posts_div.appendChild(post);
    }    
}