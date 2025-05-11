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