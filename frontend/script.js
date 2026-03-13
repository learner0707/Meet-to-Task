// open transcript file picker
function selectTranscript(){

document.getElementById("txtFile").click()

}



// open audio file picker
function selectAudio(){

document.getElementById("audioFile").click()

}



// when transcript selected
document.getElementById("txtFile").addEventListener("change",function(){

const file = this.files[0]

if(!file) return

const reader = new FileReader()

reader.onload = function(e){

const transcript = e.target.result

sendTranscript(transcript)

}

reader.readAsText(file)

})



// when audio selected
document.getElementById("audioFile").addEventListener("change",function(){

const file = this.files[0]

if(!file) return

const formData = new FormData()

formData.append("audio",file)

fetch("/upload-audio",{
method:"POST",
body:formData
})
.then(res=>res.json())
.then(data=>{

showSummary(data.summary)

showIssues(data.tasks)

})

})



// manual analyze
function processTranscript(){

const transcript =
document.getElementById("transcript")?.value

if(!transcript) return

sendTranscript(transcript)

}



// send transcript to backend
function sendTranscript(transcript){

fetch("/process-text",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
transcript: transcript
})

})

.then(res=>res.json())

.then(data=>{

showSummary(data.summary)

showIssues(data.tasks)

})

}



// show summary
function showSummary(summary){

const list =
document.getElementById("summaryList")

list.innerHTML=""

summary.forEach(point=>{

const li = document.createElement("li")

li.textContent = point

list.appendChild(li)

})

}



// show issues
function showIssues(tasks){

const container =
document.getElementById("issuesList")

container.innerHTML=""

const repo =
document.getElementById("repo").value

const token =
document.getElementById("token").value


tasks.forEach(task=>{

const card = document.createElement("div")

card.className="issueCard"

card.innerHTML=`

<h3>${task.title}</h3>

<p>${task.description}</p>

<div class="badges">
<span class="priority">${task.priority}</span>
<span class="category">${task.category}</span>
<span class="status">${task.status}</span>
</div>

<button class="issueBtn">Open GitHub Issue</button>

`

const btn = card.querySelector(".issueBtn")

btn.onclick = async function(){

const res = await fetch("/create-issue",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
repo:repo,
token:token,
task:task
})

})

const data = await res.json()

if(data.issue_url){

window.open(data.issue_url,"_blank")

}

}

container.appendChild(card)

})

}