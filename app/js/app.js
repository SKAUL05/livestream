document.getElementById("form").addEventListener("submit", sendIdea);

function addUpVote(count) {
  document.getElementById("vote").innerHTML += `<small> ( ${count} ) </small>`;
}

function upvote(ele, id) {
  console.log(id);
  $.ajax({
    url: "/upvote",
    type: "post",
    dataType: "json",
    contentType: "application/json",
    success: function (data) {
      console.log(data);
      addUpVote(data.count);
    },
    data: JSON.stringify({ id: id }),
  });
}

async function sendIdea(e) {
  const text = document.getElementById("idea-text");
  const tech = document.getElementById("idea-tech");
  const viewer = document.getElementById("idea-viewer");

  var jsonToSend = {
    text: text.value,
    tech: tech.value,
    viewer: viewer.value,
  };
  $.ajax({
    url: "/livestream",
    type: "post",
    dataType: "json",
    contentType: "application/json",
    success: function (data) {
      const ideas = JSON.parse(data);
      console.log(ideas);
    },
    data: JSON.stringify(jsonToSend),
  });
  // Clear inputs
  text.value = "";
  tech.value = "";
  viewer.value = "";
}

function renderIdea(idea) {
  document.getElementById(
    "ideas"
  ).innerHTML += `<div class="card my-3" style="background-color: rgb(0,0,0,0.4);">
      <div class="card-body">
        <div class="card-title">
          <h4>${idea.text}</h4>
          <h6>[${idea.tech}]</h6>
        </div>
        <div class="mt-3">
          <em style="font-size: large;">Submitted by ${idea.viewer}</em>
        </div>
        <div class="text-muted">${idea.time}</div> &emsp;
        <div id="vote">
          <i onclick="upvote(this,${idea.id})" class="fa fa-thumbs-up fa-lg"></i>
        </div>
      </div>
    </div>`;
}

async function init() {
  // Find ideas
  $.ajax({
    url: "/livestream",
    type: "get",
    success: function (data) {
      // alert(data);
      document.getElementById("ideas").innerHTML = ``;
      const ideas = JSON.parse(data);
      console.log(ideas);
      // Add existing ideas to list
      ideas.forEach(renderIdea);
      console.log(ideas);
    },
  });
  setTimeout(init, 5000);
}

init();
