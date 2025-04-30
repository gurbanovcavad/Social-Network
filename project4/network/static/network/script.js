document.addEventListener("DOMContentLoaded", function() {
    const follow_btn = document.querySelector("#follow_btn");
    follow_btn.addEventListener("click", function() {
        let username = document.querySelector("#profile").innerHTML;
        // fetch(`/get/${username}/`)
        // .then(response => response.json())
        // .then(data => {
        //     fetch('/follow', {
        //         method: 'POST',
        //         body: JSON.stringify({
        //             user: data.user,
        //             cur: data.cur,
        //             follow: data.is_following ? false : true
        //         })
        //     })
        //     .then(response => {
        //         if (response.ok) {
        //             console.log("OK");
        //         } else {
        //             console.log("Error: ", response.statusText);
        //         }
        //     })
        //     .then(() => {
        //         if (data.is_following) {
        //             follow_btn.innerHTML = "Follow";
        //         } else {
        //             follow_btn.innerHTML = "Unfollow";
        //         }
        //     })
        // })
    });
});